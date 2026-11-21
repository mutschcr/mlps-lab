# Bilder und öffentliche Downloads

Die Website lädt ihre lokalen Bilder aus `docs/assets/media/`. Die übernommenen Lehrstuhl-Bilder liegen dort nach Jahr und Monat sortiert. Die fünf Abbildungen der DEBS Grand Challenge liegen unter `docs/assets/media/debs.org/grand-challenges/2013/`.

`media-sources.json` enthält die Originaladressen von 199 öffentlich verwendeten Bildern und zwei PDFs aus dem WordPress-Export. Von den Bildern sind 139 in Originalgröße verfügbar, weitere 59 in einer anderen Originalgröße desselben Motivs. Für eine Publikationsgrafik fehlt die Datei. `local_variant` nennt die mitgelieferte Alternative. `variants` führt die im Export verzeichneten Größen auf. Die in `status_at_export` genannten Werte beschreiben den Stand der Übernahme.

## Originale nachladen

Im Projektordner ausführen. `--check` liest nur die vorhandenen Dateien. `--missing-only` versucht die fehlende Grafik und die beiden PDFs über ihre bisherigen öffentlichen Originaladressen zu beziehen. Ein Lauf ohne Optionen versucht zusätzlich die 59 fehlenden Bildoriginale.

```sh
python3 scripts/fetch_media.py --check
python3 scripts/fetch_media.py --missing-only
```

Bilder werden unter `docs/assets/media/YYYY/MM/` mit ihrem Originalnamen gespeichert. Das Skript aktualisiert die relativen Bildverweise im HTML und die Zuordnungen für neu erzeugte Publikationsseiten. Wer eine Originaldatei direkt aus dem bisherigen Webspace übernimmt, kann sie dort ablegen und danach `python3 scripts/fetch_media.py --relink-only` ausführen.

## PDFs für den Downloadserver

Für die beiden PDFs ist der Upload noch offen. Die folgende Tabelle ordnet jeder Quelle aus dem Export den vorgesehenen Zielpfad auf dem Downloadserver zu.

| Bisherige Quelle im Export | Vorgesehener Upload und künftiger Link |
|---|---|
| <https://mlps-lab.de/wp-content/uploads/2020/04/NLOS_CNN_ICL__2020_.pdf> | <https://download.cmutschler.de/documents/NLOS_CNN_ICL__2020_.pdf> |
| <https://mlps-lab.de/wp-content/uploads/2020/07/SoSe_2020-Reinforcement_Learning_%E2%80%93_Seminar.pdf> | <https://download.cmutschler.de/documents/SoSe_2020-Reinforcement_Learning_%E2%80%93_Seminar.pdf> |

Das Skript legt erfolgreich geladene PDFs in `../mlps-download-staging/documents/` neben dem Projektordner ab. Mit `--documents-dir PFAD` lässt sich ein anderer Ablageort außerhalb von `docs/` wählen. Zum Veröffentlichen die beiden Originaldateien unter ihrem Dateinamen in `/documents/` auf dem Downloadserver ablegen und dort öffnen. Der Dateiname des Seminar-PDFs enthält zwischen den Unterstrichen einen Gedankenstrich (`–`, U+2013).

Die bestehenden externen Kursarchive und Forschungsdatensätze werden weiterhin über ihre bisherigen Adressen angeboten.
