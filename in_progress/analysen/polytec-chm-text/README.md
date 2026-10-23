# Polytec-Hilfedateien als durchsuchbarer Text

> **Hinweis:** Der Inhalt dieses Ordners ist Dokumentation der Polytec GmbH
> (© Polytec). Die Textfassung dient nur der internen Projektarbeit an der
> Bachelorarbeit (Nachschlagen, Durchsuchen, Belegen). Nicht weitergeben, nicht
> veröffentlichen, nicht wörtlich in die Thesis übernehmen; in der Thesis wird die
> Original-CHM zitiert.

## Herkunft

| Ordner | Quelle (unter `Input/literatur/polytec/Windows Hilfedateien/`) | SHA-256 der Quelle |
|---|---|---|
| `basic-engine-manual/` | `Basic Engine Manual.chm` (8 279 021 Byte) | `87bddc36752e4374b2565ac13d546a1356eb8f36243a136d2058966ad615c33a` |
| `polytec-file-access/` | `Polytec File Access_Object Model Reference.chm` (4 919 012 Byte) | `a6333106b9e8ae282e5ff6e94f78e0e81e85dd88104432b5ff81cab04e230fad` |

Eine Versionsangabe enthalten die CHM-Dateien nicht. Einziger Hinweis: Ein Beispiel
öffnet `C:\ProgramData\Polytec\PSV\10.4\Examples\Data\Example.svd`
(`POLYPROPERTIESLib/GeneratorAcqPropertiesContainer.md`). Die Hilfe beschreibt also
mindestens den Stand von PSV 10.4.

## Aufbau

- Ein Unterordner je Typbibliothek, z. B. `PSV/`, `POLYFILELib/`, `POLYPROPERTIESLib/`,
  `POLYSIGNALLib/`, `POLYWAVEFORMSLib/`, `Polytec_IO_VibInterfaces/`.
- **Eine Datei je Objekt, Collection, Interface oder Enumeration**, z. B.
  `PSV/Acquisition.md`. Darin stehen alle CHM-Themen dieses Objekts hintereinander:
  Objektbeschreibung, Mitgliederliste, jede Methode, jede Property und jedes Event.
- Jedes Thema beginnt mit `## <Titel>` und der Zeile
  `*Quelle: \`<CHM-Themendatei>.html\` · <Typbibliothek> · <Brotkrumen>*`.
  Mit diesem Dateinamen wird im Referenzdokument zitiert, z. B. `[BEM] PSV~Acquisition~ScanEx`.
- `<Bibliothek>/_Library.md` enthält die Übersichtsseite der Typbibliothek.
- `_Konzept/` enthält die Einführungskapitel (z. B. „Access to Data“, „Using
  Collections“, „Examples“).
- `INDEX.md` je CHM listet alle Dateien mit der Anzahl der enthaltenen CHM-Themen.
- Code-Beispiele (VB/WinWrap Basic) stehen als Codeblöcke im Abschnitt `### Example`.
- Weggelassen wurden nur Navigation („See Also“, „Collapse All“), Skripte, Stylesheets,
  Bilder und Objektmodell-Diagramme. Die Diagramme sind Grafiken; im Text bleibt
  nur die leere Überschrift `### Object Model` stehen.

Beide CHM-Dateien überschneiden sich stark: Polytec File Access enthält alle
Bibliotheken außer `PSV` und `PolyAcquisitionLib`. Die gemeinsamen Themen sind bis
auf Leerzeichen gleich. Nur in der PFA-Fassung gibt es einige neuere Interfaces,
z. B. `IVibrometersAcqProperties5` und `IFrontEnd3`.

## Umfang

- `basic-engine-manual/`: 560 Dateien, 4376 CHM-Themen, rund 2,5 MB
- `polytec-file-access/`: 358 Dateien, 2406 CHM-Themen, rund 1,5 MB
- **Gesamt: rund 4,0 MB, also unter der Grenze von 10 MB.** Beide Hilfedateien sind
  deshalb **vollständig** abgelegt, ohne Auswahl.

## Erzeugung (Stand 2026-10-23, Paket I5)

Erzeugt in der Cloud-Sitzung (Linux) mit `libchm-bin` 0.40a (`extract_chmLib`),
Python 3 und BeautifulSoup 4.15:

```bash
extract_chmLib "Basic Engine Manual.chm" chm/Basic_Engine_Manual
extract_chmLib "Polytec File Access_Object Model Reference.chm" chm/PFA
python3 -I werkzeug/chm2md.py chm/Basic_Engine_Manual basic-engine-manual \
    "chm/Basic_Engine_Manual/Basic Engine Manual.hhc"
python3 -I werkzeug/chm2md.py chm/PFA polytec-file-access \
    "chm/PFA/Polytec File Access_Object Model Reference.hhc"
```

`werkzeug/chm2md.py` ist das verwendete Umwandlungsskript. Es ist ein Hilfswerkzeug
der Analyse und gehört nicht zum Softwarepaket. Die Reihenfolge der Themen in einer
Datei folgt dem Inhaltsverzeichnis (`.hhc`) der CHM.

## Suchen

```bash
grep -rn "ScanFileName" in_progress/analysen/polytec-chm-text/
grep -rln "ptcDisplayMagPhaseRad" in_progress/analysen/polytec-chm-text/
```

Die Auswertung dieser Texte steht in
`in_progress/analysen/2026-10-23_I5_com-referenz.md`.
