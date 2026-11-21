# Publikationen pflegen

Jedes Paper erhält eine TOML-Datei in `data/publications/`. Eine Publikation wird einmal eingetragen und über `profiles` allen beteiligten Teammitgliedern zugeordnet.

## Dateinamen und Bilder

Die vorhandenen Dateinamen folgen dem Muster `<kurztitel-in-kleinbuchstaben>-<id>.toml`. Wörter werden mit Bindestrichen getrennt. Bei importierten Papern ist die Zahl die bisherige WordPress-ID. Für neue Einträge einen eindeutigen Namen vergeben; zur Fortführung des Musters eine freie numerische ID verwenden. Dateinamen nach Veröffentlichung stabil halten.

Das PNG-Thumbnail trägt **denselben Basisnamen wie die TOML-Datei**. Beispiel:

- `data/publications/active-sensing-with-meta-reinforcement-learning-for-emitter-localization-4195.toml`
- `docs/assets/media/publications/active-sensing-with-meta-reinforcement-learning-for-emitter-localization-4195.png`

## TOML-Beispiel

```toml
title = "A New Method for Wireless Sensing"
authors = ["Jonathan Ott", "Christopher Mutschler"]
date = "2026-11-21"
venue = "Example Conference"
profiles = ["jonathan-ott", "christopher-mutschler"]

[links]
Website = "https://example.org/paper"

[image]
src = "/assets/media/publications/a-new-method-for-wireless-sensing-5000.png"
alt = "Comparison of positioning accuracy across three environments"
```

`title` und `date` sind erforderlich. Ein Jahr allein ist zulässig. Die Profilkennungen stehen in `data/publication-views.json`. Ohne Bild den Block `[image]` weglassen. Ein Bild wird über `src` eingebunden. Zusätzliche Felder wie `abstract`, `pdf_url`, `doi` (als HTTPS-URL) und `bibtex` **vor** dem ersten Tabellenkopf wie `[links]` eintragen. Für längeren Text bietet TOML mehrzeilige Strings an. Weitere beschriftete Links, etwa Code oder Dataset, gehören in `[links]`.

## Highlights und Veröffentlichung

Hervorgehobene Arbeiten separat in `data/publication-highlights.toml` pflegen. Einen vorhandenen Block `[[highlights]]` samt Bild als Vorlage verwenden. Bild und Beschriftung bestimmen die Darstellung; die Reihenfolge der Blöcke bestimmt die Reihenfolge auf der Website.

Im Projektordner `python3 scripts/publications.py` ausführen. Der Generator aktualisiert die zentrale Liste, die Highlight-Auswahl und die paginierten Personenprofile. Mit `python3 -m http.server 8000 --directory docs` lokal prüfen und Quelldateien, Thumbnail und generierte HTML-Dateien gemeinsam committen.
