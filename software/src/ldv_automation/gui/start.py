"""Start der Oberfläche: ``QApplication``, Stil, Hauptfenster und Threads der Sitzung."""

from __future__ import annotations

from collections.abc import Sequence

from PySide6.QtWidgets import QApplication

from ldv_automation.gui.hauptfenster import Hauptfenster
from ldv_automation.gui.stil import wende_an
from ldv_automation.sitzung import Sitzung


def starte_gui(sitzung: Sitzung, argv: Sequence[str] = ()) -> int:
    """Startet die Oberfläche und blockiert bis zum Schließen des Fensters.

    Die Sitzung startet Geräte- und Wächter-Thread; die Oberfläche selbst startet keinen
    Thread (Brief Abschnitt 4). Beim Ende werden beide Threads beendet.

    Returns
    -------
    int
        Rückgabewert der Qt-Ereignisschleife (0 bei normalem Ende).
    """
    app = QApplication.instance()
    if not isinstance(app, QApplication):
        app = QApplication(["ldv_automation", *argv])
    app.setApplicationName("LDV-Warteschlange")
    wende_an(app)
    sitzung.starte_threads()
    try:
        fenster = Hauptfenster(sitzung)
        fenster.show()
        return int(app.exec())
    finally:
        if not sitzung.beende_threads():
            print("Warnung: Geräte- oder Wächter-Thread endete nicht rechtzeitig.")
