"""Serienverwaltung von Ansicht 5 (R-058/R-059, P-AUSW2 S7; UI-12, UI-14, UI-18, UI-20): ohne Qt."""

from __future__ import annotations

import re

import pytest
from gui_ausw_hilfen import synth_geladen

from ldv_automation.darstellung.auswahl import PaarCache
from ldv_automation.darstellung.serien_daten import SerienSpec
from ldv_automation.gui.messungen import Messung, Messungen
from ldv_automation.gui.serien import (
    SERIEN_MAX,
    TEXT_SERIE_DOPPELT,
    TEXT_SERIEN_VOLL,
    SerienFehler,
    SerienListe,
    baue_spec,
    groessen_verfuegbar,
    komponente_von_paar,
    kopf_text,
    messungs_zugriff,
    paare_je_messung,
    serie_text,
    serien_aus_ansicht,
    serien_fuer_alle,
    standard_paar,
    stempel_dateien,
    uebernimm,
    unmoeglich_text,
)

PAAR = ("Vib X", "Ref1")


def messung(liste: Messungen, pfad: str, **kw: object) -> Messung:
    m = liste.hinzufuegen(pfad)
    g = synth_geladen(pfad=pfad, **kw)  # type: ignore[arg-type]
    return liste.fertig(
        m.id, geladen=g, cache=PaarCache(g.messdaten), antrieb=None, paare=tuple(g.messdaten.cp)
    )


def h1(mid: int, label: int | None = None) -> SerienSpec:
    return baue_spec(mid, label, "h1", kanalpaar=PAAR)


def test_slot_ist_der_niedrigste_freie_und_bleibt_beim_entfernen() -> None:
    liste = SerienListe()
    a, b, c = (liste.hinzufuegen(h1(1, 10 + i)) for i in range(3))
    assert [s.slot for s in (a, b, c)] == [0, 1, 2]
    liste.entferne(1)  # die zweite Serie geht, die dritte behält Slot 2
    assert [s.slot for s in liste.specs] == [0, 2]  # UI-18, UI-20
    neu = liste.hinzufuegen(h1(1, 13))
    assert neu.slot == 1  # die Lücke wird gefüllt


def test_doppelte_serie_und_fuenfte_serie_werden_abgelehnt_mit_hinweistext() -> None:
    liste = SerienListe()
    liste.hinzufuegen(h1(1, 10))
    with pytest.raises(SerienFehler, match=TEXT_SERIE_DOPPELT):
        liste.hinzufuegen(h1(1, 10))
    for i in range(1, SERIEN_MAX):
        liste.hinzufuegen(h1(1, 10 + i))
    assert liste.ist_voll and liste.freier_slot() is None
    with pytest.raises(SerienFehler) as fehler:
        liste.hinzufuegen(h1(1, 99))
    assert str(fehler.value) == TEXT_SERIEN_VOLL and len(liste) == SERIEN_MAX
    # gleiche Auswahl in anderer Messung oder anderer Größe ist keine Dopplung
    liste.entferne(0)
    liste.hinzufuegen(h1(2, 11))
    assert len(liste) == SERIEN_MAX


def test_sichtbarkeit_aendert_nur_das_flag() -> None:
    liste = SerienListe()
    liste.hinzufuegen(h1(1))
    liste.setze_sichtbar(0, False)
    assert not liste.specs[0].sichtbar and liste.specs[0].slot == 0


def test_entfernen_einer_messung_entfernt_ihre_serien_und_zaehlt() -> None:
    liste = SerienListe()
    for mid, label in ((1, 10), (2, 10), (1, 11)):
        liste.hinzufuegen(h1(mid, label))
    assert liste.betroffene(1) == 2 and liste.betroffene(3) == 0  # UI-14: Zahl für die Rückfrage
    assert liste.entferne_messung(1) == 2
    assert [s.messung_id for s in liste.specs] == [2]


def test_baue_spec_prueft_die_angaben() -> None:
    with pytest.raises(SerienFehler, match="Komponente"):
        baue_spec(1, None, "spektrum")
    with pytest.raises(SerienFehler, match="Kanalpaar"):
        baue_spec(1, None, "h2")
    s = baue_spec(1, 11, "spektrum", komponente="Z", teilgroesse="leistung")
    assert s.teilgroesse == "leistung" and s.komponente == "Z" and s.kanalpaar is None


def test_wandle_groesse_zieht_alle_serien_mit() -> None:
    liste = SerienListe()
    liste.hinzufuegen(baue_spec(1, None, "spektrum", komponente="X"))
    liste.hinzufuegen(baue_spec(1, None, "spektrum", komponente="Y"))
    m = Messungen()
    me = messung(m, "a.svd")

    def standard(mid: int, komp: str | None) -> tuple[str, str] | None:
        return standard_paar(me, komp)

    assert liste.wandle_groesse("h1", standard) == 0
    assert [s.kanalpaar for s in liste.specs] == [("Vib X", "Ref1"), ("Vib Y", "Ref1")]
    assert all(s.groesse == "h1" and s.komponente is None for s in liste.specs)
    assert liste.wandle_groesse("spektrum", standard) == 0  # zurück: Komponenten aus den Paaren
    assert [s.komponente for s in liste.specs] == ["X", "Y"]
    liste.wandle_groesse("kohaerenz", standard)
    assert liste.wandle_groesse("phase", standard) == 0
    liste.hinzufuegen(baue_spec(1, None, "spektrum", komponente="X", teilgroesse="leistung"))
    # √AP und |CPH| derselben Komponente werden nach dem Umstellen von √AP auf |CPH| gleich
    liste.wandle_groesse("spektrum", standard)
    assert liste.setze_teilgroesse("kohaerent") == 1
    assert liste.setze_teilgroesse("leistung") == 0
    assert {s.teilgroesse for s in liste.specs} == {"leistung"}


def test_komponente_von_paar() -> None:
    assert komponente_von_paar(("Vib Y", "Ref1")) == "Y"
    assert komponente_von_paar(("Ref2", "Ref1")) == "3D"


def test_standard_paar_bevorzugt_die_komponente_sonst_das_erste_paar() -> None:
    m = Messungen()
    me = messung(m, "a.svd")
    assert standard_paar(me, "Z") == ("Vib Z", "Ref1")
    assert standard_paar(me, "3D") == me.paare[0]
    ohne = messung(m, "b.svd", referenz=False)
    assert standard_paar(ohne, "X") is None


def test_serien_fuer_alle_ordnet_ueber_das_label_zu_und_nennt_den_grund() -> None:
    liste = Messungen()
    a = messung(liste, "a.svd")
    b = messung(liste, "b.svd")
    # Label 10 … 13 gibt es in beiden Messungen: je eine Serie, Kennung der Messung eingesetzt
    serien, gruende = serien_fuer_alle(h1(a.id, 12), liste.bereite())
    assert [s.messung_id for s in serien] == [a.id, b.id] and not gruende
    assert all(s.punkt_label == 12 for s in serien)
    # fehlendes Label (UI-12): keine Serie, Grund mit Kurzname
    serien, gruende = serien_fuer_alle(h1(a.id, 99), liste.bereite())
    assert serien == [] and gruende == ["A: Punkt 99 gibt es nicht.", "B: Punkt 99 gibt es nicht."]
    # Mittel gibt es immer; fehlendes Kanalpaar nennt das Paar
    serien, gruende = serien_fuer_alle(
        baue_spec(a.id, None, "h1", kanalpaar=("Vib X", "Ref9")), liste.bereite()
    )
    assert serien == [] and "Kanalpaar Vib X / Ref9 gibt es nicht" in gruende[0]
    serien, _ = serien_fuer_alle(baue_spec(a.id, None, "spektrum", komponente="Z"), liste.bereite())
    assert len(serien) == 2
    nicht_bereit = liste.hinzufuegen("c.svd")  # lädt noch: ohne Daten, keine Serie
    assert nicht_bereit.geladen is None
    serien, _ = serien_fuer_alle(h1(a.id), liste.alle)
    assert len(serien) == 2


def test_groessen_verfuegbar_mit_und_ohne_referenz() -> None:
    liste = Messungen()
    messung(liste, "a.svd", referenz=False)
    g = groessen_verfuegbar(liste)
    assert g["spektrum"] is None and "Referenz" in str(g["h1"]) and "Referenz" in str(g["phase"])
    messung(liste, "b.svd")  # eine Messung mit Referenz genügt für die Größe
    assert all(v is None for v in groessen_verfuegbar(liste).values())
    assert groessen_verfuegbar(Messungen())["h1"] == ""  # ohne Messung kein Grund, nichts wählbar


def test_zugriff_liefert_nur_bereite_messungen() -> None:
    liste = Messungen()
    a = messung(liste, "C:\\m\\a.svd")
    lade = liste.hinzufuegen("C:\\m\\b.svd")
    zugriff = messungs_zugriff(liste)
    daten, cache, kurz, datei = zugriff(a.id)  # type: ignore[misc]
    assert kurz == "A" and datei == "a.svd" and cache is a.cache and daten is a.geladen.messdaten  # type: ignore[union-attr]
    assert zugriff(lade.id) is None and zugriff(999) is None


def test_paare_je_messung_zaehlt_verschiedene_paare() -> None:
    specs = [
        baue_spec(1, None, "h1", kanalpaar=PAAR),
        baue_spec(1, 10, "h1", kanalpaar=PAAR),  # dasselbe Paar
        baue_spec(1, None, "phase", kanalpaar=("Vib Y", "Ref1")),
        baue_spec(2, None, "spektrum", komponente="3D"),  # |CPH| 3D: drei Paare
        baue_spec(3, None, "spektrum", komponente="Z", teilgroesse="leistung"),  # √AP: keines
    ]
    assert paare_je_messung(specs) == {1: 2, 2: 3, 3: 0}


def test_texte() -> None:
    s = baue_spec(1, 12, "h1", kanalpaar=PAAR)
    assert serie_text(s, "A") == "A · Punkt 12 · Vib X / Ref1"
    assert serie_text(s, "A", mit_groesse=True).endswith(" · |H1|")
    z = baue_spec(1, None, "spektrum", komponente="3D")
    assert serie_text(z, "B") == "B · Mittel · 3D"
    assert serie_text(baue_spec(1, None, "spektrum", komponente="Y"), "B") == "B · Mittel · Vib Y"
    assert unmoeglich_text(s, "A", "Grund", symbol="✖") == (
        "✖ Nicht darstellbar: A · Punkt 12 · Vib X / Ref1: Grund"
    )
    assert kopf_text(["A", "B"], ["h1", "h1"], "nebeneinander") == (
        "Diagramm · Messungen A, B · |H1| · nebeneinander"
    )
    assert kopf_text([], [], "ueberlagert") == "Diagramm · Messungen – · – · überlagert"


# --- S8: Bearbeiten, Übernahme aus Ansicht 1 bis 3, Stempeldateien -------------------------


def test_ersetze_behaelt_slot_und_haekchen_und_lehnt_dopplung_ab() -> None:
    liste = SerienListe()
    for i in range(3):
        liste.hinzufuegen(h1(1, 10 + i))
    liste.setze_sichtbar(1, False)
    neu = liste.ersetze(1, h1(2, 10))
    assert (neu.slot, neu.sichtbar, neu.messung_id) == (1, False, 2)
    assert liste.specs[1] == neu and len(liste) == 3
    with pytest.raises(SerienFehler, match=TEXT_SERIE_DOPPELT):
        liste.ersetze(0, h1(1, 12))  # gleicht der dritten Serie
    assert liste.specs[0].punkt_label == 10  # unverändert
    liste.ersetze(2, h1(1, 12))  # sich selbst ersetzen ist keine Dopplung


def test_ansicht_1_uebernimmt_je_komponente_eine_serie_mit_teilgroesse() -> None:
    u = serien_aus_ansicht(
        1,
        5,
        punkt_label=11,
        komponenten=("X", "3D"),
        teilgroesse="leistung",
        kanalpaar=PAAR,
    )
    assert u.groesse == "spektrum" and u.teilgroesse == "leistung" and u.ansicht == 1
    assert [(s.komponente, s.punkt_label, s.teilgroesse, s.messung_id) for s in u.specs] == [
        ("X", 11, "leistung", 5),
        ("3D", 11, "leistung", 5),
    ]
    with pytest.raises(SerienFehler, match="Komponente"):
        serien_aus_ansicht(
            1, 5, punkt_label=None, komponenten=(), teilgroesse="kohaerent", kanalpaar=PAAR
        )


def test_ansicht_2_uebernimmt_h1_oder_nur_h2_mit_dem_punkt() -> None:
    u = serien_aus_ansicht(
        2, 5, punkt_label=12, komponenten=("X",), teilgroesse="kohaerent", kanalpaar=PAAR
    )
    assert [(s.groesse, s.kanalpaar, s.punkt_label) for s in u.specs] == [("h1", PAAR, 12)]
    nur_h2 = serien_aus_ansicht(
        2,
        5,
        punkt_label=None,
        komponenten=("X",),
        teilgroesse="kohaerent",
        kanalpaar=PAAR,
        h1=False,
        h2=True,
    )
    assert nur_h2.groesse == "h2" and nur_h2.specs[0].punkt_label is None
    beide = serien_aus_ansicht(
        2,
        5,
        punkt_label=None,
        komponenten=("X",),
        teilgroesse="kohaerent",
        kanalpaar=PAAR,
        h1=True,
        h2=True,
    )
    assert beide.groesse == "h1"  # beide gewählt: |H1|
    with pytest.raises(SerienFehler, match="Referenz"):
        serien_aus_ansicht(
            2, 5, punkt_label=None, komponenten=("X",), teilgroesse="kohaerent", kanalpaar=None
        )


def test_ansicht_3_uebernimmt_das_betragsmittel_oder_ohne_referenz_das_leistungsmittel() -> None:
    mit = serien_aus_ansicht(
        3, 5, punkt_label=12, komponenten=("X",), teilgroesse="kohaerent", kanalpaar=PAAR
    )
    assert [(s.groesse, s.punkt_label, s.kanalpaar) for s in mit.specs] == [("h1", None, PAAR)]
    ohne = serien_aus_ansicht(
        3,
        5,
        punkt_label=None,
        komponenten=("X",),
        teilgroesse="kohaerent",
        kanalpaar=None,
        kanal="Vib Z",
    )
    assert ohne.groesse == "spektrum" and ohne.teilgroesse == "leistung"
    assert (ohne.specs[0].komponente, ohne.specs[0].teilgroesse) == ("Z", "leistung")
    with pytest.raises(SerienFehler, match="Vib-Kanal"):
        serien_aus_ansicht(
            3,
            5,
            punkt_label=None,
            komponenten=("X",),
            teilgroesse="kohaerent",
            kanalpaar=None,
            kanal="Ref1",
        )
    with pytest.raises(SerienFehler, match="Ansicht 4"):
        serien_aus_ansicht(
            4, 5, punkt_label=None, komponenten=("X",), teilgroesse="kohaerent", kanalpaar=PAAR
        )


def test_uebernahme_legt_an_zaehlt_dopplungen_und_rest() -> None:
    u = serien_aus_ansicht(
        1, 1, punkt_label=10, komponenten=("X", "Y", "Z", "3D"), teilgroesse="kohaerent",
        kanalpaar=PAAR,
    )  # fmt: skip
    liste = SerienListe()
    liste.hinzufuegen(baue_spec(1, 10, "spektrum", komponente="Y"))
    liste.hinzufuegen(h1(1, 10))
    erg = uebernimm(
        liste, u, diagramm_groesse="spektrum", diagramm_teilgroesse="kohaerent", nebeneinander=False
    )
    # Y gab es schon; X und Z passen; 3D kommt nicht mehr hinein (vier Serien)
    assert (erg.angelegt, erg.vorhanden, erg.rest) == (2, 1, 1) and not erg.vollstaendig
    assert len(liste) == SERIEN_MAX
    assert erg.text(1) == (
        "2 Serien aus Ansicht 1 übernommen; 1 gab es schon; 1 passte nicht (höchstens 4 Serien)."
    )
    leer = SerienListe()
    ein = uebernimm(
        leer,
        serien_aus_ansicht(
            2, 1, punkt_label=None, komponenten=("X",), teilgroesse="kohaerent", kanalpaar=PAAR
        ),
        diagramm_groesse="spektrum",  # bei leerer Liste ohne Bedeutung
        diagramm_teilgroesse="kohaerent",
        nebeneinander=False,
    )
    assert ein.text(2) == "1 Serie aus Ansicht 2 übernommen." and ein.vollstaendig


def test_uebernahme_wechselt_weder_groesse_noch_teilgroesse_still() -> None:
    liste = SerienListe()
    liste.hinzufuegen(h1(1, 10))
    spektrum = serien_aus_ansicht(
        1, 1, punkt_label=None, komponenten=("X",), teilgroesse="kohaerent", kanalpaar=PAAR
    )
    with pytest.raises(SerienFehler, match="Ansicht 1 zeigt Spektrum"):
        uebernimm(
            liste,
            spektrum,
            diagramm_groesse="h1",
            diagramm_teilgroesse="kohaerent",
            nebeneinander=False,
        )
    assert len(liste) == 1  # unverändert
    # nebeneinander darf die Größe wechseln (je Serie eine Größe) ...
    erg = uebernimm(
        liste,
        spektrum,
        diagramm_groesse="h1",
        diagramm_teilgroesse="kohaerent",
        nebeneinander=True,
    )
    assert erg.angelegt == 1
    # ... aber die Teilgröße des Spektrums gilt für alle Serien
    leistung = serien_aus_ansicht(
        1, 1, punkt_label=None, komponenten=("Z",), teilgroesse="leistung", kanalpaar=PAAR
    )
    with pytest.raises(SerienFehler, match=re.escape("Spektrum als √AP, das Diagramm als |CPH|")):
        uebernimm(
            liste,
            leistung,
            diagramm_groesse="h1",
            diagramm_teilgroesse="kohaerent",
            nebeneinander=True,
        )
    assert len(liste) == 2


def test_teilgroesse_wird_nur_bei_spektren_in_der_liste_geprueft() -> None:
    """Liste nur mit |H1|: ein √AP-Spektrum bei |CPH| am Diagramm wird übernommen (Annahme 6).

    Sobald ein Spektrum in der Liste steht, gilt die Teilgröße des Diagramms wieder.
    """
    liste = SerienListe()
    liste.hinzufuegen(h1(1, 10))
    leistung = serien_aus_ansicht(
        1, 1, punkt_label=None, komponenten=("X",), teilgroesse="leistung", kanalpaar=PAAR
    )
    erg = uebernimm(
        liste,
        leistung,
        diagramm_groesse="h1",
        diagramm_teilgroesse="kohaerent",
        nebeneinander=True,
    )
    assert (erg.angelegt, erg.rest) == (1, 0) and erg.vollstaendig
    assert [(s.groesse, s.teilgroesse) for s in liste.specs] == [
        ("h1", "kohaerent"),
        ("spektrum", "leistung"),
    ]
    kohaerent = serien_aus_ansicht(
        1, 1, punkt_label=None, komponenten=("Y",), teilgroesse="kohaerent", kanalpaar=PAAR
    )
    with pytest.raises(SerienFehler, match=re.escape("Spektrum als |CPH|, das Diagramm als √AP")):
        uebernimm(
            liste,
            kohaerent,
            diagramm_groesse="h1",
            diagramm_teilgroesse="leistung",
            nebeneinander=True,
        )
    assert len(liste) == 2


def test_stempel_dateien_nur_sichtbare_je_messung_einmal_in_serienfolge() -> None:
    class Attrappe:
        def __init__(self, kurz: str, name: str, sichtbar: bool) -> None:
            self.kurzname, self.dateiname, self.sichtbar = kurz, name, sichtbar

    serien = [
        Attrappe("B", "b.svd", True),
        Attrappe("A", "a.svd", True),
        Attrappe("B", "b.svd", True),
        Attrappe("C", "c.svd", False),
    ]
    erg = stempel_dateien(serien)  # type: ignore[arg-type]
    assert erg == (("B", "b.svd"), ("A", "a.svd"))
