"""Messungsverwaltung (R-058, P-AUSW2 S4/S5; UI-9, UI-14): Qt-frei, Standardlauf."""

from __future__ import annotations

import pytest
from gui_ausw_hilfen import synth_geladen

from ldv_automation.darstellung.auswahl import PaarCache
from ldv_automation.gui.messungen import (
    KURZNAME_MAX,
    MESSUNGEN_MAX,
    TEXT_KURZNAME_DOPPELT,
    TEXT_KURZNAME_LANG,
    TEXT_KURZNAME_LEER,
    TEXT_KURZNAME_UMBRUCH,
    Messung,
    Messungen,
    MessungsZustand,
    kurzname_vorschlag,
    nbytes_von,
    pruefe_kurzname,
)


def bereit(liste: Messungen, pfad: str = "C:\\m\\a.svd", **kw: object) -> Messung:
    """Legt eine Messung an und macht sie bereit."""
    m = liste.hinzufuegen(pfad)
    geladen = synth_geladen(pfad=pfad, **kw)  # type: ignore[arg-type]
    liste.fertig(
        m.id,
        geladen=geladen,
        cache=PaarCache(geladen.messdaten),
        antrieb=None,
        paare=tuple(geladen.messdaten.cp),
    )
    return m


def test_kurznamen_folgen_a_bis_z_dann_aa() -> None:
    belegt: list[str] = []
    for _ in range(28):
        belegt.append(kurzname_vorschlag(belegt))
    assert belegt[:3] == ["A", "B", "C"] and belegt[25] == "Z"
    assert belegt[26:] == ["AA", "AB"]


def test_kurzname_vorschlag_nimmt_erste_freie_luecke_ohne_gross_klein() -> None:
    assert kurzname_vorschlag(["A", "c"]) == "B"
    assert kurzname_vorschlag(["a", "B"]) == "C"


@pytest.mark.parametrize(
    ("text", "erwartet"),
    [
        ("", TEXT_KURZNAME_LEER),
        ("   ", TEXT_KURZNAME_LEER),
        ("x" * (KURZNAME_MAX + 1), TEXT_KURZNAME_LANG),
        ("a\nb", TEXT_KURZNAME_UMBRUCH),
        ("b", TEXT_KURZNAME_DOPPELT),  # ohne Beachtung der Schreibweise
        ("Probe 1", None),
        ("x" * KURZNAME_MAX, None),
    ],
)
def test_pruefe_kurzname(text: str, erwartet: str | None) -> None:
    assert pruefe_kurzname(text, ["A", "B"]) == erwartet


def test_erste_messung_wird_aktiv_zweite_erst_nach_dem_laden() -> None:
    liste = Messungen()
    a = bereit(liste)
    assert a.kurzname == "A" and a.zustand is MessungsZustand.BEREIT and liste.aktive is a
    b = liste.hinzufuegen("C:\\m\\b.svd")
    assert b.kurzname == "B" and b.zustand is MessungsZustand.LADEN
    assert liste.aktive is a
    with pytest.raises(ValueError, match="noch nicht bereit"):
        liste.setze_aktiv(b.id)
    assert liste.bereite() == (a,)


def test_grenze_und_ids_werden_nie_wiederverwendet() -> None:
    liste = Messungen()
    ms = [bereit(liste) for _ in range(MESSUNGEN_MAX)]
    assert liste.ist_voll
    with pytest.raises(ValueError, match="Höchstens"):
        liste.hinzufuegen("x.svd")
    liste.entferne(ms[1].id)
    assert not liste.ist_voll
    neu = liste.hinzufuegen("y.svd")
    assert neu.id not in {m.id for m in ms}
    assert neu.kurzname == "B"  # die freie Lücke


def test_ersetzen_behaelt_kurzname_und_position_gibt_neue_id() -> None:
    liste = Messungen()
    a = bereit(liste)
    b = bereit(liste, "C:\\m\\b.svd")
    liste.umbenennen(a.id, "Referenz")
    geladen = synth_geladen(pfad="C:\\m\\neu.svd")
    neu = liste.ersetze(
        a.id,
        "C:\\m\\neu.svd",
        geladen=geladen,
        cache=PaarCache(geladen.messdaten),
        antrieb=None,
        paare=(),
    )
    assert neu.id != a.id and neu.kurzname == "Referenz" and neu.dateiname == "neu.svd"
    assert liste.alle == (neu, b) and liste.aktive is neu
    assert liste.finde(a.id) is None


def test_entfernen_der_aktiven_rueckt_auf_die_vorige() -> None:
    liste = Messungen()
    a, b, c = (bereit(liste) for _ in range(3))
    liste.setze_aktiv(b.id)
    assert liste.entferne(b.id) is b
    assert liste.aktive is a
    liste.setze_aktiv(c.id)
    liste.entferne(a.id)  # nicht die aktive: aktiv bleibt
    assert liste.aktive is c
    liste.entferne(c.id)
    assert liste.aktive is None and len(liste) == 0
    assert liste.entferne(999) is None


def test_entfernen_der_ersten_aktiven_rueckt_auf_die_naechste_bereite() -> None:
    liste = Messungen()
    a = bereit(liste)
    lade = liste.hinzufuegen("l.svd")  # noch nicht bereit: wird nie aktiv
    b = bereit(liste)
    liste.entferne(a.id)
    assert liste.aktive is b and lade.zustand is MessungsZustand.LADEN


def test_umbenennen_prueft_eindeutigkeit_ohne_sich_selbst() -> None:
    liste = Messungen()
    a, b = bereit(liste), bereit(liste)
    assert liste.umbenennen(b.id, "A") == TEXT_KURZNAME_DOPPELT and b.kurzname == "B"
    assert liste.umbenennen(a.id, " a ") is None and a.kurzname == "a"  # eigener Name erlaubt
    assert liste.umbenennen(b.id, "") == TEXT_KURZNAME_LEER


def test_ladewarteschlange_hoechstens_ein_auftrag_gleichzeitig() -> None:
    liste = Messungen()
    bereit(liste)
    b = liste.hinzufuegen("b.svd")
    c = liste.hinzufuegen("c.svd")
    assert liste.naechster_ladeauftrag() is b
    b.gestartet = True
    assert liste.naechster_ladeauftrag() is None  # b läuft: c wartet
    geladen = synth_geladen(pfad="b.svd")
    liste.fertig(b.id, geladen=geladen, cache=PaarCache(geladen.messdaten), antrieb=None, paare=())
    assert liste.naechster_ladeauftrag() is c


def test_speicher_zaehlt_daten_und_paare_einmal() -> None:
    liste = Messungen()
    m = bereit(liste)
    ohne = liste.speicher_mib(m.id)
    assert m.geladen is not None and m.cache is not None
    daten_bytes = nbytes_von(m.geladen.messdaten)
    assert daten_bytes > 0 and ohne == pytest.approx(daten_bytes / 2**20, rel=1e-12)
    m.cache.paar("Vib X", "Ref1")
    mit = liste.speicher_mib(m.id)
    assert mit > ohne  # das Kanalpaar kommt dazu


def test_nbytes_von_zaehlt_mehrfach_verwendetes_feld_einmal() -> None:
    import numpy as np

    feld = np.zeros(100, dtype=np.float64)
    assert nbytes_von({"a": feld, "b": [feld, (feld,)]}) == 800
    assert nbytes_von("text") == 0


def test_leere_vergisst_alles_aber_ids_laufen_weiter() -> None:
    liste = Messungen()
    a = bereit(liste)
    liste.leere()
    assert len(liste) == 0 and liste.aktive is None
    assert bereit(liste).id > a.id


def test_unbekannte_messung_wirft() -> None:
    liste = Messungen()
    with pytest.raises(ValueError, match="gibt es nicht"):
        liste.setze_aktiv(5)
    with pytest.raises(ValueError, match="gibt es nicht"):
        liste.speicher_mib(5)


def test_paarcache_groesse_aendern_verwirft_aelteste() -> None:
    geladen = synth_geladen()
    cache = PaarCache(geladen.messdaten, groesse=3)
    for kanal in ("Vib X", "Vib Y", "Vib Z"):
        cache.paar(kanal, "Ref1")
    assert len(cache.alle_paare()) == 3 and cache.groesse == 3
    cache.setze_groesse(2)
    assert cache.gespeichert() == (("Vib Y", "Ref1"), ("Vib Z", "Ref1"))
    with pytest.raises(ValueError, match="groesse"):
        cache.setze_groesse(0)
