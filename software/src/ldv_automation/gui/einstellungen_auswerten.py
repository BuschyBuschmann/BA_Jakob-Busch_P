"""Gemerkte Einstellungen des Reiters „Auswerten“ über ``QSettings`` (P-AUSW T4).

Gemerkt werden der zuletzt benutzte Ordner des Öffnen-Dialogs und die Liste „Zuletzt geöffnet“
(höchstens :data:`~ldv_automation.gui.anzeige_aktionen.ZULETZT_MAX` Einträge). Die Datei ist
eine INI-Datei; ihr Pfad ist austauschbar, damit Tests einen temporären Pfad verwenden und nie
die Einstellungen des Nutzers berühren.

Dünnes Qt-Modul (Abdeckung nur mit ``pytest -m gui``); die Listenlogik liegt Qt-frei in
:func:`~ldv_automation.gui.anzeige_aktionen.zuletzt_aktualisieren`.
"""

from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import QSettings, QStandardPaths

from ldv_automation.gui.anzeige_aktionen import ZULETZT_MAX, zuletzt_aktualisieren

__all__ = ["AuswertenEinstellungen", "standard_pfad"]

DATEINAME = "auswerten.ini"
"""Name der INI-Datei im Konfigurationsordner der Anwendung."""


def standard_pfad() -> str:
    """Pfad der INI-Datei im Konfigurationsordner der Anwendung (Windows: ``%LOCALAPPDATA%``)."""
    ordner = QStandardPaths.writableLocation(QStandardPaths.StandardLocation.AppConfigLocation)
    if not ordner:
        ordner = str(Path.home())
    return str(Path(ordner) / DATEINAME)


class AuswertenEinstellungen:
    """Letzter Ordner und „Zuletzt geöffnet“ in einer INI-Datei.

    Parameters
    ----------
    pfad : str, optional
        Pfad der INI-Datei; ohne Angabe :func:`standard_pfad`.
    """

    def __init__(self, pfad: str | None = None) -> None:
        self._pfad = pfad if pfad is not None else standard_pfad()
        self._daten = QSettings(self._pfad, QSettings.Format.IniFormat)

    @property
    def pfad(self) -> str:
        """Pfad der INI-Datei."""
        return self._pfad

    def zuletzt(self) -> tuple[str, ...]:
        """Zuletzt geöffnete Dateien, neueste zuerst (höchstens fünf)."""
        wert = self._daten.value("zuletzt", [])
        if isinstance(wert, str):  # QSettings liefert eine Liste mit einem Eintrag als Text
            wert = [wert]
        liste = [str(p) for p in wert] if isinstance(wert, list) else []
        return tuple(liste[:ZULETZT_MAX])

    def merke_datei(self, pfad: str) -> tuple[str, ...]:
        """Setzt ``pfad`` an den Anfang der Liste und speichert sie; gibt die neue Liste zurück."""
        neu = zuletzt_aktualisieren(self.zuletzt(), pfad)
        self._daten.setValue("zuletzt", list(neu))
        self._daten.sync()
        return neu

    def letzter_ordner(self) -> str:
        """Zuletzt benutzter Ordner des Öffnen-Dialogs (leer = keiner)."""
        return str(self._daten.value("letzter_ordner", ""))

    def merke_ordner(self, ordner: str) -> None:
        """Merkt den Ordner des Öffnen-Dialogs."""
        self._daten.setValue("letzter_ordner", ordner)
        self._daten.sync()
