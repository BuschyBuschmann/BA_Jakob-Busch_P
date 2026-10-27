"""Qt-freie Anzeigelogik der Oberfläche (Brief P3, Abschnitt 8): läuft im Standardlauf.

Je Test ist das UI-Kriterium genannt, dessen Logik geprüft wird; das Zusammenspiel mit den
Widgets prüfen die Tests mit Marker ``gui``.
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

import pytest
from gui_hilfen import Z, bild, eintrag, fortschritt, zusammenfassung

from ldv_automation.ablauf.steuerung import DurchgangErgebnis
from ldv_automation.domaene import KATALOG, Parameterkatalog, ParameterSpec
from ldv_automation.gui import anzeige as a
from ldv_automation.gui import tokens
from ldv_automation.sitzung import Betriebsart, SitzungsEreignis, Voraussetzung

# --- UI-9: Aktivierungstabelle 3.3 ------------------------------------------------------------

# Zustand -> (Start, Pause aktiv, Pause-Beschriftung, Abbrechen, Anlegen, Laden, Betriebsart)
TABELLE_3_3 = {
    Z.BEREIT: (True, False, "Pausieren (F6)", False, True, True, True),
    Z.LAEUFT: (False, True, "Pausieren (F6)", True, True, False, False),
    Z.PAUSE_ANGEFORDERT: (False, False, "Pause angefordert", True, True, False, False),
    Z.PAUSIERT: (False, True, "Fortsetzen (F6)", True, True, False, False),
    Z.WARTET_AUF_BESTAETIGUNG: (False, False, "Pausieren (F6)", True, True, False, False),
    Z.WARTET_AUF_ENTSCHEIDUNG: (False, False, "Pausieren (F6)", True, True, False, False),
    Z.ABBRUCH_LAEUFT: (False, False, "Pausieren (F6)", False, False, False, False),
    Z.GERAET_UNKLAR: (False, False, "Pausieren (F6)", False, False, False, False),
    Z.BEENDET: (True, False, "Pausieren (F6)", False, True, True, True),
}


@pytest.mark.parametrize("zustand", list(Z))
def test_ui_9_aktivierung_je_durchgangszustand(zustand: Z) -> None:
    b = bild(durchgang=zustand, eintraege=[eintrag()])
    k = a.bedienbarkeit(b, None)
    start, pause, pause_text, abbrechen, anlegen, laden, betriebsart = TABELLE_3_3[zustand]
    assert k["start"].aktiv is start
    assert k["pause"].aktiv is pause
    assert k["pause"].text == pause_text
    assert k["abbrechen"].aktiv is abbrechen
    assert k["messung_neu"].aktiv is anlegen
    assert k["pausenpunkt_neu"].aktiv is anlegen
    assert k["laden"].aktiv is laden
    assert k["speichern"].aktiv is True
    assert k["betriebsart"].aktiv is betriebsart
    for name in ("start", "pause", "abbrechen", "messung_neu", "laden", "betriebsart"):
        if not k[name].aktiv:
            assert k[name].grund, f"{name} ohne Grund im Zustand {zustand}"


def test_ui_9_verbinden_und_trennen() -> None:
    k = a.bedienbarkeit(bild(durchgang=Z.GERAET_UNKLAR), None)
    assert k["verbinden"] == a.Knopf(True, "", "Trennen")
    k = a.bedienbarkeit(bild(betriebsart=Betriebsart.NUR_LESEN, verbindung=None), None)
    assert k["verbinden"].aktiv and k["verbinden"].text == "Verbinden"
    k = a.bedienbarkeit(bild(betriebsart=Betriebsart.NUR_LESEN), None)
    assert k["verbinden"].text == "Trennen"
    k = a.bedienbarkeit(bild(betriebsart=Betriebsart.NUR_LESEN, durchgang=Z.LAEUFT), None)
    assert not k["verbinden"].aktiv
    k = a.bedienbarkeit(bild(), None)
    assert not k["verbinden"].aktiv and "SIMULATOR" in k["verbinden"].grund
    assert not a.bedienbarkeit(bild(durchgang=Z.LAEUFT), None)["einstellungen"].aktiv


@pytest.mark.parametrize(
    ("felder", "grund"),
    [
        ({"betriebsart": Betriebsart.NUR_LESEN}, "NUR LESEN führt keine Einträge aus"),
        ({"eintraege": []}, "keine wartende Messung"),
        ({"eintraege": [eintrag("pausenpunkt")]}, "keine wartende Messung"),
        ({"verbindung": None}, "Simulator nicht verbunden"),
        (
            {"verbindung": None, "betriebsart": Betriebsart.TROCKENLAUF},
            "keine Verbindung zur PSV",
        ),
        ({"messdaten_wurzel": None}, "kein Messdaten-Ordner"),
        ({"durchgang": Z.ABBRUCH_LAEUFT}, "Abbruchs"),
        ({"durchgang": Z.GERAET_UNKLAR}, "Gerätezustand unklar"),
    ],
)
def test_ui_1_start_deaktiviert_mit_grund(felder: dict[str, object], grund: str) -> None:
    werte: dict[str, object] = {"eintraege": [eintrag()]}
    werte.update(felder)
    k = a.bedienbarkeit(bild(**werte), None)["start"]
    assert not k.aktiv
    assert grund in k.grund
    assert k.grund.startswith("Start nicht möglich")


@pytest.mark.parametrize(
    ("zustand", "grund"),
    [
        ("laeuft", "läuft bereits"),
        ("fertig", "fertig"),
        ("fehler", "Fehler"),
        ("abgebrochen", "abgebrochen"),
    ],
)
def test_ui_3_nicht_wartende_eintraege_gesperrt(zustand: str, grund: str) -> None:
    e = eintrag(zustand=zustand)
    k = a.bedienbarkeit(bild(eintraege=[e, eintrag()]), e.id)
    for name in ("entfernen", "hoch", "runter", "uebernehmen"):
        assert not k[name].aktiv
        assert grund in k[name].grund


def test_ui_3_pausenpunkt_zustaende_gesperrt() -> None:
    for zustand, grund in (("erreicht", "erreicht"), ("erledigt", "bestätigt")):
        p = eintrag("pausenpunkt", zustand)
        k = a.bedienbarkeit(bild(eintraege=[p]), p.id)
        assert not k["entfernen"].aktiv and grund in k["entfernen"].grund


def test_ui_3_hoch_runter_an_den_raendern_des_wartebereichs() -> None:
    fertig = eintrag(zustand="fertig")
    w1, w2, w3 = eintrag(), eintrag("pausenpunkt"), eintrag()
    b = bild(eintraege=[fertig, w1, w2, w3])
    k = a.bedienbarkeit(b, w1.id)
    assert k["entfernen"].aktiv and k["uebernehmen"].aktiv
    assert not k["hoch"].aktiv and "Anfang der wartenden" in k["hoch"].grund
    assert k["runter"].aktiv
    k = a.bedienbarkeit(b, w2.id)
    assert k["hoch"].aktiv and k["runter"].aktiv
    k = a.bedienbarkeit(b, w3.id)
    assert k["hoch"].aktiv
    assert not k["runter"].aktiv and "Ende der Liste" in k["runter"].grund
    k = a.bedienbarkeit(b, None)
    assert not k["entfernen"].aktiv and "Kein Eintrag gewählt" in k["entfernen"].grund
    k = a.bedienbarkeit(bild(durchgang=Z.ABBRUCH_LAEUFT, eintraege=[w1]), w1.id)
    assert not k["entfernen"].aktiv


def test_ui_3_wartender_eintrag_vor_gestartetem_ist_nicht_verschiebbar() -> None:
    # Entsteht z. B., wenn ein Eintrag vor einer Wiederholung steht; Verschieben nach unten
    # in den gestarteten Bereich ist gesperrt.
    w, f = eintrag(), eintrag(zustand="fertig")
    k = a.bedienbarkeit(bild(eintraege=[w, f]), w.id)
    assert not k["hoch"].aktiv and not k["runter"].aktiv


# --- Einfügeposition -----------------------------------------------------------------------


def test_ui_2_einfuegeposition_hinter_auswahl_ohne_auswahl_am_ende() -> None:
    e = [eintrag(), eintrag(), eintrag()]
    assert a.einfuegeposition(e, None) == 3
    assert a.einfuegeposition(e, 0) == 1
    assert a.einfuegeposition([], None) == 0
    gestartet = [eintrag(zustand="fertig"), eintrag(zustand="laeuft"), eintrag()]
    assert a.einfuegeposition(gestartet, 0) == 2
    assert a.wartebereich_anfang(gestartet) == 2


def test_ui_2_einfuegeort_text() -> None:
    m1, p, m2 = eintrag(), eintrag("pausenpunkt", text="Umbau"), eintrag()
    e = [m1, p, m2]
    assert a.einfuegeort_text(e, 1) == "wird eingefügt nach Nr 01 (vorl.)"
    gestartet = [eintrag(zustand="fertig", nummer=4), p, m2]
    assert a.einfuegeort_text(gestartet, 1) == "wird eingefügt nach Nr 04"
    assert a.einfuegeort_text(e, 2) == "wird eingefügt nach dem Pausenpunkt „Umbau“"
    assert a.einfuegeort_text(e, 0) == "wird eingefügt am Anfang"
    assert a.einfuegeort_text(e, 3) == "wird eingefügt am Ende"
    assert a.einfuegeort_text([], 0) == "wird eingefügt am Anfang"


# --- UI-7: Zeilenstatus 3.4 ----------------------------------------------------------------


@pytest.mark.parametrize(
    ("art", "zustand", "felder", "text", "stil"),
    [
        ("messung", "wartend", {}, "○ wartend", "normal"),
        ("messung", "wartend", {"versuch": 2}, "○ wartend (Versuch 2)", "normal"),
        ("messung", "laeuft", {}, "▶ läuft", "laeuft"),
        ("messung", "fertig", {}, "✔ fertig", "ok"),
        ("messung", "fertig", {"trockenlauf": True}, "✔ fertig (Trockenlauf)", "ok"),
        ("messung", "fehler", {}, "✖ Fehler", "fehler"),
        ("messung", "fehler", {"uebersprungen": True}, "✖ Fehler (übersprungen)", "fehler"),
        ("messung", "abgebrochen", {}, "■ abgebrochen", "normal"),
        ("pausenpunkt", "wartend", {}, "⏸ Pausenpunkt", "normal"),
        ("pausenpunkt", "erreicht", {}, "⏸ wartet auf Bestätigung", "warn"),
        ("pausenpunkt", "erledigt", {}, "✔ bestätigt", "normal"),
    ],
)
def test_ui_7_zeilenstatus_symbol_und_wort(
    art: str, zustand: str, felder: dict[str, Any], text: str, stil: str
) -> None:
    s = a.zeilenstatus(eintrag(art, zustand, **felder))
    assert s == a.ZeilenStatus(text, stil)


def test_ui_7_unbekannter_zustand_ist_ein_lauter_fehler() -> None:
    with pytest.raises(ValueError, match="Unbekannter Zustand"):
        a.zeilenstatus(eintrag(zustand="kaputt"))
    with pytest.raises(ValueError, match="Unbekannter Zustand"):
        a.zeilenstatus(eintrag("pausenpunkt", "kaputt"))


def test_ui_7_ascii_rueckfall_ueber_eine_tabelle(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(tokens, "ASCII_RUECKFALL", True)
    assert a.zeilenstatus(eintrag()).text == "[ ] wartend"
    assert set(tokens.SYMBOLE_ASCII) == set(tokens.SYMBOLE_UNICODE)


# --- Tabellenzeilen ------------------------------------------------------------------------


def test_zeilen_nr_pausenpunkt_set_fehlt_und_aenderungen() -> None:
    m1 = eintrag(parameter={"mittelung.anzahl": 10, "fft.linien": 1600}, zeitlimit_s=600.0)
    p = eintrag("pausenpunkt", text="Umbau")
    m2 = eintrag(einstellungsdatei="C:\\psv\\fehlt.set", set_fehlt=True, zustand="laeuft", nummer=1)
    z = a.zeilen(bild(durchgang=Z.LAEUFT, eintraege=[m1, p, m2]))
    # m1 wartet: vorläufig nach der laufenden Nummer 01 gezählt; m2 trägt die Dateinummer.
    assert [x.nr for x in z] == ["(02)", "–", "01"]
    assert [x.nr_vorlaeufig for x in z] == [True, False, False]
    assert z[0].aenderungen == "Mittelung Anzahl 10, FFT Linien 1600"
    assert "mittelung.anzahl" in z[0].aenderungen_tooltip
    assert z[0].limit == "600 s" and z[2].limit == "Std."
    assert z[1].name == "Pausenpunkt: Umbau" and z[1].pausenpunkt
    assert z[2].einstellungsdatei == "⚠ fehlt.set"
    assert z[2].einstellungsdatei_tooltip.startswith("Einstellungsdatei nicht gefunden")
    assert z[2].laeuft and not z[0].laeuft


def test_aenderungen_kurzform_aus_dem_katalog() -> None:
    assert a.aenderungen_text({}) == ("–", "Keine Änderungen gegenüber der Einstellungsdatei.")
    kurz, voll = a.aenderungen_text({"fft.bandbreite_hz": 1000.0})
    assert kurz == "FFT Bandbreite 1000 Hz"
    assert voll == "FFT Bandbreite: 1000 Hz (fft.bandbreite_hz)"
    kurz, _ = a.aenderungen_text({"unbekannt.x": 3}, Parameterkatalog())
    assert kurz == "unbekannt.x 3"


def test_parameter_bezeichnung() -> None:
    namen = [a.parameter_bezeichnung(s) for s in KATALOG]
    assert namen == ["FFT Bandbreite", "FFT Linien", "Mittelung Anzahl", "Mittelung Typ"]
    ohne_gruppe = ParameterSpec(schluessel="dauer_s", typ="float", einheit="s", com_gruppe="x")
    assert a.parameter_bezeichnung(ohne_gruppe) == "Dauer"


# --- UI-5: Eingabeprüfung ------------------------------------------------------------------


def test_ui_5_mittelung_2_liegt_ausserhalb() -> None:
    spec = KATALOG.spec("mittelung.anzahl")
    wert, fehler = a.lies_parameter(spec, "2")
    assert wert is None
    assert fehler == "✖ Mittelung Anzahl: 2 liegt außerhalb 3 … 10000."
    assert a.lies_parameter(spec, "10") == (10, None)


@pytest.mark.parametrize(
    ("schluessel", "text", "erwartet", "meldung"),
    [
        ("fft.bandbreite_hz", "1000,5", 1000.5, None),
        ("fft.bandbreite_hz", "1e3", 1000.0, None),
        ("fft.bandbreite_hz", "0", None, "liegt außerhalb > 0 Hz"),
        ("fft.bandbreite_hz", "abc", None, "Zahl erwartet"),
        ("fft.bandbreite_hz", "inf", None, "endlich"),
        ("fft.linien", "1.5", None, "Ganzzahl erwartet"),
        ("fft.linien", " ", None, "Wert fehlt"),
        ("mittelung.typ", "Complex", "Complex", None),
        ("mittelung.typ", "Quatsch", None, "liegt außerhalb"),
    ],
)
def test_ui_5_parameterpruefung(
    schluessel: str, text: str, erwartet: object, meldung: str | None
) -> None:
    wert, fehler = a.lies_parameter(KATALOG.spec(schluessel), text)
    assert wert == erwartet
    if meldung is None:
        assert fehler is None
    else:
        assert fehler is not None and meldung in fehler


@pytest.mark.parametrize(
    ("name", "teil"),
    [
        ("", "Pflichtfeld"),
        ("   ", "Pflichtfeld"),
        (" Platte", "Leerzeichen"),
        ("Platte ", "Leerzeichen"),
        ("a/b", "unzulässige Zeichen /"),
        ('a"b|c', 'unzulässige Zeichen " |'),
    ],
)
def test_ui_5_namenspruefung(name: str, teil: str) -> None:
    fehler = a.pruefe_name(name)
    assert fehler is not None and teil in fehler


def test_ui_5_gueltiger_name_und_pflichttext() -> None:
    assert a.pruefe_name("Platte_Mitte 2") is None
    assert a.pruefe_pflichttext("Text", "") == "✖ Text: Pflichtfeld."
    assert a.pruefe_pflichttext("Text", "x") is None


def test_zieldatei_text() -> None:
    assert a.zieldatei_text(None, "M1").startswith("Zieldatei: NN_M1.svd")
    assert a.zieldatei_text(None, "").startswith("Zieldatei: NN_<Name>.svd")
    e = eintrag(messdatei="D:/daten/01_M1.svd")
    assert a.zieldatei_text(e, "M1") == "Zieldatei: D:/daten/01_M1.svd"


# --- Statuszeile ---------------------------------------------------------------------------


def test_ui_14_fenstertitel_und_betriebsart_wort() -> None:
    assert a.fenstertitel(bild(betriebsart=Betriebsart.MESSEN)) == "LDV-Warteschlange – MESSEN"
    assert a.BETRIEBSART_WORT[Betriebsart.NUR_LESEN] == "NUR LESEN"
    assert set(a.BETRIEBSART_TOOLTIP) == set(Betriebsart)


def test_durchgang_text() -> None:
    m1, m2 = eintrag(zustand="fertig", nummer=1), eintrag(zustand="laeuft", nummer=2)
    e = [m1, eintrag("pausenpunkt"), m2, eintrag()]
    assert a.durchgang_text(bild(durchgang=Z.LAEUFT, eintraege=e)) == "Läuft · Messung 02 von 03"
    assert (
        a.durchgang_text(bild(durchgang=Z.PAUSE_ANGEFORDERT, eintraege=e))
        == "Pause angefordert · Messung 02 läuft zu Ende"
    )
    assert a.durchgang_text(bild(durchgang=Z.LAEUFT)) == "Läuft"
    assert a.durchgang_text(bild(durchgang=Z.PAUSE_ANGEFORDERT)) == "Pause angefordert"
    beendet = bild(durchgang=Z.BEENDET, ergebnis=DurchgangErgebnis.VOLLSTAENDIG)
    assert a.durchgang_text(beendet) == "Beendet (vollständig)"
    beendet = bild(durchgang=Z.BEENDET, ergebnis=DurchgangErgebnis.ABGEBROCHEN)
    assert a.durchgang_text(beendet) == "Beendet (abgebrochen)"
    beendet = bild(durchgang=Z.BEENDET, ergebnis=DurchgangErgebnis.GERAET_UNKLAR)
    assert "unklar" in a.durchgang_text(beendet)
    for z in (Z.BEREIT, Z.PAUSIERT, Z.WARTET_AUF_BESTAETIGUNG, Z.GERAET_UNKLAR):
        assert a.durchgang_text(bild(durchgang=z))
    assert a.durchgang_text(bild(durchgang=Z.ABBRUCH_LAEUFT)) == "Abbruch läuft …"
    assert all(a.durchgang_text_kurz(z) for z in Z)


def test_verbindung_text() -> None:
    assert a.verbindung_text(bild()) == "Simulator aktiv"
    assert a.verbindung_text(bild(verbindung=None)) == "Simulator nicht verbunden"
    nur = bild(betriebsart=Betriebsart.NUR_LESEN)
    assert a.verbindung_text(nur) == "PSV 10.x-SIM verbunden · Gerät: gestoppt"
    nur = bild(betriebsart=Betriebsart.NUR_LESEN, verbindung=None)
    assert a.verbindung_text(nur) == "PSV nicht verbunden"


# --- Hinweisband 3.5 -----------------------------------------------------------------------


def test_ui_17_geraet_unklar_hat_vorrang() -> None:
    b = bild(
        durchgang=Z.GERAET_UNKLAR,
        waechter_s=45.0,
        durchgangsordner="/x",
    )
    h = a.hinweis(b)
    assert h is not None and h.fall == "1" and h.alarm
    assert h.text.startswith("✖ Gerätezustand unklar.")
    assert [k.schluessel for k in h.knoepfe] == ["trennen"]
    assert h.knoepfe[0].text == "Verbindung trennen"


def test_ui_16_waechter_hat_vorrang_vor_entscheidung() -> None:
    b = bild(durchgang=Z.WARTET_AUF_ENTSCHEIDUNG, waechter_s=45.4)
    h = a.hinweis(b)
    assert h is not None and h.fall == "3"
    assert h.text == "⚠ PSV reagiert nicht seit 45 s. Bitte am Gerät prüfen (Dialog in der PSV?)."
    assert a.hinweis(bild(durchgang=Z.ABBRUCH_LAEUFT, waechter_s=9.0)).fall == "2"  # type: ignore[union-attr]


def test_ui_12_fehlerentscheidung() -> None:
    m1 = eintrag(zustand="fertig", nummer=1)
    m2 = eintrag(zustand="fehler", name="Platte_Mitte", nummer=2)
    b = bild(
        durchgang=Z.WARTET_AUF_ENTSCHEIDUNG,
        eintraege=[m1, m2],
        fehler_eintrag_id=m2.id,
        fehlertext="Zeitlimit überschritten",
    )
    h = a.hinweis(b)
    assert h is not None and h.fall == "4" and h.alarm and h.stil == "fehler"
    assert h.text == (
        "✖ Messung 02 „Platte_Mitte“ fehlgeschlagen: Zeitlimit überschritten. "
        "Vorläufiges Verhalten (O1): Durchgang angehalten."
    )
    assert [k.schluessel for k in h.knoepfe] == ["wiederholen", "ueberspringen", "abbrechen"]
    assert not any(k.primaer for k in h.knoepfe)
    ohne = a.hinweis(bild(durchgang=Z.WARTET_AUF_ENTSCHEIDUNG))
    assert ohne is not None and "Messung fehlgeschlagen: unbekannter Fehler" in ohne.text


def test_ui_11_pausenpunkt() -> None:
    p = eintrag("pausenpunkt", "erreicht", text="Sensorkopf umsetzen")
    h = a.hinweis(bild(durchgang=Z.WARTET_AUF_BESTAETIGUNG, eintraege=[p], pausenpunkt_id=p.id))
    assert h is not None and h.fall == "5" and h.alarm and h.stil == "warn_rand"
    assert h.text == (
        "⏸ Pausenpunkt erreicht: Sensorkopf umsetzen. "
        "Die nächste Messung startet erst nach Bestätigung."
    )
    assert h.knoepfe == (a.BandKnopf("bestaetigen", "Bestätigen (F7)", primaer=True),)


def test_ui_13_pause_texte() -> None:
    m1, m2 = eintrag(zustand="fertig", nummer=1), eintrag(zustand="laeuft", nummer=2)
    m3 = eintrag(name="Platte_Rand")
    h = a.hinweis(bild(durchgang=Z.PAUSE_ANGEFORDERT, eintraege=[m1, m2, m3]))
    assert h is not None and h.fall == "6a"
    assert h.text == "⏸ Pause angefordert. Messung 02 läuft zu Ende, danach startet keine neue."
    assert not h.knoepfe
    m2f = eintrag(zustand="fertig", nummer=2)
    h = a.hinweis(bild(durchgang=Z.PAUSIERT, eintraege=[m1, m2f, m3]))
    assert h is not None and h.fall == "6b"
    # Vorläufig: ohne Messdatei im Durchgangsordner zählen m1/m2f nicht zum Durchgang.
    assert h.text == "⏸ Durchgang pausiert. Nächste wartende Messung: Nr 01 (vorl.) „Platte_Rand“."
    m2d = eintrag(zustand="fertig", nummer=2, messdatei="/d/lauf1/02_M.svd")
    h = a.hinweis(bild(durchgang=Z.PAUSIERT, durchgangsordner="/d/lauf1", eintraege=[m1, m2d, m3]))
    assert h is not None
    assert h.text == "⏸ Durchgang pausiert. Nächste wartende Messung: Nr 03 (vorl.) „Platte_Rand“."
    assert [k.schluessel for k in h.knoepfe] == ["fortsetzen"]
    h = a.hinweis(bild(durchgang=Z.PAUSIERT))
    assert h is not None and "Keine wartende Messung mehr." in h.text
    h = a.hinweis(bild(durchgang=Z.PAUSE_ANGEFORDERT))
    assert h is not None and "Die laufende Messung läuft zu Ende" in h.text


def test_ui_18_zusammenfassung() -> None:
    voll = bild(
        durchgang=Z.BEENDET,
        ergebnis=DurchgangErgebnis.VOLLSTAENDIG,
        zusammenfassung=zusammenfassung(fertig=5),
        durchgangsordner="/daten/d1",
    )
    h = a.hinweis(voll)
    assert h is not None and h.fall == "7" and not h.alarm
    assert h.text == "✔ Durchgang beendet: 5 fertig."
    assert [k.schluessel for k in h.knoepfe] == ["ordner", "schliessen"]
    assert a.hinweis(voll, beendet_quittiert=True) is not None  # dann Fall 8 (Simulator)
    assert a.hinweis(voll, beendet_quittiert=True).fall == "8"  # type: ignore[union-attr]
    gemischt = bild(
        durchgang=Z.BEENDET,
        ergebnis=DurchgangErgebnis.VOLLSTAENDIG,
        zusammenfassung=zusammenfassung(fertig=3, fehler=2, uebersprungen=1),
    )
    assert (
        a.zusammenfassung_text(gemischt)
        == "✔ Durchgang beendet: 3 fertig, 1 Fehler, 1 übersprungen."
    )
    abgebrochen = bild(
        durchgang=Z.BEENDET,
        ergebnis=DurchgangErgebnis.ABGEBROCHEN,
        zusammenfassung=zusammenfassung(fertig=1, abgebrochen=1, wartend=3),
    )
    assert a.zusammenfassung_text(abgebrochen) == (
        "■ Durchgang abgebrochen: 1 fertig, 1 abgebrochen, 3 nicht gestartet (bleiben wartend)."
    )
    unklar = bild(durchgang=Z.BEENDET, ergebnis=DurchgangErgebnis.GERAET_UNKLAR)
    assert (
        a.zusammenfassung_text(unklar)
        == "✖ Durchgang beendet (Gerätezustand unklar): keine Messung."
    )
    ohne_ordner = a.hinweis(bild(durchgang=Z.BEENDET, ergebnis=DurchgangErgebnis.VOLLSTAENDIG))
    assert ohne_ordner is not None and [k.schluessel for k in ohne_ordner.knoepfe] == ["schliessen"]


def test_ui_1_betriebsart_hinweis_und_leer() -> None:
    assert a.hinweis(bild()).fall == "8"  # type: ignore[union-attr]
    h = a.hinweis(bild(betriebsart=Betriebsart.TROCKENLAUF))
    assert h is not None and h.text.startswith("Trockenlauf: Es wird nicht gescannt.")
    assert a.hinweis(bild(betriebsart=Betriebsart.NUR_LESEN)) is None
    assert a.hinweis(bild(betriebsart=Betriebsart.MESSEN)) is None
    assert a.hinweis(bild(durchgang=Z.LAEUFT)) is None


# --- UI-8: Fortschritt 3.6 -----------------------------------------------------------------


def test_ui_8_fortschritt_geschaetzt() -> None:
    m = eintrag(zustand="laeuft", nummer=1)
    b = bild(durchgang=Z.LAEUFT, eintraege=[m], fortschritt=fortschritt(m.id, 0.4))
    f = a.fortschritt_anzeige(b)
    assert f == a.FortschrittAnzeige(
        "Messung 01:", 40, False, "ca. 40 % (geschätzt) · noch ca. 2 min · Zeitlimit in 7:41", True
    )


def test_ui_8_fortschritt_varianten() -> None:
    m = eintrag(zustand="laeuft")

    def mit(f: object, z: Z = Z.LAEUFT) -> a.FortschrittAnzeige:
        return a.fortschritt_anzeige(bild(durchgang=z, eintraege=[m], fortschritt=f))

    ueber = mit(fortschritt(m.id, 1.3, zeitlimit_rest_s=130.0))
    assert ueber.wert == 99
    assert ueber.text == "Schätzung überschritten – Messung läuft noch · Zeitlimit in 2:10"
    unbekannt = mit(fortschritt(m.id, None, zeitlimit_rest_s=3725.0))
    assert unbekannt.unbestimmt and unbekannt.text == "Fortschritt unbekannt · Zeitlimit in 1:02:05"
    ereignisse = mit(
        fortschritt(m.id, 4 / 9, geschaetzt=False, quelle="ereignisse", restzeit_s=None)
    )
    assert ereignisse.wert == 44 and "geschätzt" not in ereignisse.text
    assert "ereignisse" in ereignisse.text
    vorbereitung = mit(None)
    assert vorbereitung.unbestimmt and vorbereitung.text == "Messung wird vorbereitet."
    assert mit(None, Z.BEREIT) == a.FortschrittAnzeige("", 0, False, "Kein Durchgang läuft.", False)
    pause = mit(None, Z.PAUSIERT)
    assert pause.text == "Zwischen den Messungen." and pause.wert is None and not pause.aktiv
    assert mit(None, Z.GERAET_UNKLAR).text == "Gerätezustand unklar."


def test_ui_8_messung_fertig_zwischen_den_messungen() -> None:
    t0 = datetime(2026, 11, 2, 10, 0, tzinfo=UTC)
    t1 = datetime(2026, 11, 2, 10, 5, tzinfo=UTC)
    m1 = eintrag(zustand="fertig", zeit_ende=t0, nummer=1)
    m2 = eintrag(zustand="fertig", zeit_ende=t1, nummer=2)
    f = a.fortschritt_anzeige(bild(durchgang=Z.LAEUFT, eintraege=[m1, m2, eintrag()]))
    assert f == a.FortschrittAnzeige("Messung 02:", 100, False, "Messung 02 fertig.", True)
    f = a.fortschritt_anzeige(bild(durchgang=Z.LAEUFT, eintraege=[eintrag()]))
    assert f.text == "Zwischen den Messungen."


def test_dauer_und_uhr_text() -> None:
    assert a.dauer_text(45.4) == "45 s"
    assert a.dauer_text(-3) == "0 s"
    assert a.dauer_text(120) == "2 min"
    assert a.dauer_text(7200) == "2,0 h"
    assert a.uhr_text(461) == "7:41"
    assert a.uhr_text(-5) == "0:00"
    assert a.uhr_text(float("nan")) == "0:00"


# --- Dialoge, Schließen, Protokoll ---------------------------------------------------------


def test_ui_10_abbruchtext_je_lage() -> None:
    m = eintrag(zustand="laeuft")
    assert a.abbruch_laeuft_messung(bild(durchgang=Z.LAEUFT, eintraege=[m]))
    assert not a.abbruch_laeuft_messung(bild(durchgang=Z.PAUSIERT, eintraege=[m]))
    assert not a.abbruch_laeuft_messung(bild(durchgang=Z.LAEUFT))


def test_ui_26_schliessen_entscheidung() -> None:
    for z in (Z.LAEUFT, Z.PAUSE_ANGEFORDERT, Z.ABBRUCH_LAEUFT):
        assert a.schliessen_entscheidung(bild(durchgang=z), ungespeichert=True) == "sperren"
    assert (
        a.schliessen_entscheidung(bild(durchgang=Z.GERAET_UNKLAR), ungespeichert=False) == "unklar"
    )
    voll = bild(eintraege=[eintrag()])
    assert a.schliessen_entscheidung(voll, ungespeichert=True) == "fragen"
    assert a.schliessen_entscheidung(voll, ungespeichert=False) == "frei"
    assert a.schliessen_entscheidung(bild(), ungespeichert=True) == "frei"


def test_ui_15_start_dialog_je_betriebsart() -> None:
    assert a.start_dialog(bild(betriebsart=Betriebsart.MESSEN)) == "messen"
    assert a.start_dialog(bild(betriebsart=Betriebsart.TROCKENLAUF)) == "trockenlauf"
    assert a.start_dialog(bild()) == "keiner"


def test_definitionen_ignorieren_laufzustand() -> None:
    m = eintrag()
    b1 = bild(eintraege=[m])
    b2 = bild(eintraege=[eintrag(id=m.id, zustand="fertig", messdatei="x")])
    assert a.definitionen(b1) == a.definitionen(b2)
    b3 = bild(eintraege=[eintrag(id=m.id, name="anders")])
    assert a.definitionen(b1) != a.definitionen(b3)


def test_ui_14_voraussetzung_zeilen_aus_der_sitzung() -> None:
    v = [
        Voraussetzung(name="verbindung", erfuellt=True, text="Verbindung steht"),
        Voraussetzung(name="geraet_gestoppt", erfuellt=False, text="PSV gestoppt"),
        Voraussetzung(name="meldungen_unterdrueckt", erfuellt=True, text="Suppress"),
        Voraussetzung(name="git_hash", erfuellt=True, text="Git"),
        Voraussetzung(name="messdaten_wurzel", erfuellt=False, text="Wurzel fehlt"),
        Voraussetzung(name="neu", erfuellt=False, text="Neue Bedingung"),
    ]
    z = a.voraussetzung_zeilen(v)
    assert [x.text for x in z][:5] == [
        "Verbindung steht, Gerät gestoppt",
        "Meldungen unterdrückt (Suppress)",
        "Git-Hash bekannt",
        "Messdaten-Ordner gesetzt und beschreibbar",
        "Trockenlauf des ersten Eintrags ohne Abweichung in dieser Sitzung",
    ]
    assert [x.erfuellt for x in z] == [False, True, True, False, False, False]
    assert z[0].detail == "Verbindung steht; PSV gestoppt"
    assert z[3].abhilfe == "In den Einstellungen setzen."
    assert z[4].detail == "Keine Angabe der Sitzung" and not z[4].erfuellt
    assert z[5].text == "Neue Bedingung"
    assert z[1].abhilfe == ""


def test_protokolltext() -> None:
    def ev(art: str, text: str = "t") -> SitzungsEreignis:
        return SitzungsEreignis(revision=1, art=art, text=text)

    assert a.protokolltext(ev("fehler", "kaputt")) == "Fehler: kaputt"
    assert a.protokolltext(ev("waechter", "PSV reagiert nicht")) == "Warnung: PSV reagiert nicht"
    assert a.protokolltext(ev("durchgang_zustand", "x")) == "x"
    assert a.protokolltext(ev("warteschlange_gespeichert")) is None
    assert a.protokolltext(ev("warteschlange_geladen")) is None


# --- UI-23: Kontrast -----------------------------------------------------------------------


@pytest.mark.parametrize(("name", "vorder", "hinter"), tokens.KONTRAST_PAARE)
def test_ui_23_kontrast_mindestens_4_5(name: str, vorder: str, hinter: str) -> None:
    assert tokens.kontrastverhaeltnis(vorder, hinter) >= tokens.KONTRAST_MINDEST_TEXT, name


def test_ui_23_kontrast_referenzwerte() -> None:
    # Analytisch: Schwarz/Weiß = 21:1, gleiche Farbe = 1:1 (WCAG 2.x). Toleranz rel 1e-12:
    # reine Gleitkomma-Rundung der Formel.
    assert tokens.kontrastverhaeltnis("#000000", "#FFFFFF") == pytest.approx(21.0, rel=1e-12)
    assert tokens.kontrastverhaeltnis("#777777", "#777777") == pytest.approx(1.0, rel=1e-12)
    assert tokens.kontrastverhaeltnis("#FFFFFF", "#000000") == pytest.approx(21.0, rel=1e-12)
    for falsch in ("FFFFFF", "#FFF", "#GGGGGG"):
        with pytest.raises(ValueError, match="#RRGGBB"):
            tokens.relative_leuchtdichte(falsch)


def test_ui_5_neuer_katalogeintrag_ohne_gui_aenderung() -> None:
    katalog = Parameterkatalog(KATALOG)
    katalog.registrieren(
        ParameterSpec(
            schluessel="trigger.pegel_v",
            typ="float",
            einheit="V",
            com_gruppe="trigger",
            minimum=-10,
            maximum=10,
        )
    )
    kurz, _ = a.aenderungen_text({"trigger.pegel_v": 1.5}, katalog)
    assert kurz == "Trigger Pegel 1.5 V"


# --- UI-29/UI-30: Zurücksetzen (Nachtrag 2026-10-27) ----------------------------------------


@pytest.mark.parametrize("zustand", list(Z))
def test_ui_29_knopf_genau_wenn_zuruecksetzen_moeglich(zustand: Z) -> None:
    for moeglich in (True, False):
        b = bild(
            durchgang=zustand,
            ergebnis=DurchgangErgebnis.VOLLSTAENDIG,
            zuruecksetzen_moeglich=moeglich,
            eintraege=[eintrag(zustand="fertig")],
        )
        h = a.hinweis(b)
        knoepfe = [k.schluessel for k in h.knoepfe] if h is not None else []
        erwartet = moeglich and zustand in (Z.BEREIT, Z.BEENDET)
        assert ("zuruecksetzen" in knoepfe) is erwartet, (zustand, moeglich)


def test_ui_29_fall_7b_ueber_fall_8_und_fall_7() -> None:
    h = a.hinweis(bild(zuruecksetzen_moeglich=True, betriebsart=Betriebsart.TROCKENLAUF))
    assert h is not None and h.fall == "7b" and h.stil == "neutral"
    assert h.text == (
        "Einträge sind bereits ausgeführt (fertig, Fehler oder abgebrochen). Zum erneuten "
        "Ausführen auf wartend zurücksetzen."
    )
    assert h.knoepfe == (a.ZURUECKSETZEN_KNOPF,)
    assert a.ZURUECKSETZEN_KNOPF.tooltip == (
        "Alle Einträge wieder auf wartend setzen. Messdateien und Protokolle bleiben erhalten."
    )
    b7 = bild(
        durchgang=Z.BEENDET,
        ergebnis=DurchgangErgebnis.VOLLSTAENDIG,
        durchgangsordner="/d",
        zuruecksetzen_moeglich=True,
    )
    h7 = a.hinweis(b7)
    assert h7 is not None and h7.fall == "7"
    assert [k.schluessel for k in h7.knoepfe] == ["zuruecksetzen", "ordner", "schliessen"]
    assert a.hinweis(b7, beendet_quittiert=True).fall == "7b"  # type: ignore[union-attr]


def test_ui_30_rueckfrage_nur_bei_echt_gemessenen() -> None:
    nur_trocken = bild(
        eintraege=[
            eintrag(zustand="fertig", trockenlauf=True),
            eintrag(zustand="fehler"),
            eintrag(),
            eintrag("pausenpunkt", "erledigt"),
        ]
    )
    assert a.echt_gemessen(nur_trocken) == 0
    echt = bild(eintraege=[eintrag(zustand="fertig"), eintrag(zustand="abgebrochen"), eintrag()])
    assert a.echt_gemessen(echt) == 2
    assert a.zuruecksetzen_frage_text(2) == (
        "2 Einträge wurden bereits gemessen. Nach dem Zurücksetzen werden sie beim nächsten "
        "Start erneut gemessen, in einem neuen Durchgangsordner. Vorhandene Messdateien und "
        "Protokolle bleiben unverändert."
    )


# --- K-U4, 1: Nr = Dateinummer ----------------------------------------------------------------


def test_k_u4_nr_endgueltig_und_vorlaeufig() -> None:
    a1 = eintrag(zustand="fertig", nummer=1)
    p = eintrag("pausenpunkt")
    b = eintrag()
    n = a.nummern([a1, p, b])
    assert n[a1.id] == a.Nr(1, True) and n[a1.id].kurz == "01" and n[a1.id].lang == "01"
    assert n[b.id] == a.Nr(1, False)
    assert n[b.id].kurz == "(01)" and n[b.id].lang == "01 (vorl.)"
    lauf = eintrag(zustand="laeuft", nummer=3)
    w1, w2 = eintrag(), eintrag()
    n = a.nummern([lauf, w1, w2], durchgang_aktiv=True)
    assert (n[w1.id].wert, n[w2.id].wert) == (4, 5)
    # Ohne Durchgang: neuer Durchgang zählt ab 01
    n = a.nummern([lauf, w1, w2])
    assert (n[w1.id].wert, n[w2.id].wert) == (1, 2)
    # Im Durchgang ohne laufende Messung: nur Einträge des aktuellen Durchgangsordners zählen
    alt = eintrag(zustand="fertig", nummer=5, messdatei="/d/lauf1/05_A.svd")
    neu = eintrag(zustand="fertig", nummer=1, messdatei="/d/lauf2/01_B.svd")
    n = a.nummern([alt, neu, w1], durchgang_aktiv=True, durchgangsordner="/d/lauf2")
    assert n[w1.id] == a.Nr(2, False)
    n = a.nummern([alt, w1], durchgang_aktiv=True, durchgangsordner="/d/lauf2")
    assert n[w1.id] == a.Nr(1, False)
    n = a.nummern([alt, w1], durchgang_aktiv=True, durchgangsordner=None)
    assert n[w1.id] == a.Nr(1, False)
    # Wartender Eintrag mit Nummer (nach „Wiederholen“) bleibt vorläufig gezählt
    n = a.nummern([eintrag(nummer=7)])
    assert not next(iter(n.values())).endgueltig


def test_k_u4_auswahlfarbe_neutral_und_verschieden_von_aktiv() -> None:
    assert tokens.C_AUSWAHL_BG != tokens.C_AKTIV_BG
    namen = {n for n, _v, _h in tokens.KONTRAST_PAARE}
    assert {"text/auswahl_bg", "akzent/auswahl_bg"} <= namen
    # Gleiche Leuchtdichte wäre nur am Farbton unterscheidbar: Abstand ≥ 1,05:1 verlangt.
    assert tokens.kontrastverhaeltnis(tokens.C_AUSWAHL_BG, tokens.C_AKTIV_BG) >= 1.05


def test_k_u4_geraet_in_geraet_unklar_deaktiviert() -> None:
    k = a.bedienbarkeit(bild(durchgang=Z.GERAET_UNKLAR), None)["geraet"]
    assert not k.aktiv and "Gerätezustand unklar" in k.grund
    assert a.bedienbarkeit(bild(), None)["geraet"].aktiv


def test_k_u4_zuruecksetzen_ereignis_nicht_doppelt_im_protokoll() -> None:
    ev = SitzungsEreignis(revision=1, art="warteschlange_zurueckgesetzt", text="x")
    assert a.protokolltext(ev) is None
