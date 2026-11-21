"""Compare two docs directories in Chromium at desktop and mobile sizes.

Usage: python scripts/compare_layout.py ../mlps-lab-v3/docs docs ./layout-diffs
Requires Playwright with Chromium installed, and Pillow.
"""
import argparse
from io import BytesIO
from pathlib import Path

from PIL import Image, ImageChops
from playwright.sync_api import sync_playwright


def screenshot(context, path):
    page = context.new_page()
    try:
        page.goto(path.as_uri(), wait_until="load")
        page.locator("img").evaluate_all("(images) => Promise.all(images.map(img => {"
                                         "img.loading = 'eager'; return img.decode().catch(() => {}); }))")
        page.evaluate("document.fonts.ready")
        return Image.open(BytesIO(page.screenshot(full_page=True, animations="disabled"))).convert("RGB")
    finally:
        page.close()


def difference(before, after):
    size = (max(before.width, after.width), max(before.height, after.height))
    canvases = []
    for image in (before, after):
        padded = Image.new("RGB", size)
        padded.paste(image)
        canvases.append(padded)
    return ImageChops.difference(*canvases)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("before", "after", "output"):
        parser.add_argument(name, type=Path)
    args = parser.parse_args()
    pages = sorted(args.after.resolve().rglob("*.html"))
    changed = 0
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        for width, height in [(1440, 900), (768, 1024), (390, 844)]:
            context = browser.new_context(viewport={"width": width, "height": height}, reduced_motion="reduce")
            context.route("https://**/*", lambda route: route.abort())
            for page in pages:
                relative = page.relative_to(args.after.resolve())
                old = args.before.resolve() / relative
                if relative.as_posix() == "team/application-guidelines.html" and not old.exists():
                    old = args.before.resolve() / "uncategorized/application-guidelines.html"
                before = screenshot(context, old)
                after = screenshot(context, page)
                diff = difference(before, after)
                if diff.getbbox() or before.size != after.size:
                    changed += 1
                    target = args.output / str(width) / relative.with_suffix(".png")
                    target.parent.mkdir(parents=True, exist_ok=True)
                    diff.save(target)
                    print(width, relative)
            context.close()
        browser.close()
    print(f"{changed} differing snapshots out of {len(pages) * 3}")
    return int(changed > 0)


if __name__ == "__main__":
    raise SystemExit(main())
