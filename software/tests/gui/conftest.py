"""Einstellungen der Oberflächentests: Qt offscreen (vor dem ersten Erzeugen der QApplication)."""

import os

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
