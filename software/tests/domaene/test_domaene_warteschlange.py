"""Tests der Warteschlange (U1-1, U1-2, U1-3)."""

import threading
from uuid import UUID, uuid4

import pytest

from ldv_automation.domaene import (
    Eintrag,
    Messung,
    MessungZustand,
    Pausenpunkt,
    PausenpunktZustand,
    Warteschlange,
)


def _m(name: str) -> Messung:
    return Messung(name=name, einstellungsdatei=f"{name}.set")


def _namen(q: Warteschlange) -> list[str]:
    return [e.name if isinstance(e, Messung) else e.text for e in q.eintraege()]


@pytest.fixture
def q() -> Warteschlange:
    return Warteschlange([_m("A"), _m("B"), _m("C")])


# --- U1-1 -----------------------------------------------------------------------------------


@pytest.mark.parametrize("pos", [0, 1, 2, 3])
def test_u1_1_einfuegen_setzt_an_index(q: Warteschlange, pos: int) -> None:
    neu = _m("X")
    q.einfuegen(pos, neu)
    assert q.eintraege()[pos] is neu
    assert len(q) == 4
    erwartet = ["A", "B", "C"]
    erwartet.insert(pos, "X")
    assert _namen(q) == erwartet


@pytest.mark.parametrize("pos", [-1, 4, 100])
def test_u1_1_einfuegen_ausserhalb_wirft_indexerror(q: Warteschlange, pos: int) -> None:
    vorher = q.eintraege()
    with pytest.raises(IndexError):
        q.einfuegen(pos, _m("X"))
    assert q.eintraege() == vorher


def test_einfuegen_in_leere_schlange_und_pausenpunkt() -> None:
    q = Warteschlange()
    q.einfuegen(0, Pausenpunkt(text="P"))
    assert _namen(q) == ["P"]


def test_einfuegen_lehnt_doppelte_id_und_nicht_wartende_ab(q: Warteschlange) -> None:
    vorhanden = q.eintraege()[0]
    with pytest.raises(ValueError, match="bereits vorhanden"):
        q.einfuegen(0, vorhanden)
    laeuft = _m("L").mit_zustand(MessungZustand.LAEUFT)
    with pytest.raises(ValueError, match="WARTEND"):
        q.einfuegen(0, laeuft)
    assert len(q) == 3


def test_konstruktor_lehnt_doppelte_ids_ab() -> None:
    m = _m("A")
    with pytest.raises(ValueError, match="Doppelte"):
        Warteschlange([m, m])


# --- U1-2 -----------------------------------------------------------------------------------

NICHT_WARTEND = [
    MessungZustand.LAEUFT,
    MessungZustand.FERTIG,
    MessungZustand.FEHLER,
    MessungZustand.ABGEBROCHEN,
]


def _mit_zustand(zustand: MessungZustand) -> tuple[Warteschlange, UUID]:
    """Schlange A, Ziel, C mit Ziel im gewünschten Zustand (über erlaubte Übergänge)."""
    ziel = _m("Z")
    q = Warteschlange([_m("A"), ziel, _m("C")])
    # Z muss als erstes wartendes beansprucht werden: A zuerst abschließen
    a = q.eintraege()[0]
    q.naechsten_beanspruchen()  # A -> LAEUFT
    q.zustand_setzen(a.id, MessungZustand.FERTIG)
    q.naechsten_beanspruchen()  # Z -> LAEUFT
    if zustand is not MessungZustand.LAEUFT:
        q.zustand_setzen(ziel.id, zustand)
    return q, ziel.id


@pytest.mark.parametrize("zustand", NICHT_WARTEND)
def test_u1_2_entfernen_bearbeiten_verschieben_nur_wartend(zustand: MessungZustand) -> None:
    q, zid = _mit_zustand(zustand)
    vorher = q.eintraege()
    with pytest.raises(ValueError, match="WARTEND"):
        q.entfernen(zid)
    with pytest.raises(ValueError, match="WARTEND"):
        q.bearbeiten(zid, name="neu")
    with pytest.raises(ValueError, match="WARTEND"):
        q.verschieben(zid, 0)
    assert q.eintraege() == vorher


def test_u1_2_pausenpunkt_erreicht_ist_unveraenderlich() -> None:
    p = Pausenpunkt(text="P")
    q = Warteschlange([p])
    q.naechsten_beanspruchen()
    assert q.hole(p.id).zustand is PausenpunktZustand.ERREICHT
    for aktion in (
        lambda: q.entfernen(p.id),
        lambda: q.bearbeiten(p.id, text="x"),
        lambda: q.verschieben(p.id, 0),
    ):
        with pytest.raises(ValueError, match="WARTEND"):
            aktion()


# --- Entfernen / Bearbeiten / Verschieben im Normalfall ------------------------------------------


def test_entfernen(q: Warteschlange) -> None:
    b = q.eintraege()[1]
    assert q.entfernen(b.id) is b
    assert _namen(q) == ["A", "C"]
    with pytest.raises(KeyError):
        q.entfernen(b.id)


def test_bearbeiten_messung(q: Warteschlange) -> None:
    a = q.eintraege()[0]
    neu = q.bearbeiten(
        a.id, name="A2", parameter={"mittelung.anzahl": 5}, zeitlimit_s=30, notiz="n"
    )
    assert isinstance(neu, Messung)
    assert (neu.name, neu.zeitlimit_s, neu.notiz) == ("A2", 30, "n")
    assert neu.id == a.id
    assert q.eintraege()[0] is neu  # gleiche Position
    assert neu.parameter["mittelung.anzahl"] == 5


def test_bearbeiten_pausenpunkt() -> None:
    p = Pausenpunkt(text="alt")
    q = Warteschlange([p])
    q.bearbeiten(p.id, text="neu")
    assert _namen(q) == ["neu"]


def test_u1_3_bearbeiten_mit_ungueltigem_parameter_laesst_schlange_unveraendert(
    q: Warteschlange,
) -> None:
    vorher = q.eintraege()
    with pytest.raises(ValueError, match=r"mittelung\.anzahl.*3 … 10000"):
        q.bearbeiten(vorher[0].id, parameter={"mittelung.anzahl": 2})
    assert q.eintraege() == vorher


def test_bearbeiten_unzulaessige_felder(q: Warteschlange) -> None:
    a = q.eintraege()[0]
    for feld, teil in (
        ("id", "nicht änderbar"),
        ("zustand", "nicht änderbar"),
        ("foo", "unbekannt"),
    ):
        with pytest.raises(ValueError, match=teil):
            q.bearbeiten(a.id, **{feld: 1})
    p = Pausenpunkt(text="p")
    q.einfuegen(0, p)
    with pytest.raises(ValueError, match="änderbar: text"):
        q.bearbeiten(p.id, name="x")


def test_verschieben(q: Warteschlange) -> None:
    c = q.eintraege()[2]
    q.verschieben(c.id, 0)
    assert _namen(q) == ["C", "A", "B"]
    q.verschieben(c.id, 2)
    assert _namen(q) == ["A", "B", "C"]
    q.verschieben(c.id, 2)  # auf eigene Position: erlaubt, ohne Wirkung
    assert _namen(q) == ["A", "B", "C"]
    vorher = q.eintraege()
    for pos in (-1, 3):
        with pytest.raises(IndexError):
            q.verschieben(c.id, pos)
    assert q.eintraege() == vorher


def test_unbekannte_id() -> None:
    q = Warteschlange()
    unbekannt = uuid4()
    for aktion in (
        lambda: q.hole(unbekannt),
        lambda: q.index_von(unbekannt),
        lambda: q.bearbeiten(unbekannt, name="x"),
        lambda: q.verschieben(unbekannt, 0),
        lambda: q.zustand_setzen(unbekannt, MessungZustand.LAEUFT),
    ):
        with pytest.raises(KeyError):
            aktion()


# --- Beanspruchen ----------------------------------------------------------------------------


def test_naechsten_beanspruchen_reihenfolge_und_pausenpunkt() -> None:
    a, p, b = _m("A"), Pausenpunkt(text="P"), _m("B")
    q = Warteschlange([a, p, b])
    e1 = q.naechsten_beanspruchen()
    assert isinstance(e1, Messung) and e1.id == a.id and e1.zustand is MessungZustand.LAEUFT
    q.zustand_setzen(a.id, MessungZustand.FERTIG)
    e2 = q.naechsten_beanspruchen()
    assert isinstance(e2, Pausenpunkt) and e2.zustand is PausenpunktZustand.ERREICHT
    q.zustand_setzen(p.id, PausenpunktZustand.ERLEDIGT)
    e3 = q.naechsten_beanspruchen()
    assert isinstance(e3, Messung) and e3.id == b.id
    q.zustand_setzen(b.id, MessungZustand.ABGEBROCHEN)
    assert q.naechsten_beanspruchen() is None


def test_leere_schlange_beansprucht_nichts() -> None:
    assert Warteschlange().naechsten_beanspruchen() is None


def test_aenderung_vor_beanspruchen_wirkt_danach_nicht_mehr() -> None:
    a, b = _m("A"), _m("B")
    q = Warteschlange([a, b])
    q.bearbeiten(a.id, name="A-neu")
    beansprucht = q.naechsten_beanspruchen()
    assert isinstance(beansprucht, Messung) and beansprucht.name == "A-neu"
    with pytest.raises(ValueError, match="WARTEND"):
        q.bearbeiten(a.id, name="zu spaet")
    # Einfügen vor dem nächsten wartenden wirkt im selben Durchgang
    q.einfuegen(2, _m("N"))
    q.zustand_setzen(a.id, MessungZustand.FERTIG)
    assert [e.name for e in _beanspruche_alle(q)] == ["B", "N"]


def _beanspruche_alle(q: Warteschlange) -> list[Messung]:
    ergebnis: list[Messung] = []
    while (e := q.naechsten_beanspruchen()) is not None:
        assert isinstance(e, Messung)
        ergebnis.append(e)
        q.zustand_setzen(e.id, MessungZustand.FERTIG)
    return ergebnis


def test_wiederholen_behaelt_position_und_erhoeht_versuch() -> None:
    a, b = _m("A"), _m("B")
    q = Warteschlange([a, b])
    q.naechsten_beanspruchen()
    q.zustand_setzen(a.id, MessungZustand.FEHLER)
    neu = q.zustand_setzen(a.id, MessungZustand.WARTEND)
    assert isinstance(neu, Messung) and neu.versuch == 2
    assert q.index_von(a.id) == 0
    erneut = q.naechsten_beanspruchen()
    assert isinstance(erneut, Messung) and erneut.id == a.id and erneut.versuch == 2


def test_zustand_setzen_prueft_art_und_uebergang(q: Warteschlange) -> None:
    a = q.eintraege()[0]
    with pytest.raises(ValueError, match="passt nicht"):
        q.zustand_setzen(a.id, PausenpunktZustand.ERREICHT)
    with pytest.raises(ValueError, match="nicht erlaubt"):
        q.zustand_setzen(a.id, MessungZustand.FERTIG)
    p = Pausenpunkt(text="p")
    q.einfuegen(0, p)
    with pytest.raises(ValueError, match="passt nicht"):
        q.zustand_setzen(p.id, MessungZustand.LAEUFT)
    assert q.hole(a.id).zustand is MessungZustand.WARTEND


def test_eintraege_ist_momentaufnahme(q: Warteschlange) -> None:
    schnappschuss: tuple[Eintrag, ...] = q.eintraege()
    q.entfernen(schnappschuss[0].id)
    assert len(schnappschuss) == 3
    assert len(q) == 2


# --- Nebenläufigkeit (Sperre) --------------------------------------------------------------------


def test_beanspruchen_aus_mehreren_threads_vergibt_jeden_eintrag_genau_einmal() -> None:
    n = 200
    q = Warteschlange(_m(f"M{i}") for i in range(n))
    erhalten: list[list[UUID]] = [[] for _ in range(8)]

    def arbeite(liste: list[UUID]) -> None:
        while (e := q.naechsten_beanspruchen()) is not None:
            liste.append(e.id)

    threads = [threading.Thread(target=arbeite, args=(liste,)) for liste in erhalten]
    for t in threads:
        t.start()
    for t in threads:
        t.join(timeout=10)
        assert not t.is_alive()
    alle = [i for liste in erhalten for i in liste]
    assert len(alle) == n
    assert len(set(alle)) == n


# --- Review-Korrekturen (MINOR-1, MINOR-2) -------------------------------------------------


def test_minor2_wartend_zu_laeuft_oder_erreicht_nur_ueber_beanspruchen(q: Warteschlange) -> None:
    a = q.eintraege()[0]
    with pytest.raises(ValueError, match="naechsten_beanspruchen"):
        q.zustand_setzen(a.id, MessungZustand.LAEUFT)
    p = Pausenpunkt(text="p")
    q.einfuegen(0, p)
    with pytest.raises(ValueError, match="naechsten_beanspruchen"):
        q.zustand_setzen(p.id, PausenpunktZustand.ERREICHT)
    assert q.hole(a.id).zustand is MessungZustand.WARTEND
    assert q.hole(p.id).zustand is PausenpunktZustand.WARTEND


@pytest.mark.parametrize(
    "aenderung",
    [
        {"name": None},
        {"name": 5},
        {"einstellungsdatei": None},
        {"parameter": None},
        {"parameter": [("fft.linien", 400)]},
        {"parameter": {1: 2}},
        {"parameter": {"fft.linien": None}},
        {"parameter": {"fft.bandbreite_hz": 10**400}},
        {"parameter": {"mittelung.anzahl": 10**400}},
        {"zeitlimit_s": "x"},
        {"zeitlimit_s": 10**400},
        {"zeitlimit_s": True},
        {"notiz": None},
    ],
)
def test_minor1_bearbeiten_mit_ungueltigem_typ_wirft_valueerror(
    q: Warteschlange, aenderung: dict[str, object]
) -> None:
    vorher = q.eintraege()
    with pytest.raises(ValueError, match=r"\S"):
        q.bearbeiten(vorher[0].id, **aenderung)
    assert q.eintraege() == vorher


def test_minor1_bearbeiten_pausenpunkt_text_none() -> None:
    p = Pausenpunkt(text="p")
    q = Warteschlange([p])
    with pytest.raises(ValueError, match="Text"):
        q.bearbeiten(p.id, text=None)
    assert q.eintraege() == (p,)


@pytest.mark.parametrize("pos", [True, False, 1.0, None, "1"])
def test_minor1_position_muss_echte_ganzzahl_sein(q: Warteschlange, pos: object) -> None:
    vorher = q.eintraege()
    with pytest.raises(ValueError, match="Ganzzahl"):
        q.einfuegen(pos, _m("X"))  # type: ignore[arg-type]
    with pytest.raises(ValueError, match="Ganzzahl"):
        q.verschieben(vorher[0].id, pos)  # type: ignore[arg-type]
    assert q.eintraege() == vorher


def test_minor1_einfuegen_lehnt_fremde_objekte_ab(q: Warteschlange) -> None:
    with pytest.raises(ValueError, match="Messung oder Pausenpunkt"):
        q.einfuegen(0, "x")  # type: ignore[arg-type]
    assert len(q) == 3
