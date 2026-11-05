"""Einstellungen der Oberflächentests: Qt offscreen (vor dem ersten Erzeugen der QApplication)."""

import os

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")


import pytest


@pytest.fixture(autouse=True)
def _einstellungen_temporaer(request, tmp_path, monkeypatch):  # type: ignore[no-untyped-def]
    """Lenkt die INI-Datei des Reiters „Auswerten“ in ein Temp-Verzeichnis (nie die des Nutzers)."""
    if request.node.get_closest_marker("gui") is None:
        return
    from ldv_automation.gui import einstellungen_auswerten

    monkeypatch.setattr(
        einstellungen_auswerten, "standard_pfad", lambda: str(tmp_path / "auswerten_test.ini")
    )


@pytest.fixture
def baue(qtbot, monkeypatch):  # type: ignore[no-untyped-def]
    """Baut ein ``Hauptfenster`` mit Reiter „Auswerten“ (Aufträge über Attrappen, kein Prozess).

    ``baue(ausfuehrer=None, *, sitzung=None, aktiv=True)`` liefert ``(fenster, protokoll)``;
    ``protokoll`` ersetzt ``lese_job`` und ``pruef_job`` (synthetische Datei, Fehler wählbar),
    ``ausfuehrer`` ist ein ``DirektAusfuehrer``, wenn nichts angegeben ist. Qt-Importe stehen in
    der Fixture, damit der Standardlauf (ohne Qt-Bibliotheken) diese Datei laden kann.
    """
    from gui_ausw_hilfen import DirektAusfuehrer, Protokoll
    from gui_hilfen import AttrappenSitzung, bild
    from PySide6.QtWidgets import QApplication

    from ldv_automation.gui import auswerten_reiter, stil
    from ldv_automation.gui.hauptfenster import Hauptfenster

    stil.wende_an(QApplication.instance())  # type: ignore[arg-type]
    erzeugt = []
    protokoll = Protokoll()
    monkeypatch.setattr(auswerten_reiter, "lese_job", protokoll.lese_job)
    monkeypatch.setattr(auswerten_reiter, "pruef_job", protokoll.pruef_job)
    monkeypatch.setattr(auswerten_reiter, "export_job", protokoll.export_job)

    def bau(ausfuehrer=None, *, sitzung=None, aktiv=True):  # type: ignore[no-untyped-def]
        w = Hauptfenster(
            sitzung or AttrappenSitzung(bild()),
            takt_ms=None,
            ausfuehrer=ausfuehrer if ausfuehrer is not None else DirektAusfuehrer(),
        )
        monkeypatch.setattr(w, "_fuehre_aus", lambda _dialog: 0)  # kein modaler Dialog
        qtbot.addWidget(w)
        w.resize(1366, 768)
        w.show()
        qtbot.waitExposed(w)
        if aktiv:
            w.reiter.setCurrentIndex(1)
            QApplication.processEvents()  # Layout zeigt später angelegte Kinder verzögert
        erzeugt.append(w)
        return w, protokoll

    yield bau
    for w in erzeugt:
        w._timer.stop()
        if w.auswerten is not None:
            w.auswerten.beende()
