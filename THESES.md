# Abschlussarbeiten und Projekte pflegen

Eine Datei in `data/theses/` entspricht einem Thema. Alle Angaben für die Karte und die Detailseite stehen in dieser TOML-Datei. Dateinamen folgen dem Schema `vorname-nachname-titel-des-themas.toml`. Der Generator prüft den Namen anhand von `student` und `title`. Bei offenen Themen dient der Name der betreuenden Person in `filename_owner` als Präfix. Fehlt im Altbestand jeder Name, wird `unknown-student` verwendet. Akzente entfallen, ß wird ss. Das Beispiel unten heißt `jonathan-ott-wireless-channel-models.toml`.

Bei einer Umbenennung hält `detail_slug` die bisherige HTML-Adresse stabil. Alle importierten Arbeiten haben dieses Feld.

## Ein Thema anlegen

```toml
title = "Wireless Channel Models"
type = "Master Thesis"
status = "open"
tags = ["5G & 6G", "Wireless Sensing"]
posted = "2026-11-21"
summary = "Investigate how channel models generalize across indoor environments."
filename_owner = "Jonathan Ott"
supervisors = ["Jonathan Ott", "Christopher Mutschler"]
body_html = '''
<p>Describe the research question and the tasks here.</p>
<h2>Required skills</h2>
<ul><li>Python</li></ul>
'''
```

- Pflichtfelder sind `title`, `type` und `status`. Für `type` normalerweise `Master Thesis`, `Bachelor Thesis` oder `Project` verwenden. Tags sind frei wählbar. Vorhandene Schreibweisen wiederverwenden.
- `summary` ist der Kurztext der Karte. `body_html` enthält den ausführlichen Text mit Absätzen, Listen, Bildern und Links. Ohne Langtext erscheint die Zusammenfassung auf der Detailseite. Links innerhalb des Inhalts sind relativ zu `docs/theses/`.
- Optional lassen sich `student`, `institution`, `supervisors` (Namensliste) und `image` setzen. Ein Kartenbild liegt beispielsweise unter `docs/assets/media/theses/channel.png`; der Eintrag lautet dann `image = "../assets/media/theses/channel.png"`.
- `open` bedeutet ausgeschrieben, `running` vergeben und in Bearbeitung, `finished` abgeschlossen. Bei Vergabe Status und gegebenenfalls `student` ändern. Bei Abschluss `status = "finished"` und das Abschlussdatum in `finished` setzen.
- Die Karte zeigt je nach Status `posted`, `started` oder `finished`. Werte als `"YYYY-MM-DD"` oder `"YYYY"` angeben. Unbekannte Werte bleiben leer und erscheinen als „Not recorded“. Bei Finished folgen undatierte Arbeiten nach den datierten.
- Bei Vergabe `student` und `started` ergänzen, den Dateinamen auf den Bearbeiter umstellen und den vorherigen URL-Namen in `detail_slug` behalten. Die Liste `supervisors` kann mehrere Namen enthalten. Das lokale Ersatzbild wird automatisch verwendet, wenn `image` fehlt.
- Die Statusbuttons öffnen die statischen Übersichten `index.html`, `running.html` und `finished.html`. Finished zeigt zehn Arbeiten pro Seite; weitere Seiten heißen `finished-2.html` usw.

## Erzeugen und prüfen

Im Projektordner `python3 scripts/theses.py` ausführen (Python 3.11 oder neuer). Anschließend mit `python3 -m http.server 8000 --directory docs` starten und unter `http://localhost:8000/theses/` die drei Filter und den Link zur Detailseite prüfen. TOML, neue Bilder und generierte HTML-Dateien gemeinsam committen. Eine entfernte TOML-Datei entfernt beim nächsten Lauf auch ihre generierte Detailseite.

Die Übersicht startet mit Open. Open und Running sind alphabetisch nach dem Titel sortiert, Finished absteigend nach Datum. Alle drei Typen können in jeder Ansicht erscheinen. Die Layoutvorlagen liegen in `templates/theses-index.html` und `templates/thesis-detail.html`, die Gestaltung in `docs/assets/css/theses.css`.

## Hinweise zum übernommenen Bestand

Die beiden älteren Themen zu elektrischen Schaltungen und zur Koordination von 6G-Basisstationen hatten im Export keinen Status. Sie sind gemäß der Vorgabe, dass nur Diffusion offen ist, als Finished einsortiert. Die Dateinamen der bestehenden Themen wurden für vorhandene Links beibehalten.
