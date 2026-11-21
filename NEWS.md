# News veröffentlichen

Eine vorhandene JSON-Datei unter `data/news/` kopieren. Der neue Dateiname bestimmt die Adresse des ausführlichen Beitrags. Kleinbuchstaben und Bindestriche verwenden.

Für eine kurze Meldung genügen diese Angaben:

```json
{
  "title": "New seminar announced",
  "date": "2026-11-20",
  "summary": "Registration for the winter seminar is open."
}
```

Für ein Bild das Feld `images` wie in den vorhandenen Meldungen ergänzen. `file` verweist auf das große Bild unter `/assets/media/`, `thumbnail` optional auf eine kleinere Vorschau. In `alt` den Bildinhalt beschreiben.

Für einen ausführlichen Beitrag zusätzlich `"article": "new-seminar.html"` eintragen und unter `data/news/new-seminar.html` den Artikel als HTML-Fragment schreiben. Die angegebenen Bilder erscheinen auch im Artikel. Weitere Bilder im Text lassen sich mit relativen Pfaden wie `../assets/media/2026/11/seminar.jpg` einfügen.

Im Projektordner `python3 scripts/news.py` ausführen. Auf der Startseite erscheinen die drei neuesten Meldungen, im News-Archiv alle. Bei einem ausführlichen Beitrag führt die Überschrift zum Artikel. Quelldateien, Medien und geänderte Seiten unter `docs/` gemeinsam committen.
