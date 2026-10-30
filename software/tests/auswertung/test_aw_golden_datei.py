"""Golden-File-Test an ``Input/20261012_ref_Mitte.svd`` (FG-02 9.9, A7); ohne Datei übersprungen.

Geprüft mit den Toleranzen aus FG-02 Abschnitt 8 (rtol 1e-5, atol 1e-6·max|Kurve|; die
Datei speichert float32):

- alle 35 von PSV gespeicherten Punktmittel (``AvgSeq_Data``) gegen die Punktmittel nach
  3.2/3.3 (|CP|, |CPH|, ABS, AP, |H1|, |H2|, γ²);
- alle PSV-Banddaten des Gesamtbands (``Band_Data``) je Punkt gegen ``rms_psv`` bzw.
  ``bandnorm`` nach 3.8 (außer CP-Bändern, die FG-02 nicht definiert);
- die an der Datei belegte FRF-Bandnorm H1 Vib X/Ref1 an Punkt 0: 0,01851376 (S17);
- P-07 liefert q >= 0,9 (W3: 0,982);
- die Datei bleibt unverändert (SHA-256 vor/nach).
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

import numpy as np
import pytest

from ldv_automation.auswertung import Auswertung, Toleranzen, werte_aus
from ldv_automation.auswertung.baender import band_amplitude, band_ap, band_frf
from ldv_automation.auswertung.export import sha256_datei
from ldv_automation.auswertung.mittel import punktmittel_betrag
from ldv_automation.auswertung.svd_adapter import aus_svd_messung

DATEI = Path(__file__).resolve().parents[3] / "Input" / "20261012_ref_Mitte.svd"
SHA256_DATEI = "7ef46262df0055f5a45470ae0fc5e6bde547624cdee6b5dc3838060a452e790b"
#: Zeitkanalnummer → Kanalname dieser Datei (vom W2-Leser über Kanalanker belegt).
NAMEN = {0: "Vib X", 1: "Vib Y", 2: "Vib Z", 3: "Ref1", 4: "Ref2"}
TOL = Toleranzen()

pytestmark = pytest.mark.skipif(not DATEI.is_file(), reason="Messdatei nicht vorhanden")


@pytest.fixture(scope="module")
def ergebnis() -> tuple[Any, Auswertung, str]:
    import beispiel_svd  # bindet den unveränderten W2-Leser aus tools/svd_analyse ein

    vorher = sha256_datei(DATEI)
    messung = beispiel_svd.lese_svd_werkzeug(DATEI)
    auswertung = werte_aus(
        aus_svd_messung(messung, sha256=vorher), antriebspunkt=("Ref2", "Ref1", "akzeleranz")
    )
    return messung, auswertung, vorher


def _kanaele(formel: str) -> list[str]:
    return [NAMEN[int(n)] for n in re.findall(r"T\[(\d+)\]", formel)]


def _punktmittel_ist(formel: str, a: Auswertung) -> np.ndarray:
    t = _kanaele(formel)
    if formel.startswith("AVGSEQ[COH["):
        m = a.paare[(t[1], t[2])].mittel_kohaerenz.mittel_arithmetisch
    elif formel.startswith("AVGSEQ[ABS[FRF["):
        pa = a.paare[(t[1], t[2])]
        m = (pa.mittel_h1 if t[0] == t[2] else pa.mittel_h2).mittel_betrag
    elif formel.startswith("AVGSEQ[ABS[AVG[CPH["):
        m = a.paare[(t[1], t[2])].mittel_spektrum_kohaerent.mittel_betrag
    elif formel.startswith("AVGSEQ[ABS[AVG[CP["):
        m = punktmittel_betrag(a.daten.cp[(t[0], t[1])]).mittel_betrag
    elif formel.startswith("AVGSEQ[AVG[AP["):
        m = a.mittel_ap[t[0]].mittel_arithmetisch
    elif formel.startswith("AVGSEQ[AVG[ABS["):
        m = a.mittel_betrag[t[0]].mittel_betrag
    else:  # pragma: no cover - nur bei unbekannter Formel
        raise AssertionError(f"unbekannte Punktmittelformel {formel}")
    assert m is not None
    return m


def test_datei_unveraendert(ergebnis: tuple[Any, Auswertung, str]) -> None:
    _, _, vorher = ergebnis
    assert vorher == SHA256_DATEI
    assert sha256_datei(DATEI) == vorher


def test_punktmittel_gegen_avgseq(ergebnis: tuple[Any, Auswertung, str]) -> None:
    messung, a, _ = ergebnis
    assert len(messung.punktmittel) == 35
    abweichend = []
    for pm in messung.punktmittel:
        ist = _punktmittel_ist(pm.formel, a)
        if not TOL.kurve_stimmt(ist, pm.werte):
            abweichend.append(pm.formel)
    assert abweichend == []


def test_banddaten_gegen_rms_psv_und_bandnorm(ergebnis: tuple[Any, Auswertung, str]) -> None:
    messung, a, _ = ergebnis
    d = a.daten
    f_u, f_o = float(d.frequenz_hz[0]), float(d.frequenz_hz[-1])
    geprueft = 0
    for name, band in messung.baender.items():
        signal = messung.signale.get(f"M{name[1:]}")
        kanaele = [k[0] for k in band.kanaele]
        if band.titel.startswith(("H1 ", "H2 ")):
            frf = a.paare[(kanaele[0], kanaele[1])].frf
            h = frf.h1 if band.titel.startswith("H1") else frf.h2
            ist = band_frf(h, d.frequenz_hz, f_u, f_o).bandnorm
        elif signal is not None and signal.art == "AP":
            ist = band_ap(d.ap[kanaele[0]], d.frequenz_hz, f_u, f_o).rms_psv
        elif signal is not None and signal.art == "ABS":
            ist = band_amplitude(d.betrag[kanaele[0]], d.frequenz_hz, f_u, f_o).rms_psv
        elif signal is not None and signal.art == "CPH":
            paar = (signal.kanaele[0], signal.kanaele[1])
            ist = band_amplitude(a.paare[paar].paar.cph, d.frequenz_hz, f_u, f_o).rms_psv
        else:
            assert signal is not None and signal.art == "CP"  # in FG-02 3.8 nicht definiert
            continue
        assert ist is not None
        assert TOL.kurve_stimmt(ist, band.werte), name
        geprueft += 1
    assert geprueft == 22  # 29 Bänder, davon 7 CP-Bänder ohne Definition in FG-02


def test_bandnorm_h1_s17_punkt_0(ergebnis: tuple[Any, Auswertung, str]) -> None:
    _, a, _ = ergebnis
    d = a.daten
    h1 = a.paare[("Vib X", "Ref1")].frf.h1
    b = band_frf(h1, d.frequenz_hz, float(d.frequenz_hz[0]), float(d.frequenz_hz[-1]))
    assert b.bandnorm is not None
    assert b.bandnorm[0] == pytest.approx(0.01851376, rel=1e-5)


def test_plausibilitaet_an_der_datei(ergebnis: tuple[Any, Auswertung, str]) -> None:
    _, a, _ = ergebnis
    nach_id: dict[tuple[str, str], Any] = {(e.id, e.bezug): e for e in a.pruefungen}
    p07 = nach_id[("P-07", "Vib Z/Ref1")]
    assert p07.status == "ok" and p07.wert >= 0.9
    for e in a.pruefungen:
        assert e.status != "fehler", e
    p08 = nach_id[("P-08", "Ref2/Ref1 (akzeleranz)")]
    assert p08.status == "warnung" and p08.wert <= 0.05  # W3 2.3: r = 0 (M8 offen)
    assert nach_id[("P-06", "")].status == "ok"
