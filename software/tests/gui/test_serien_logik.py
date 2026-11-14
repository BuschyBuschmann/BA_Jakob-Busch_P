"""Serienverwaltung von Ansicht 5 (R-058/R-059, P-AUSW2 S7; UI-12, UI-14, UI-18, UI-20): ohne Qt."""

from __future__ import annotations

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
    serien_fuer_alle,
    standard_paar,
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
