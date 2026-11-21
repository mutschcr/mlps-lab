# MLPS Lab – Website pflegen

Die veröffentlichte Website steht unter `docs/`. Sie besteht aus HTML, CSS und JavaScript. Python ab 3.11 wird für die Listen mit Publikationen, Abschlussarbeiten und News gebraucht.

## Wo ändere ich was?

| Aufgabe | Dateien |
|---|---|
| Biografie oder eigene Lehre ändern | `docs/team/<person>/index.html`. Weitere Publikationsseiten unter `page/2/`, `page/3/` usw. entstehen automatisch nach jeweils 25 Publikationen. Profilfoto und Bild für die Teamübersicht liegen im selben Personenordner. Der Abschnitt **Teaching** wird von Hand gepflegt, neuestes Semester zuerst. |
| Kursseite oder Materiallink ändern | `docs/teaching/`; auch die Übersicht in `index.html` prüfen. |
| Abschlussarbeit bearbeiten | Eine TOML-Datei pro Thema in `data/theses/`. Anleitung: [THESES.md](THESES.md). |
| Datensatz beschreiben | `docs/research/datasets/`. Weitere Forschungsseiten liegen direkt in `docs/research/`. |
| Bewerbungsinfos | `docs/team/application-guidelines.html` |
| Paper eintragen | Anleitung: [PUBLICATIONS.md](PUBLICATIONS.md). Eine Datei pro Paper in `data/publications/`. Eine ähnliche Datei als Vorlage verwenden und den Eintrag mit `profiles` den Personen zuordnen. Das Vorschaubild liegt als PNG unter `docs/assets/media/publications/<TOML-Dateiname ohne Endung>.png`. Den Pfad unter `[image]` als `src` eintragen. |
| Publikation hervorheben | Auswahl und Reihenfolge in `data/publication-highlights.toml`. |
| Nachricht veröffentlichen | Eine Datei pro Meldung in `data/news/`. Der Kurztext genügt, für einen ausführlichen Artikel kann ein eigener Text mit Bildern ergänzt werden. Siehe [NEWS.md](NEWS.md). |
| Farben, Schrift oder Links ändern | `docs/assets/css/style.css`; Bereichsstile im selben Verzeichnis. |
| Bild hinzufügen | `docs/assets/media/`, zum Beispiel im Unterordner für Jahr und Monat. Für größere Dokumente die Datei zuerst auf `download.cmutschler.de` hochladen und dann ihre HTTPS-Adresse im Inhalt verwenden. |

## Lokal testen

Im Projektordner starten und anschließend http://localhost:8000 öffnen.

```sh
python3 scripts/publications.py
python3 scripts/news.py
python3 scripts/theses.py
python3 -m http.server 8000 --directory docs
```

Die Generatoren sind nach Änderungen an ihren Quelldaten auszuführen. Generierte Seiten und Quelldateien gemeinsam committen. Auf Personenprofilen bleiben Biografie und Teaching manuell bearbeitbar; der Generator verwaltet den markierten Publikationsabschnitt.

## Veröffentlichen

In GitHub unter **Settings → Pages** den gewünschten Branch und **/docs** als Quelle wählen. Die statischen Seiten funktionieren auch unter einem Repository-Unterpfad. Die Neuordnung ändert alte Seitenadressen. Externe Links auf frühere Personen-, Kurs- oder Themenpfade bei der Domainumstellung aktualisieren.

## Übernommene Medien

`python3 scripts/fetch_media.py --check` prüft den Bestand aus der früheren Mediathek. Hinweise zu den zwei extern zu hinterlegenden PDFs und zu fehlenden Originalauflösungen stehen in der Medien-Dokumentation.

## Layout vergleichen

`scripts/compare_layout.py` vergleicht zwei entpackte Website-Versionen bei 390, 768 und 1440 Pixeln Breite. Benötigt werden Python mit Playwright und Pillow sowie der Playwright-Chromium-Browser. Den Aufruf zeigt `python scripts/compare_layout.py --help`. Abweichungen werden als PNG gespeichert. Bei bewegten Bildinhalten können auch unterschiedliche Animationsphasen als Abweichung erscheinen.
