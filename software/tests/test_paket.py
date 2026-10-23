"""Rauchtest des (noch leeren) Hauptpakets."""

import ldv_automation


def test_version_ist_gesetzt() -> None:
    assert ldv_automation.__version__ == "0.1.0"
