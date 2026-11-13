"""Prüflogik des Abgleichs vor der Messung (R-003b, Plan P-R003, Schritt 4).

Handrechenbare Tabellen. Alle Zahlen sind Testwerte, keine Gerätewerte oder Empfehlungen.
Vergleiche sind exakt (``<=``): Die Grenze ist eine Vorgabe, keine Messgröße, es gibt keine
Rundung und keine Toleranz.
"""

from __future__ import annotations

import math
from typing import Any

import pytest

from ldv_automation.ablauf.abgleich import (
    AbgleichModus,
    AbgleichRegel,
    PruefErgebnis,
    abgleich_hinweise,
    pruefe_abgleich,
    pruefung_nicht_ausgefuehrt_zu_dict,
    pruefung_zu_dict,
)
from ldv_automation.geraet.schnittstelle import Abgleich2D, Abgleich3D, AbgleichStand

V = AbgleichModus.VERWEIGERN


def _a3(index: int = 0, /, **kw: Any) -> Abgleich3D:
    basis: dict[str, Any] = {
        "gueltig": True,
        "qualitaet_ist_m": 2.0,
        "qualitaet_soll_m": 4.0,
        "positionsunsicherheit_m": 0.5,
        "winkelunsicherheit_rad": 0.25,
    }
    basis.update(kw)
    return Abgleich3D(index=index, **basis)


def _stand(*a3: Abgleich3D, a2: tuple[Abgleich2D, ...] = (), **kw: object) -> AbgleichStand:
    return AbgleichStand(
        abgleich_3d=a3,
        abgleich_2d=a2,
        anzahl_3d=kw.pop("anzahl_3d", len(a3)),  # type: ignore[arg-type]
        anzahl_2d=kw.pop("anzahl_2d", len(a2)),  # type: ignore[arg-type]
        **kw,  # type: ignore[arg-type]
    )


def _regel(**kw: object) -> AbgleichRegel:
    return AbgleichRegel(modus=kw.pop("modus", V), **kw)  # type: ignore[arg-type]


def test_modus_aus_ist_nicht_geprueft_auch_bei_schlechtem_abgleich() -> None:
    schlecht = _stand(_a3(gueltig=False))
    p = pruefe_abgleich(schlecht, None, AbgleichRegel())
    assert p.ergebnis is PruefErgebnis.NICHT_GEPRUEFT and p.befunde == ()
    assert pruefe_abgleich(None, "x", AbgleichRegel()).ergebnis is PruefErgebnis.NICHT_GEPRUEFT


def test_gueltig_ohne_grenzen_besteht() -> None:
    p = pruefe_abgleich(_stand(_a3()), None, _regel())
    assert p.ergebnis is PruefErgebnis.BESTANDEN and p.befunde == ()


def test_ohne_gesetzte_grenze_zaehlt_nur_valid_auch_bei_fehlendem_wert() -> None:
    stand = _stand(_a3(qualitaet_ist_m=None, positionsunsicherheit_m=None))
    assert pruefe_abgleich(stand, None, _regel()).ergebnis is PruefErgebnis.BESTANDEN


@pytest.mark.parametrize("gueltig", [False])
def test_ungueltig_ist_nicht_bestanden(gueltig: bool) -> None:
    p = pruefe_abgleich(_stand(_a3(gueltig=gueltig)), None, _regel())
    assert p.ergebnis is PruefErgebnis.NICHT_BESTANDEN
    assert p.befunde == ("3D-Abgleich 0: ungültig (Valid = False)",)


def test_gueltigkeit_unbekannt_ist_nicht_pruefbar() -> None:
    p = pruefe_abgleich(_stand(_a3(gueltig=None)), None, _regel())
    assert p.ergebnis is PruefErgebnis.NICHT_PRUEFBAR


# Wert == Grenze besteht, nextafter(Grenze, inf) nicht: je Größe.
@pytest.mark.parametrize(
    ("feld", "regelname", "wert"),
    [
        ("qualitaet_ist_m", "qualitaet_max_m", 2.0),
        ("positionsunsicherheit_m", "position_max_m", 0.5),
        ("winkelunsicherheit_rad", "winkel_max_rad", 0.25),
    ],
)
def test_grenzfall_wert_gleich_grenze_besteht_naechste_zahl_nicht(
    feld: str, regelname: str, wert: float
) -> None:
    regel = _regel(**{regelname: wert})
    assert pruefe_abgleich(_stand(_a3(**{feld: wert})), None, regel).ergebnis is (
        PruefErgebnis.BESTANDEN
    )
    ueber = math.nextafter(wert, math.inf)
    p = pruefe_abgleich(_stand(_a3(**{feld: ueber})), None, regel)
    assert p.ergebnis is PruefErgebnis.NICHT_BESTANDEN
    assert "über Grenze" in p.befunde[0]


@pytest.mark.parametrize(
    ("feld", "regelname"),
    [
        ("qualitaet_ist_m", "qualitaet_max_m"),
        ("positionsunsicherheit_m", "position_max_m"),
        ("winkelunsicherheit_rad", "winkel_max_rad"),
    ],
)
def test_fehlender_wert_bei_gesetzter_grenze_ist_nicht_pruefbar(feld: str, regelname: str) -> None:
    p = pruefe_abgleich(_stand(_a3(**{feld: None})), None, _regel(**{regelname: 1.0}))
    assert p.ergebnis is PruefErgebnis.NICHT_PRUEFBAR
    assert "Wert nicht lesbar" in p.befunde[0]


@pytest.mark.parametrize("wert", [math.nan, math.inf, -math.inf])
@pytest.mark.parametrize(
    ("feld", "regelname"),
    [
        ("qualitaet_ist_m", "qualitaet_max_m"),
        ("positionsunsicherheit_m", "position_max_m"),
        ("winkelunsicherheit_rad", "winkel_max_rad"),
    ],
)
def test_nicht_endlicher_wert_bei_gesetzter_grenze_ist_nicht_pruefbar(
    feld: str, regelname: str, wert: float
) -> None:
    p = pruefe_abgleich(_stand(_a3(**{feld: wert})), None, _regel(**{regelname: 1.0}))
    assert p.ergebnis is PruefErgebnis.NICHT_PRUEFBAR
    assert "nicht endlich" in p.befunde[0]


def test_nicht_endlicher_wert_ohne_grenze_wird_nicht_beanstandet() -> None:
    stand = _stand(_a3(qualitaet_ist_m=math.nan))
    assert pruefe_abgleich(stand, None, _regel()).ergebnis is PruefErgebnis.BESTANDEN


def test_weniger_gelesen_als_count_ist_nicht_pruefbar() -> None:
    stand = _stand(_a3(), anzahl_3d=20)
    p = pruefe_abgleich(stand, None, _regel())
    assert p.ergebnis is PruefErgebnis.NICHT_PRUEFBAR
    assert "nur 1 von 20" in p.befunde[0]
    assert "nur 1 von 20" in abgleich_hinweise(stand, None)[0]
    voll = _stand(_a3(), anzahl_3d=1)
    assert pruefe_abgleich(voll, None, _regel()).ergebnis is PruefErgebnis.BESTANDEN
    zwei_d = _stand(_a3(), a2=(Abgleich2D(index=0, gueltig=True),), anzahl_2d=3)
    assert pruefe_abgleich(zwei_d, None, _regel()).ergebnis is PruefErgebnis.BESTANDEN
    assert (
        pruefe_abgleich(zwei_d, None, _regel(pruefe_2d=True)).ergebnis
        is PruefErgebnis.NICHT_PRUEFBAR
    )


def test_pruefung_nicht_ausgefuehrt_zu_dict() -> None:
    d = pruefung_nicht_ausgefuehrt_zu_dict(_regel(qualitaet_max_m=2.0))
    assert d["ergebnis"] == "nicht_ausgefuehrt" and d["modus"] == "verweigern"
    assert d["grenzen"]["qualitaet_max_m"] == 2.0  # type: ignore[index]
    assert "nicht ausgeführt" in str(d["befunde"])


def test_verletzung_hat_vorrang_vor_nicht_pruefbar() -> None:
    stand = _stand(_a3(gueltig=False, qualitaet_ist_m=None))
    p = pruefe_abgleich(stand, None, _regel(qualitaet_max_m=1.0))
    assert p.ergebnis is PruefErgebnis.NICHT_BESTANDEN and len(p.befunde) == 2


def test_mehrere_3d_alle_muessen_bestehen() -> None:
    gut, schlecht = _a3(0), _a3(1, qualitaet_ist_m=3.0)
    regel = _regel(qualitaet_max_m=2.0)
    assert pruefe_abgleich(_stand(gut, gut), None, regel).ergebnis is PruefErgebnis.BESTANDEN
    p = pruefe_abgleich(_stand(gut, schlecht), None, regel)
    assert p.ergebnis is PruefErgebnis.NICHT_BESTANDEN and "3D-Abgleich 1" in p.befunde[0]


def test_kein_3d_abgleich_count_null_ist_nicht_bestanden() -> None:
    p = pruefe_abgleich(_stand(), None, _regel())
    assert p.ergebnis is PruefErgebnis.NICHT_BESTANDEN
    assert p.befunde == ("kein 3D-Abgleich vorhanden (Count = 0)",)


def test_nicht_gelesene_sammlung_ist_nicht_pruefbar_mit_grund() -> None:
    stand = AbgleichStand(nicht_lesbar={"Infos.HasAlignments": "Infos.HasAlignments ist False"})
    p = pruefe_abgleich(stand, None, _regel())
    assert p.ergebnis is PruefErgebnis.NICHT_PRUEFBAR
    assert "Infos.HasAlignments ist False" in p.befunde[0]


def test_nicht_gelesen_ist_nicht_pruefbar() -> None:
    p = pruefe_abgleich(None, "Gerät bietet kein Lesen des Abgleichs an", _regel())
    assert p.ergebnis is PruefErgebnis.NICHT_PRUEFBAR
    assert p.befunde == ("Abgleich nicht gelesen: Gerät bietet kein Lesen des Abgleichs an",)
    assert "ohne Angabe" in pruefe_abgleich(None, None, _regel()).befunde[0]


def test_2d_zaehlt_nur_mit_schalter() -> None:
    schlecht2d = (Abgleich2D(index=0, gueltig=False, scankopfabstand_m=1.0),)
    stand = _stand(_a3(), a2=schlecht2d)
    assert pruefe_abgleich(stand, None, _regel()).ergebnis is PruefErgebnis.BESTANDEN
    p = pruefe_abgleich(stand, None, _regel(pruefe_2d=True))
    assert p.ergebnis is PruefErgebnis.NICHT_BESTANDEN
    assert p.befunde == ("2D-Abgleich 0: ungültig (Valid = False)",)


def test_2d_ohne_eintrag_und_unbekannt() -> None:
    regel = _regel(pruefe_2d=True)
    assert pruefe_abgleich(_stand(_a3()), None, regel).ergebnis is PruefErgebnis.NICHT_BESTANDEN
    unklar = _stand(_a3(), anzahl_2d=None)
    assert pruefe_abgleich(unklar, None, regel).ergebnis is PruefErgebnis.NICHT_PRUEFBAR
    unbekannt = _stand(_a3(), a2=(Abgleich2D(index=0),))
    assert pruefe_abgleich(unbekannt, None, regel).ergebnis is PruefErgebnis.NICHT_PRUEFBAR
    gut = _stand(_a3(), a2=(Abgleich2D(index=0, gueltig=True),))
    assert pruefe_abgleich(gut, None, regel).ergebnis is PruefErgebnis.BESTANDEN


def test_befundtexte_nennen_lesbare_einheiten() -> None:
    p = pruefe_abgleich(
        _stand(_a3(qualitaet_ist_m=0.003, winkelunsicherheit_rad=math.radians(2.0))),
        None,
        _regel(qualitaet_max_m=0.002, winkel_max_rad=math.radians(1.0)),
    )
    text = " | ".join(p.befunde)
    assert "3 mm (0.003 m) über Grenze 2 mm (0.002 m)" in text
    assert "2 Grad (34.91 mrad) über Grenze 1 Grad (17.45 mrad)" in text


@pytest.mark.parametrize(
    "kw",
    [
        {"qualitaet_max_m": 0.0},
        {"position_max_m": -1.0},
        {"winkel_max_rad": math.nan},
        {"qualitaet_max_m": math.inf},
        {"position_max_m": True},
        {"winkel_max_rad": "1"},
    ],
)
def test_regel_validiert_grenzen(kw: dict[str, object]) -> None:
    with pytest.raises(ValueError, match="AbgleichRegel"):
        AbgleichRegel(**kw)  # type: ignore[arg-type]


def test_regel_ohne_obergrenze() -> None:
    assert AbgleichRegel(qualitaet_max_m=1e12).qualitaet_max_m == 1e12


def test_hinweise_ohne_auffaelligkeit_leer_und_mit_auffaelligkeiten() -> None:
    assert abgleich_hinweise(_stand(_a3(), a2=(Abgleich2D(index=0, gueltig=True),)), None) == ()
    assert abgleich_hinweise(None, "g") == ("Abgleich nicht gelesen: g",)
    stand = _stand(
        _a3(0, gueltig=False),
        _a3(1, nicht_lesbar={"qualitaet_ist_m": "COM-Fehler"}, qualitaet_ist_m=None),
        a2=(Abgleich2D(index=0, gueltig=None, nicht_lesbar={"gueltig": "x"}),),
        anzahl_2d=1,
        nicht_lesbar={"Alignments3D.Count": "y"},
    )
    text = abgleich_hinweise(stand, None)
    assert "Alignments3D.Count: y" in text
    assert "3D-Abgleich 0: Valid = False" in text
    assert "3D-Abgleich 1 qualitaet_ist_m: COM-Fehler" in text
    assert "2D-Abgleich 0: Valid = None" in text and "2D-Abgleich 0 gueltig: x" in text
    assert "kein 3D-Abgleich vorhanden (Count = 0)" in abgleich_hinweise(_stand(), None)


def test_pruefung_zu_dict() -> None:
    regel = _regel(qualitaet_max_m=2.0, pruefe_2d=True)
    p = pruefe_abgleich(_stand(_a3(gueltig=False)), None, regel)
    assert pruefung_zu_dict(regel, p) == {
        "modus": "verweigern",
        "ergebnis": "nicht_bestanden",
        "grenzen": {
            "qualitaet_max_m": 2.0,
            "position_max_m": None,
            "winkel_max_rad": None,
            "pruefe_2d": True,
        },
        "befunde": [
            "3D-Abgleich 0: ungültig (Valid = False)",
            "kein 2D-Abgleich vorhanden (Count = 0)",
        ],
    }
