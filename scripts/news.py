"""Generate the home page's latest news, the news index and optional articles."""

import json
import posixpath
import re
import sys
from datetime import datetime
from html import escape
from pathlib import Path, PurePosixPath
from string import Template
from urllib.parse import quote


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
DATA = ROOT / "data" / "news"
LATEST_COUNT = 3
START = "<!-- news:start -->"
END = "<!-- news:end -->"
ARTICLE_MARK = "<!-- mlps-generated-news-article -->"


def required_text(record, field):
    value = record.get(field)
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field} must be a nonempty string")
    return value.strip()


def image_path(value):
    path = PurePosixPath(value)
    if not path.is_relative_to("/assets/media") or ".." in path.parts:
        raise ValueError(f"Image path must start with /assets/media/: {value}")
    if not (DOCS / path.relative_to("/")).is_file():
        raise ValueError(f"Missing image: {value}")
    return str(path)


def read_stories():
    stories = []
    for file in sorted(DATA.glob("*.json")):
        try:
            story = json.loads(file.read_text(encoding="utf-8"))
            slug = file.stem
            if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", slug) or slug == "index":
                raise ValueError("Use a lowercase filename with words separated by hyphens")
            for key in ("title", "summary", "date"):
                story[key] = required_text(story, key)
            story["day"] = datetime.fromisoformat(story["date"]).date()
            story["slug"] = slug
            pictures = story.setdefault("images", [])
            if not isinstance(pictures, list):
                raise ValueError("images must be a list")
            for photo in pictures:
                photo["file"] = image_path(required_text(photo, "file"))
                photo["thumbnail"] = image_path(photo.get("thumbnail", photo["file"]))
                photo["alt"] = required_text(photo, "alt")
            if story.get("article"):
                file_name = required_text(story, "article")
                if not re.fullmatch(r"[a-z0-9-]+\.html", file_name):
                    raise ValueError("article must name an HTML fragment in data/news/")
                story["article"] = (DATA / file_name).read_text(encoding="utf-8").strip()
                if not story["article"]:
                    raise ValueError("The article fragment is empty")
            stories.append(story)
        except (ValueError, OSError, KeyError, TypeError) as error:
            raise ValueError(f"{file.name}: {error}") from error
    return sorted(stories, key=lambda s: (s["day"], s["date"], s["slug"]), reverse=True)


def photo_link(photo, page_dir, thumbnail):
    original = quote(posixpath.relpath(photo["file"], page_dir), safe="/-_.~")
    display = photo["thumbnail"] if thumbnail else photo["file"]
    image = quote(posixpath.relpath(display, page_dir), safe="/-_.~")
    alt = escape(photo["alt"], quote=True)
    return (
        f'<a class="news-photo" data-news-photo href="{original}" aria-label="Enlarge image: {alt}">'
        f'<img decoding="async" loading="lazy" src="{image}" alt="{alt}"></a>'
    )


def story_card(story, page_dir):
    headline = escape(story["title"])
    if story.get("article"):
        target = posixpath.relpath("/news/" + story["slug"] + ".html", page_dir)
        headline = f'<a href="{target}">{headline}</a>'
    figures = ""
    if story["images"]:
        photos = "\n".join(photo_link(photo, page_dir, True) for photo in story["images"])
        figures = f'<figure class="entry-image">{photos}</figure>'
    day = story["day"]
    month = ("Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec")[day.month - 1]
    published = f"{month} {day.day}, {day.year}"
    return f'''<li class="wp-block-post hentry category-news">
  <div class="wp-block-group mlps-news-item"><div class="wp-block-group__inner-container is-layout-constrained wp-block-group-is-layout-constrained">
    <div class="entry-date"><time datetime="{escape(story['date'])}">{published}</time></div>
    <div class="wp-block-group mlps-news-text"><div class="wp-block-group__inner-container is-layout-constrained wp-block-group-is-layout-constrained">
      <h2 class="entry-heading">{headline}</h2>
      <div class="entry-excerpt"><p class="entry-excerpt__excerpt">{escape(story['summary'])}</p></div>
    </div></div>
    {figures}
  </div></div>
</li>'''


def replace_once(source, pattern, replacement, description):
    matches = list(re.finditer(pattern, source, flags=re.DOTALL | re.IGNORECASE))
    if len(matches) != 1:
        raise ValueError(f"Expected exactly one {description}, found {len(matches)}")
    start, end = matches[0].span()
    return source[:start] + replacement + source[end:]


def with_assets(source, prefix):
    css = prefix + "assets/lightbox.css"
    js = prefix + "assets/news.js"
    needed = []
    if f'href="{css}"' not in source:
        needed.append(f'<link rel="stylesheet" href="{css}">')
    if f'src="{js}"' not in source:
        needed.append(f'<script src="{js}" defer></script>')
    if needed:
        return replace_once(source, r"</head>", "\n".join(needed) + "\n</head>", "head closing tag")
    return source


def render_list(source, stories, page_dir):
    items = "\n".join(story_card(story, page_dir) for story in stories)
    block = START + "\n" + items + "\n" + END
    page = replace_once(source, re.escape(START) + r".*?" + re.escape(END), block, "news marker pair")
    return with_assets(page, "" if page_dir == "/" else "../")


def render_detail(source, template, story):
    photos = "\n".join(
        '<div class="post-thumb entry-media thumbnail">' + photo_link(photo, "/news", False) + "</div>"
        for photo in story["images"]
    )
    title = escape(story["title"])
    main = template.substitute(headline=title, article=story["article"], photos=photos)
    page = replace_once(source, r"<main\b[^>]*>.*?</main>", main.strip(), "main element")
    # The news index supplies the shared navigation, scripts and style references.
    # Article body classes keep Sinatra's original, narrower reading column.
    body = re.search(r'<body\b[^>]*\bclass="([^"]*)"', page, flags=re.I)
    if not body:
        raise ValueError("News index has no body class")
    classes = [c for c in body[1].split() if c != "page" and c != "page-template-default" and not c.startswith("page-id-")]
    classes.extend(("post-template-default", "single", "single-post", "single-format-standard", "si-single-title-in-content", "narrow-content"))
    page = page[:body.start(1)] + " ".join(dict.fromkeys(classes)) + page[body.end(1):]
    page = replace_once(page, r"<title>.*?</title>", f"<title>{title} – Machine Learning and Positioning Systems</title>", "document title")
    canonical = f'https://mlps-lab.de/news/{story["slug"]}.html'
    return replace_once(page, r'<link\b(?=[^>]*\brel="canonical")[^>]*>', f'<link rel="canonical" href="{canonical}">', "canonical URL")


def main():
    news = DOCS / "news"
    home = DOCS / "index.html"
    archive = news / "index.html"
    stories = read_stories()
    template = Template((ROOT / "templates" / "news-article.html").read_text(encoding="utf-8"))
    output = {
        home: render_list(home.read_text(encoding="utf-8"), stories[:LATEST_COUNT], "/"),
        archive: render_list(archive.read_text(encoding="utf-8"), stories, "/news"),
    }
    for story in stories:
        if not story.get("article"):
            continue
        target = news / (story["slug"] + ".html")
        if target.exists() and ARTICLE_MARK not in target.read_text(encoding="utf-8"):
            raise ValueError(f"An independently edited page already exists at {target.name}")
        output[target] = render_detail(output[archive], template, story)
    # Validate every source before touching any of the published pages.
    for target, content in output.items():
        if not target.exists() or target.read_text(encoding="utf-8") != content:
            target.write_text(content, encoding="utf-8")
    for old in news.glob("*.html"):
        if old not in output and ARTICLE_MARK in old.read_text(encoding="utf-8"):
            old.unlink()
    print(f"{len(stories)} news entries, {len(output) - 2} articles")


if __name__ == "__main__":
    try:
        main()
    except (ValueError, OSError) as problem:
        sys.exit(str(problem))
