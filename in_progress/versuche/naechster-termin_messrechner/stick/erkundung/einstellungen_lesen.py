r"""Liest die Erfassungseinstellungen einer PSV-Messdatei über Polytec File Access (nur lesen).

Zweck: Prüfschritte M5 und M8 am Messrechner (Fenster, Mittelung, Generator, Kanäle mit
Einheit, Kalibrierung und Richtung). Die Datei wird mit ``ReadOnly = True`` geöffnet, es wird
nichts geschrieben; nur eine Kopie verwenden, die nicht in PSV geöffnet ist. Dieses Werkzeug
nutzt den Whitelist-Proxy von ``erkundung.py`` nicht.

Aufruf (Windows, pywin32)::

    python einstellungen_lesen.py "D:\...\kopie.svd" > einstellungen.txt

Eigenschaftsnamen aus dem Basic Engine Manual (POLYPROPERTIESLib, POLYWAVEFORMSLib).

Annahmen: Die Listen der Eigenschaftsnamen unten sind aus dem Handbuch übernommen und am
Gerät nur teilweise bestätigt (Erkundung 1b, 2026-11-02). Je Eigenschaft wird gemeldet:
``name = wert``, ``nicht lesbar`` (Ausnahme) oder ``übersprungen (aufrufbar)`` (Methode statt
Eigenschaft). Fehlt ein Abschnitt (``Has…`` ist ``False`` oder fehlt), steht „nicht vorhanden“.

Offen (am Gerät zu testen, hier nicht umgesetzt): Die Waveform-Parameter des Generators sind
vermutlich nur nach einem Cast auf das konkrete Wellenform-Interface lesbar; die Ausgabe
„Waveform-Parameter nicht lesbar (Cast nötig)“ markiert genau diesen Fall.
"""

from __future__ import annotations

import sys
from typing import Any

KANAL = [
    "Name",
    "ShortName",
    "Type",
    "Active",
    "Reference",
    "ReferencePointIndex",
    "Quantity",
    "Unit",
    "IntDiffPhysicalQuantity",
    "Calibration",
    "InputRange",
    "InputCoupling",
    "ICPInput",
    "DifferentialInput",
    "InputImpedance",
    "DirectionOfVibration",
    "WindowFunction",
    "WindowFunctionParams",
    "WindowFunctionRMSCorrection",
    "DigitalFilter",
    "SignalDelay",
    "SEActive",
    "VibrometerIndex",
]
FFT = [
    "Bandwidth",
    "StartFrequency",
    "EndFrequency",
    "Lines",
    "SampleFrequency",
    "SampleResolution",
    "SampleTime",
    "Samples",
    "Overlap",
]
MITTELUNG = ["Type", "Count"]
GENERATOR = [
    "Active",
    "Amplitude",
    "Offset",
    "SteadyStateTime",
    "MultipleChannels",
    "UseAmplitudeCorrection",
]
WELLENFORM = [
    "Frequency",
    "StartFrequency",
    "EndFrequency",
    "SweepTime",
    "BurstStart",
    "BurstLength",
    "BurstStartEx",
    "BurstLengthEx",
]
ALLGEMEIN = [
    "SaveTimeDataForScan",
    "RealSampleFrequency",
    "AutoRemeasure",
    "PrincipalComponentAnalysis",
]
TRIGGER = ["Source", "Edge", "Level", "PreTrigger", "PhaseFromRef"]

WAVEFORM_CAST_HINWEIS = (
    "Waveform-Parameter nicht lesbar (Cast auf das konkrete Wellenform-Interface nötig, "
    "am Gerät zu klären; siehe Kopf von einstellungen_lesen.py)"
)


def lies(obj: Any, namen: list[str], einzug: str = "  ") -> tuple[int, int]:
    """Gibt die Eigenschaften ``namen`` von ``obj`` aus.

    Returns
    -------
    tuple[int, int]
        Anzahl gelesener und Anzahl nicht lesbarer Eigenschaften (Übersprungene zählen nicht).
    """
    gelesen = nicht_lesbar = 0
    for name in namen:
        try:
            wert = getattr(obj, name)
            if callable(wert):
                print(f"{einzug}{name}: übersprungen (aufrufbar, keine Eigenschaft)")
                continue
            if isinstance(wert, tuple):
                wert = list(wert)
            print(f"{einzug}{name} = {wert!r}")
            gelesen += 1
        except Exception as exc:  # nur lesen, Fehler je Eigenschaft melden
            print(f"{einzug}{name}: nicht lesbar ({type(exc).__name__})")
            nicht_lesbar += 1
    return gelesen, nicht_lesbar


def abschnitt(props: Any, has: str, get: str, titel: str) -> Any:
    """Gibt den Abschnitt ``get`` zurück, wenn ``has`` wahr ist; sonst ``None`` mit Meldung."""
    try:
        if not getattr(props, has):
            print(f"\n[{titel}] nicht vorhanden")
            return None
        print(f"\n[{titel}]")
        return getattr(props, get)
    except AttributeError as exc:
        # fehlt ``has`` selbst, gibt es den Abschnitt in dieser Version nicht
        print(f"\n[{titel}] nicht vorhanden ({exc})")
        return None
    except Exception as exc:
        print(f"\n[{titel}] nicht lesbar ({type(exc).__name__}: {exc})")
        return None


def lies_generator(g: Any) -> None:
    """Gibt einen Generator samt Waveform aus; Cast-Problem wird eindeutig gemeldet."""
    lies(g, GENERATOR)
    try:
        w = g.Waveform
    except Exception as exc:
        print(f"  Waveform: nicht lesbar ({type(exc).__name__}); {WAVEFORM_CAST_HINWEIS}")
        return
    print("  Waveform:")
    gelesen, nicht_lesbar = lies(w, WELLENFORM, "    ")
    if gelesen == 0 and nicht_lesbar > 0:
        print(f"    {WAVEFORM_CAST_HINWEIS}")


def main(pfad: str) -> int:
    """Liest und druckt die Einstellungen der Datei ``pfad``; Rückgabe ist der Exit-Code."""
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
        avg = abschnitt(props, "HasAverageProperties", "AverageProperties", "Mittelung")
        if avg is not None:
            lies(avg, MITTELUNG)
        gen = abschnitt(props, "HasGeneralProperties", "GeneralProperties", "Allgemein")
        if gen is not None:
            lies(gen, ALLGEMEIN)
        trg = abschnitt(props, "HasTriggerProperties", "TriggerProperties", "Trigger")
        if trg is not None:
            lies(trg, TRIGGER)
        gens = abschnitt(props, "HasGeneratorsProperties", "GeneratorsProperties", "Generator")
        if gens is not None:
            for i in range(1, gens.Count + 1):
                print(f" Generator {i}")
                lies_generator(gens.Item(i))
        chs = abschnitt(props, "HasChannelsProperties", "ChannelsProperties", "Kanäle")
        if chs is not None:
            for i in range(1, chs.Count + 1):
                print(f" Kanal {i}")
                try:
                    lies(chs.Item(i), KANAL)
                except Exception as exc:
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
