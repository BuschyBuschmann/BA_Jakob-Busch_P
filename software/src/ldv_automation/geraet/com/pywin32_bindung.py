"""pywin32-Anbindung: **einzige** Datei des Pakets mit pywin32-Import.

Abdeckung: Die ganze Klasse ist per ``# pragma: no cover`` ausgenommen. Begründung: Sie
braucht Windows, pywin32 und eine laufende PSV und ist ohne Gerät nicht ausführbar
(KONVENTIONEN, Standard-Prüfung). Sie enthält deshalb bewusst keine Logik: Dekodierung und
Auswertung der Prozessliste liegen in :mod:`.bindung`, jede Prüfung im Proxy und im Adapter,
die Übersetzung roher Ausnahmen (z. B. ``ImportError`` ohne pywin32, ``com_error``
``RPC_E_CHANGED_MODE``) in ``GeraeteFehler`` im Adapter. Die Importe stehen in den Methoden,
damit das Modul unter Linux importierbar bleibt.
"""

from __future__ import annotations

import subprocess

from ldv_automation.geraet.com.bindung import dekodiere_prozessliste, psv_treffer

TASKLIST_ZEITLIMIT_S = 30.0
"""Obergrenze für ``tasklist`` (Annahme; die Liste kommt üblicherweise in < 1 s)."""

TASKLIST_CODEC = "oem"
"""Konsolen-Codepage von ``tasklist`` (Python-Codec ``oem``, nur unter Windows)."""


class Pywin32Bindung:  # pragma: no cover - braucht Windows, pywin32 und PSV (s. Modultext)
    """:class:`~.bindung.ComBindung` mit pywin32 (Late Binding, ADR-003)."""

    def initialisiere_thread(self) -> None:
        """``pythoncom.CoInitialize()`` (STA) für den Geräte-Thread (ADR-008)."""
        import pythoncom

        pythoncom.CoInitialize()

    def beende_thread(self) -> None:
        """``pythoncom.CoUninitialize()``."""
        import pythoncom

        pythoncom.CoUninitialize()

    def psv_prozesse(self) -> tuple[str, ...] | None:
        """Prozessprüfung per ``tasklist``; ``None``, wenn die Liste nicht lesbar ist."""
        try:
            roh = subprocess.run(
                ["tasklist", "/FO", "CSV", "/NH"],
                capture_output=True,
                check=True,
                timeout=TASKLIST_ZEITLIMIT_S,
            ).stdout
        except (OSError, subprocess.SubprocessError):
            return None
        text = dekodiere_prozessliste(roh, TASKLIST_CODEC)
        return None if text is None else psv_treffer(text)

    def dispatch(self, progid: str) -> object:
        """``win32com.client.dynamic.Dispatch(progid)`` (Late Binding, nutzt nie gen_py)."""
        import win32com.client

        return win32com.client.dynamic.Dispatch(progid)
