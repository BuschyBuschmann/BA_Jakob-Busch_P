"""Liest die Erfassungseinstellungen einer PSV-Messdatei über Polytec File Access (nur lesen).

Zweck: Prüfschritte M5 und M8 am Messrechner (Fenster, Mittelung, Generator, Kanäle mit
Einheit, Kalibrierung und Richtung). Die Datei wird mit ``ReadOnly = True`` geöffnet, es wird
nichts geschrieben; nur eine Kopie verwenden, die nicht in PSV geöffnet ist.

Aufruf (Windows, pywin32)::

    python einstellungen_lesen.py "D:\\...\\kopie.svd" > einstellungen.txt

Eigenschaftsnamen aus dem Basic Engine Manual (POLYPROPERTIESLib, POLYWAVEFORMSLib).
"""

from __future__ import annotations

import sys
from typing import Any

KANAL = (
    "Name ShortName Type Active Reference ReferencePointIndex Quantity Unit "
    "IntDiffPhysicalQuantity Calibration InputRange InputCoupling ICPInput DifferentialInput "
    "InputImpedance DirectionOfVibration WindowFunction WindowFunctionParams "
    "WindowFunctionRMSCorrection DigitalFilter SignalDelay SEActive VibrometerIndex"
).split()
FFT = (
    "Bandwidth StartFrequency EndFrequency Lines SampleFrequency SampleResolution SampleTime "
    "Samples Overlap"
).split()
MITTELUNG = ["Type", "Count"]
GENERATOR = (
    "Active Amplitude Offset SteadyStateTime MultipleChannels UseAmplitudeCorrection".split()
)
WELLENFORM = (
    "Frequency StartFrequency EndFrequency SweepTime BurstStart BurstLength BurstStartEx "
    "BurstLengthEx"
).split()
ALLGEMEIN = (
    "SaveTimeDataForScan RealSampleFrequency AutoRemeasure PrincipalComponentAnalysis".split()
)
TRIGGER = "Source Edge Level PreTrigger PhaseFromRef".split()


def lies(obj: Any, namen: list[str], einzug: str = "  ") -> None:
    for name in namen:
        try:
            wert = getattr(obj, name)
            if callable(wert):
                continue
            if isinstance(wert, tuple):
                wert = list(wert)
            print(f"{einzug}{name} = {wert!r}")
        except Exception as exc:  # noqa: BLE001 - nur lesen, Fehler je Eigenschaft melden
            print(f"{einzug}{name}: nicht lesbar ({type(exc).__name__})")


def abschnitt(props: Any, has: str, get: str, titel: str) -> Any:
    try:
        if not getattr(props, has):
            print(f"\n[{titel}] nicht vorhanden")
            return None
        print(f"\n[{titel}]")
        return getattr(props, get)
    except Exception as exc:  # noqa: BLE001
        print(f"\n[{titel}] nicht lesbar ({type(exc).__name__}: {exc})")
        return None


def main(pfad: str) -> int:
    import win32com.client  # nur unter Windows mit pywin32

    pf = win32com.client.dynamic.Dispatch("PolyFile.PolyFile")
    pf.ReadOnly = True  # einzige Zuweisung: Schreibschutz vor dem Öffnen
    pf.Open(pfad)
    try:
        print(f"Datei: {pfad}")
        print(f"Programmversion: {pf.Version.ProgramVersionString}")
        modes = pf.Infos.AcquisitionInfoModes
        print(f"AcquisitionInfoModes.ActiveMode = {modes.ActiveMode!r}")
        props = modes.ActiveProperties

        if (fft := abschnitt(props, "HasFftProperties", "FftProperties", "FFT")) is not None:
            lies(fft, FFT)
        if (avg := abschnitt(props, "HasAverageProperties", "AverageProperties",
                             "Mittelung")) is not None:  # fmt: skip
            lies(avg, MITTELUNG)
        if (gen := abschnitt(props, "HasGeneralProperties", "GeneralProperties",
                             "Allgemein")) is not None:  # fmt: skip
            lies(gen, ALLGEMEIN)
        if (trg := abschnitt(props, "HasTriggerProperties", "TriggerProperties",
                             "Trigger")) is not None:  # fmt: skip
            lies(trg, TRIGGER)
        if (gens := abschnitt(props, "HasGeneratorsProperties", "GeneratorsProperties",
                              "Generator")) is not None:  # fmt: skip
            for i in range(1, gens.Count + 1):
                g = gens.Item(i)
                print(f" Generator {i}")
                lies(g, GENERATOR)
                try:
                    w = g.Waveform
                    print("  Waveform:")
                    lies(w, WELLENFORM, "    ")
                except Exception as exc:  # noqa: BLE001
                    print(f"  Waveform: nicht lesbar ({type(exc).__name__})")
        if (chs := abschnitt(props, "HasChannelsProperties", "ChannelsProperties",
                             "Kanäle")) is not None:  # fmt: skip
            for i in range(1, chs.Count + 1):
                print(f" Kanal {i}")
                try:
                    lies(chs.Item(i), KANAL)
                except Exception as exc:  # noqa: BLE001
                    print(f"  nicht lesbar ({type(exc).__name__}: {exc})")
    finally:
        pf.Close()
        print("\nDatei geschlossen.")
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Aufruf: python einstellungen_lesen.py <kopie.svd>")
        sys.exit(2)
    sys.exit(main(sys.argv[1]))
