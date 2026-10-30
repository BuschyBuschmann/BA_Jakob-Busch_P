"""Testdaten der Referenzfälle aus FG-02 Abschnitt 9 (Paket W5-1).

Erzeugung nach der Skalierungsvorschrift FG-02 2.1 und dem Prüfskript im Anhang von FG-02:
:math:`\\hat X_k = 2/\\sum w_n \\cdot \\sum w_n x_n e^{-i2\\pi kn/N}`, Linien
:math:`k = 1 … 1600` (:math:`k_0 = 1`), :math:`BW = 2500` Hz, :math:`N = 4000`,
:math:`f_s = 6250` Hz, :math:`\\Delta f = 1{,}5625` Hz. Die Software selbst rechnet keine
Spektren aus Zeitdaten; diese Funktionen erzeugen nur Testdaten.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import numpy as np
import numpy.typing as npt

from ldv_automation.auswertung.daten import Messdaten, Punkte

BW_HZ = 2500.0
N_LINIEN = 1600
N_ABTAST = 4000
FS_HZ = 6250.0
DF_HZ = FS_HZ / N_ABTAST  # 1,5625 Hz
ZEIT_S = np.arange(N_ABTAST) / FS_HZ
FREQUENZ_HZ = DF_HZ * np.arange(1, N_LINIEN + 1, dtype=np.float64)

RECHTECK = np.ones(N_ABTAST)
HANN = 0.5 - 0.5 * np.cos(2.0 * np.pi * np.arange(N_ABTAST) / N_ABTAST)  # periodisch


def spektrum(
    x: npt.NDArray[np.float64], fenster: npt.NDArray[np.float64]
) -> npt.NDArray[np.complex128]:
    """Einseitiges, amplitudentreues Spektrum (Spitzenwert), Linien 1 … 1600."""
    x_k = 2.0 * np.fft.rfft(fenster * x) / fenster.sum()
    return np.asarray(x_k[1 : N_LINIEN + 1], dtype=np.complex128)


def sinus(amplitude: float, linie: float, phase_rad: float = 0.0) -> npt.NDArray[np.float64]:
    """:math:`A\\cos(2\\pi\\,\\text{linie}\\,\\Delta f\\,t + \\varphi)`."""
    return amplitude * np.cos(2.0 * np.pi * linie * DF_HZ * ZEIT_S + phase_rad)


def mobilitaet_sdof(
    f_hz: npt.ArrayLike, fn_hz: float = 100.0, zeta: float = 0.01, m_kg: float = 1.0
) -> npt.NDArray[np.complex128]:
    """Mobilität :math:`Y = i\\omega/(k - m\\omega^2 + ic\\omega)` in (m/s)/N (FG-02 9.4)."""
    w = 2.0 * np.pi * np.asarray(f_hz, dtype=np.float64)
    wn = 2.0 * np.pi * fn_hz
    k = m_kg * wn**2
    c = 2.0 * zeta * m_kg * wn
    return np.asarray(1j * w / (k - m_kg * w**2 + 1j * c * w), dtype=np.complex128)


def mobilitaet_moden(
    f_hz: npt.ArrayLike, moden_hz: list[float], zeta: float = 0.01
) -> npt.NDArray[np.complex128]:
    """Summe :math:`\\sum_r i\\omega/(\\omega_r^2 - \\omega^2 + 2i\\zeta\\omega_r\\omega)`.

    Modalmasse 1 kg, Einheit (m/s)/N (FG-02 9.4, RF-M).
    """
    w = 2.0 * np.pi * np.asarray(f_hz, dtype=np.float64)
    ergebnis = np.zeros_like(w, dtype=np.complex128)
    for fr in moden_hz:
        wr = 2.0 * np.pi * fr
        ergebnis = ergebnis + 1j * w / (wr**2 - w**2 + 2j * zeta * wr * w)
    return ergebnis


def messdaten(
    *,
    frequenz_hz: npt.NDArray[np.float64],
    ap: dict[str, npt.NDArray[np.float64]],
    cp: dict[tuple[str, str], npt.NDArray[np.complex128]] | None = None,
    cph: dict[tuple[str, str], npt.NDArray[np.complex128]] | None = None,
    betrag: dict[str, npt.NDArray[np.float64]] | None = None,
    einheiten: dict[str, str] | None = None,
    delta_f_hz: float | None = None,
    phase_gueltig: bool = True,
) -> Messdaten:
    """Baut Messdaten mit P Punkten aus der Form der Felder."""
    p = next(iter(ap.values())).shape[0]
    alle = {"Vib X": "m/s", "Vib Y": "m/s", "Vib Z": "m/s", "Ref1": "N", "Ref2": "m/s²"}
    alle.update(einheiten or {})
    return Messdaten(
        frequenz_hz=frequenz_hz,
        delta_f_hz=delta_f_hz if delta_f_hz is not None else float(frequenz_hz[1] - frequenz_hz[0]),
        punkte=Punkte(
            index=np.arange(p, dtype=np.int64),
            label=np.arange(100, 100 + p, dtype=np.int64),
            koordinaten_m=np.column_stack(
                [np.linspace(0.0, 0.1, p), np.zeros(p), np.zeros(p)]
            ).astype(np.float64),
        ),
        einheiten=alle,
        ap=ap,
        betrag=betrag or {},
        cp=cp or {},
        cph=cph or {},
        phase_gueltig=phase_gueltig,
    )


def erwartungswert_paar(
    h: complex | npt.NDArray[np.complex128],
    s_x: float,
    n_r: float,
    n_v: float,
    form: tuple[int, int] = (1, 1),
    antwort: str = "Vib Z",
    referenz: str = "Ref1",
) -> Messdaten:
    """Messdaten mit Erwartungswerten nach FG-02 9.2 für ein Paar (Voreinstellung Vib Z/Ref1)."""
    h_feld = np.broadcast_to(np.asarray(h, dtype=np.complex128), form)
    ap_b = np.full(form, s_x + n_r)
    ap_a = (np.abs(h_feld) ** 2 * s_x + n_v).astype(np.float64)
    cp = (h_feld * s_x).astype(np.complex128)
    return messdaten(
        frequenz_hz=DF_HZ * np.arange(1, form[1] + 1, dtype=np.float64),
        ap={antwort: ap_a, referenz: ap_b},
        cp={(antwort, referenz): cp},
        delta_f_hz=DF_HZ,
    )


# --- Ersatz für das Ergebnis des W2-Lesers (svd_lesen.SvdMessung) ---------------------------


@dataclass
class FakeFft:
    delta_f_hz: float


@dataclass
class FakePunkte:
    index: npt.NDArray[np.int64]
    label: npt.NDArray[np.int64]
    koordinaten_m: npt.NDArray[np.float64]


@dataclass
class FakeSignal:
    name: str
    art: str
    kanaele: tuple[str, ...]
    werte: npt.NDArray[Any]


@dataclass
class FakeBand:
    kanaele: tuple[tuple[str, str, str], ...]


@dataclass
class FakeSvdMessung:
    pfad: Path
    fft: FakeFft
    frequenz_hz: npt.NDArray[np.float64]
    punkte: FakePunkte
    signale: dict[str, FakeSignal]
    baender: dict[str, FakeBand] = field(default_factory=dict)


EINHEITEN_DATEI = {
    "Vib X": ("Geschwindigkeit", "m/s"),
    "Vib Y": ("Geschwindigkeit", "m/s"),
    "Vib Z": ("Geschwindigkeit", "m/s"),
    "Ref1": ("Kraft", "N"),
    "Ref2": ("Beschleunigung", "m/s²"),
}


def fake_svd_messung(pfad: Path, p: int = 4, rauschen: float = 0.0) -> FakeSvdMessung:
    """Messung wie die Beispieldatei (3D + Ref1 + Ref2), synthetisch aus drei Moden.

    Raster 0,5 Hz bis 400 Hz, Moden 100/150/260 Hz; die Komponenten X, Y, Z sind auf Ref1
    bezogen, Ref2/Ref1 ist die Akzeleranz desselben Systems (Antriebspunkt).
    ``rauschen`` ist ein unkorreliertes Autospektrum am Ausgang ((m/s)²), das γ² senkt.
    """
    f = (np.arange(1, 801) * 0.5).astype(np.float64)
    y = mobilitaet_moden(f, [100.0, 150.0, 260.0])
    skala = np.linspace(1.0, 2.0, p)[:, None]
    signale: dict[str, FakeSignal] = {}
    ap_ref1 = np.ones((p, f.size))
    akz = np.broadcast_to(1j * 2 * np.pi * f * y, (p, f.size))
    komponenten = {"Vib X": 0.3 * skala * y, "Vib Y": 0.5j * skala * y, "Vib Z": skala * y}
    nr = 0
    for kanal, h in komponenten.items():
        signale[f"M{nr}"] = FakeSignal(f"M{nr}", "CP", (kanal, "Ref1"), h.astype(np.complex128))
        signale[f"M{nr + 1}"] = FakeSignal(
            f"M{nr + 1}", "CPH", (kanal, "Ref1"), h.astype(np.complex128)
        )
        signale[f"M{nr + 2}"] = FakeSignal(
            f"M{nr + 2}", "AP", (kanal,), (np.abs(h) ** 2 * 1.0001 + rauschen).astype(np.float32)
        )
        nr += 3
    signale[f"M{nr}"] = FakeSignal(f"M{nr}", "CP", ("Ref2", "Ref1"), akz.astype(np.complex128))
    signale[f"M{nr + 1}"] = FakeSignal(f"M{nr + 1}", "AP", ("Ref2",), np.abs(akz) ** 2)
    signale[f"M{nr + 2}"] = FakeSignal(f"M{nr + 2}", "AP", ("Ref1",), ap_ref1)
    signale[f"M{nr + 3}"] = FakeSignal(f"M{nr + 3}", "ABS", ("Ref1",), ap_ref1.copy())
    baender = {
        f"S{i}": FakeBand(((k, g, e),)) for i, (k, (g, e)) in enumerate(EINHEITEN_DATEI.items())
    }
    gitter = np.array([[x, yy, 0.0] for yy in range(2) for x in range(2)], dtype=np.float64)
    return FakeSvdMessung(
        pfad=pfad,
        fft=FakeFft(0.5),
        frequenz_hz=f,
        punkte=FakePunkte(
            index=np.arange(p, dtype=np.int64),
            label=np.arange(132, 132 + p, dtype=np.int64),
            koordinaten_m=np.resize(gitter, (p, 3)).astype(np.float64) * 0.1,
        ),
        signale=signale,
        baender=baender,
    )
