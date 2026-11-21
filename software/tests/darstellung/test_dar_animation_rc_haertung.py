"""Animation und Standbild sind unabhängig von einer fremden ``matplotlibrc`` (Paket U-HAERTUNG-3D).

Eine Rechnerdatei mit anderem ``grid.color``, anderen Wandfarben (``axes3d.*axis.panecolor``),
``axes3d.grid``, ``axes.linewidth``, ``axes.facecolor`` oder ``text.hinting`` änderte das Standbild
(gemessen am PNG-/PDF-Hash). Der Animations-Kontext (:meth:`Plotstil.text_rc`) setzt diese und
weitere gemessene Schlüssel (:data:`STANDARD_RC_SCHLUESSEL`) auf den Matplotlib-Standard. Je
Schlüssel wird mit abweichendem Wert exportiert und mit dem Export unter ``rcdefaults()`` auf
Gleichheit der Bytes verglichen (PDF: ``SOURCE_DATE_EPOCH`` legt ``CreationDate`` fest).
"""

from __future__ import annotations

from collections.abc import Iterator
from contextlib import contextmanager
from dataclasses import replace
from pathlib import Path
from typing import Any

import matplotlib
import pytest
import test_dar_bild_export_dpi as ex
from dar_animation_hilfen import lange_platte
from matplotlib import rcParamsDefault
from matplotlib.figure import Figure

from ldv_automation.darstellung.animation3d import (
    BLICK_VORGABEN,
    AnimationsOptionen,
    zeichne_animation,
)
from ldv_automation.darstellung.bild import baue_stempel, speichere_arbeitsbild
from ldv_automation.darstellung.stil import STANDARD_RC_SCHLUESSEL, THESIS_STIL, Plotstil

STANDARD: dict[Any, Any] = dict(rcParamsDefault)
_ROT = (1.0, 0.0, 0.0, 1.0)
ABWEICHEND: dict[Any, Any] = {
    "axes.axisbelow": False,
    "axes.facecolor": "yellow",
    "axes.grid": True,
    "axes.labelpad": 12.0,
    "axes.labelweight": "bold",
    "axes.linewidth": 3.0,
    "axes3d.automargin": True,
    "axes3d.grid": False,
    "axes3d.xaxis.panecolor": _ROT,
    "axes3d.yaxis.panecolor": (0.0, 1.0, 0.0, 1.0),
    "axes3d.zaxis.panecolor": (0.0, 0.0, 1.0, 1.0),
    "font.weight": "bold",
    "grid.alpha": 0.3,
    "grid.color": "red",
    "grid.linestyle": "--",
    "grid.linewidth": 2.0,
    "lines.antialiased": False,
    "patch.linewidth": 3.0,
    "savefig.facecolor": "yellow",
    "text.antialiased": False,
    "text.hinting": "no_hinting",
    "xtick.direction": "in",
    "xtick.major.pad": 10.0,
    "xtick.major.size": 10.0,
    "xtick.major.width": 3.0,
    "ytick.direction": "in",
    "ytick.major.pad": 10.0,
    "ytick.major.size": 10.0,
    "ytick.major.width": 3.0,
}
OPT = AnimationsOptionen(punktlabels=True, blick=BLICK_VORGABEN["iso"])
PLATTE = lange_platte(2.25, 45, 9)


@contextmanager
def _rc(rc: dict[Any, Any]) -> Iterator[None]:
    """Matplotlib-Standard (``rcdefaults``, nicht die Rechner-``matplotlibrc``) plus ``rc``.

    Ohne GUI-``conftest`` (``tests/darstellung`` allein) trägt ``rcParams`` die Werte der
    Rechnerdatei; der Vergleich braucht den Standard als Bezug.
    """
    with matplotlib.rc_context():
        matplotlib.rcdefaults()
        matplotlib.rcParams.update(rc)
        yield


def _standbild(pfad: Path, rc: dict[Any, Any]) -> tuple[bytes, Any]:
    with _rc(rc):
        z = speichere_arbeitsbild(
            lambda f: zeichne_animation(f, PLATTE, OPT, ex.STIL),
            pfad,
            baue_stempel(dateiname="a.svd", ansicht="Animation", git_hash="abc"),
            ex.STIL,
        )
    return pfad.read_bytes(), z.hilfsobjekte["punktlabels_schritt"]


@pytest.fixture(autouse=True)
def _fest(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("SOURCE_DATE_EPOCH", "1700000000")  # PDF: festes CreationDate


def test_die_liste_der_schluessel_und_die_abweichenden_werte_decken_sich() -> None:
    assert set(ABWEICHEND) == set(STANDARD_RC_SCHLUESSEL)
    for k, v in ABWEICHEND.items():
        assert v != STANDARD[k], k  # der Wert weicht wirklich vom Standard ab


@pytest.mark.parametrize("endung", ["png", "pdf"])
@pytest.mark.parametrize("schluessel", sorted(ABWEICHEND))
def test_standbild_ist_bei_abweichendem_rc_schluessel_gleich_dem_standard(
    schluessel: str, endung: str, tmp_path: Path
) -> None:
    standard, s0 = _standbild(tmp_path / f"standard.{endung}", {})
    fremd, s1 = _standbild(tmp_path / f"fremd.{endung}", {schluessel: ABWEICHEND[schluessel]})
    assert s0 not in (None, 0) and s1 == s0  # Labels an, Dichte-Rechnung beteiligt
    assert fremd == standard


@pytest.mark.parametrize("endung", ["png", "pdf"])
def test_standbild_ist_bei_allen_abweichenden_schluesseln_zugleich_gleich_dem_standard(
    endung: str, tmp_path: Path
) -> None:
    standard, _ = _standbild(tmp_path / f"standard.{endung}", {})
    fremd, _ = _standbild(tmp_path / f"fremd.{endung}", dict(ABWEICHEND))
    assert fremd == standard


def test_label_masse_misst_mit_dem_standard_hinting_auch_bei_fremdem_hinting() -> None:
    """Der Messschlüssel von ``LabelMasse`` enthält ``text.hinting``: Messen und Zeichnen gleich."""
    with _rc({"text.hinting": "no_hinting"}):
        z = zeichne_animation(Figure(figsize=(8, 6), dpi=100), PLATTE, OPT, ex.STIL)
        masse = z.hilfsobjekte["label_masse"]
        assert matplotlib.rcParams["text.hinting"] == "no_hinting"  # außerhalb des Kontexts
    assert masse._messbedingungen is not None
    assert masse._messbedingungen[2] == STANDARD["text.hinting"]


@pytest.mark.parametrize("endung", ["png", "pdf"])
@pytest.mark.parametrize(
    "name", ["ansicht1_spektrum", "ansicht3_spitzen", "ansicht4_schwingform", "ansicht5_diagramm"]
)
def test_2d_export_ist_bei_abweichender_axes_linewidth_gleich_dem_standard(
    name: str, endung: str, tmp_path: Path
) -> None:
    def export(ziel: Path, rc: dict[Any, Any]) -> bytes:
        with _rc(rc):
            speichere_arbeitsbild(
                ex.FAELLE[name],
                ziel,
                baue_stempel(dateiname="a", ansicht=name, git_hash="c"),
                ex.STIL,
            )
        return ziel.read_bytes()

    standard = export(tmp_path / f"s.{endung}", {})
    assert export(tmp_path / f"f.{endung}", {"axes.linewidth": 3.0}) == standard


def test_gitterfarbe_3d_kommt_aus_dem_stil_nicht_aus_der_rc_datei() -> None:
    assert THESIS_STIL.text_rc()["grid.color"] == "#b0b0b0"  # Thesis: Matplotlib-Standard
    assert THESIS_STIL.gitter != "#b0b0b0"  # die 2D-Gitterfarbe bleibt eine eigene Größe
    assert replace(THESIS_STIL, gitter_3d="#E1E3E5").text_rc()["grid.color"] == "#E1E3E5"


@pytest.mark.parametrize("endung", ["png", "pdf"])
def test_standbild_traegt_die_gitterfarbe_3d_des_stils_auch_bei_fremder_grid_color(
    endung: str, tmp_path: Path
) -> None:
    def export(ziel: Path, rc: dict[Any, Any], stil: Plotstil) -> bytes:
        with _rc(rc):
            speichere_arbeitsbild(
                lambda f: zeichne_animation(f, PLATTE, OPT, stil),
                ziel,
                baue_stempel(dateiname="a.svd", ansicht="Animation", git_hash="abc"),
                stil,
            )
        return ziel.read_bytes()

    app = replace(ex.STIL, gitter_3d="#E1E3E5")
    thesis = export(tmp_path / f"t.{endung}", {}, ex.STIL)
    ein = export(tmp_path / f"a.{endung}", {}, app)
    assert ein != thesis  # die Stilgröße wirkt (sonst prüfte der Vergleich unten nichts)
    assert export(tmp_path / f"af.{endung}", {"grid.color": "red"}, app) == ein
    assert export(tmp_path / f"tf.{endung}", {"grid.color": "red"}, ex.STIL) == thesis
