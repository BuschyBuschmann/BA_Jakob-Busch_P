"""Export der Auswertung in ein offenes Format (FG-02 Abschnitt 5, B-7).

Format: zwei Dateien mit gemeinsamem Basisnamen

``<basis>.npz``
    Alle Felder als ``float64``/``int64``/``bool`` (NumPy-Archiv, ohne Pickle lesbar).
    Komplexe Größen stehen als getrennte Real- und Imaginärteile (``….re``, ``….im``) in
    ``float64``, ohne Rundung.
``<basis>.json``
    Metadaten in UTF-8: Konventionen, Einheit und Kennzeichen jedes Felds, alle Annahmen
    mit Status (P-11), Plausibilitätsprüfungen, Spitzen, Bandwerte, Schwingform-Kennwerte,
    Herkunft (Pfad und SHA-256 der Messdatei, Git-Hash der Software, Datum) und SHA-256 der
    ``.npz``-Datei.

Pflichtinhalt nach FG-02 Abschnitt 5: Frequenzachse und Linienindex mit Δf und
:math:`k_0`; Punkte (``index``, ``label``, Koordinaten in m, Gültigkeit); Rohgrößen CP, AP,
ABS, CPH ohne Vorzeichen und ohne Konjugation; abgeleitete Größen H1, H2, γ² und die
Spektren nach 3.1 mit angewandten Vorzeichen :math:`s_a s_b` und ``konjugieren``.
"""

from __future__ import annotations

import datetime as dt
import hashlib
import json
import math
import os
import re
from collections.abc import Callable
from dataclasses import asdict
from pathlib import Path
from typing import Any

import numpy as np
import numpy.typing as npt

from ldv_automation.protokoll.version import BuildInfo, ermittle_build_info

from .baender import Bandwert
from .daten import einheit_produkt, einheit_quadrat
from .gesamt import Auswertung
from .plausibilitaet import Pruefergebnis
from .spitzen import Spitzenergebnis

FORMAT = "ldv_automation.auswertung.export"
FORMAT_VERSION = 1

ZEITKONVENTION = "exp(+i*omega*t)"
KREUZSPEKTRUM = "CP_ab = <A B*>, a = Antwort, b = Referenz"


def _schluessel(name: str) -> str:
    """Kanalname als Teil eines Feldnamens (Leerzeichen → ``_``)."""
    return re.sub(r"[^0-9A-Za-z]+", "_", name).strip("_")


def paar_schluessel(antwort: str, referenz: str) -> str:
    """Feldnamensteil eines Paars, z. B. ``"Vib_Z__Ref1"``."""
    return f"{_schluessel(antwort)}__{_schluessel(referenz)}"


def sha256_datei(pfad: Path) -> str:
    """SHA-256 einer Datei (nur lesend, blockweise)."""
    h = hashlib.sha256()
    with pfad.open("rb") as datei:
        for block in iter(lambda: datei.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def _json_wert(wert: Any) -> Any:
    """Wandelt Werte JSON-tauglich (NaN/∞ → ``None`` bzw. Text, NumPy → Python)."""
    if isinstance(wert, dict):
        return {str(k): _json_wert(v) for k, v in wert.items()}
    if isinstance(wert, list | tuple):
        return [_json_wert(v) for v in wert]
    if isinstance(wert, np.ndarray):
        return _json_wert(wert.tolist())
    if isinstance(wert, np.generic):
        return _json_wert(wert.item())
    if isinstance(wert, float):
        if math.isnan(wert):
            return None
        if math.isinf(wert):
            return "inf" if wert > 0 else "-inf"
    return wert


class _Sammler:
    """Sammelt Felder und ihre Beschreibung."""

    def __init__(self) -> None:
        self.felder: dict[str, npt.NDArray[Any]] = {}
        self.katalog: dict[str, dict[str, Any]] = {}

    def reell(self, name: str, wert: npt.ArrayLike, **beschreibung: Any) -> None:
        feld = np.asarray(wert)
        if feld.dtype.kind == "f":
            feld = feld.astype(np.float64)
        if name in self.felder:
            raise ValueError(f"Feld {name!r} doppelt")
        self.felder[name] = feld
        self.katalog[name] = {"form": list(feld.shape), "dtype": str(feld.dtype), **beschreibung}

    def komplex(self, name: str, wert: npt.ArrayLike, **beschreibung: Any) -> None:
        feld = np.asarray(wert, dtype=np.complex128)
        self.reell(f"{name}.re", feld.real, teil="Realteil", **beschreibung)
        self.reell(f"{name}.im", feld.imag, teil="Imaginärteil", **beschreibung)


def _pruefung(e: Pruefergebnis) -> dict[str, Any]:
    return dict(asdict(e))


def _spitzen(s: Spitzenergebnis) -> dict[str, Any]:
    return {
        "groesse": s.groesse,
        "einheit": s.einheit,
        "delta_f_hz": s.delta_f_hz,
        "hinweise": list(s.hinweise),
        "grenzen": list(s.grenzen),
        "spitzen": [asdict(x) for x in s.spitzen],
    }


def _band(b: Bandwert) -> dict[str, Any]:
    return {
        "f_u_hz": b.f_u_hz,
        "f_o_hz": b.f_o_hz,
        "groesse": b.groesse,
        "bezug": b.bezug,
        "einheit": b.einheit,
        "rms": b.rms,
        "rms_psv": b.rms_psv,
        "bandnorm": b.bandnorm,
        "n_linien": b.n_linien,
        "w_rbw": b.w_rbw,
        "hinweise": list(b.hinweise),
        "kennzeichen": b.kennzeichen(),
        "skalierung_grundlage": "einseitige Spektren, Spitzenwert (M4)",
    }


def baue_export(auswertung: Auswertung) -> tuple[dict[str, npt.NDArray[Any]], dict[str, Any]]:
    """Stellt Felder und Metadaten des Exports zusammen (ohne Herkunftsangaben der Software).

    Returns
    -------
    felder : dict
        Feldname → NumPy-Feld (nur reelle Typen).
    meta : dict
        JSON-taugliche Metadaten ohne die Abschnitte ``herkunft`` und ``npz_sha256``.
    """
    d = auswertung.daten
    a = auswertung.annahmen
    s = _Sammler()
    spitze = "Spitzenwert (0-to-peak)"
    s.reell("frequenz_hz", d.frequenz_hz, groesse="Frequenz", einheit="Hz")
    s.reell(
        "linienindex",
        np.arange(d.anzahl_linien, dtype=np.int64),
        groesse="Linienindex k",
        einheit="1",
        bemerkung="0-basiert, f_k = (k + k0)·Δf",
    )
    s.reell(
        "punkte.index",
        d.punkte.index.astype(np.int64),
        groesse="Punktindex",
        einheit="1",
        bemerkung="0-basiert",
    )
    s.reell(
        "punkte.label", d.punkte.label.astype(np.int64), groesse="Punktlabel (PSV)", einheit="1"
    )
    s.reell(
        "punkte.koordinaten_m", d.punkte.koordinaten_m, groesse="Koordinaten x, y, z", einheit="m"
    )
    s.reell(
        "punkte.gueltig",
        a.gueltig_je_punkt(d.anzahl_punkte),
        groesse="Gültigkeit",
        einheit="1",
        annahme="M6",
    )
    roh = {"angewandt": "roh (ohne Vorzeichen, ohne Konjugation)", "seitig": "einseitig"}
    for kanal, ap in d.ap.items():
        s.reell(
            f"roh.ap.{_schluessel(kanal)}",
            ap,
            groesse=f"AP {kanal}",
            einheit=einheit_quadrat(d.einheiten[kanal]),
            skalierung=f"{spitze}²",
            kanal=kanal,
            **roh,
        )
    for kanal, betrag in d.betrag.items():
        s.reell(
            f"roh.abs.{_schluessel(kanal)}",
            betrag,
            groesse=f"ABS {kanal}",
            einheit=d.einheiten[kanal],
            skalierung=spitze,
            kanal=kanal,
            **roh,
        )
    for (an, rf), cp in d.cp.items():
        s.komplex(
            f"roh.cp.{paar_schluessel(an, rf)}",
            cp,
            groesse=f"CP {an}/{rf}",
            einheit=einheit_produkt(d.einheiten[an], d.einheiten[rf]),
            skalierung=f"{spitze}²",
            antwort=an,
            referenz=rf,
            **roh,
        )
    for (an, rf), cph in d.cph.items():
        s.komplex(
            f"roh.cph.{paar_schluessel(an, rf)}",
            cph,
            groesse=f"CPH {an}/{rf}",
            einheit=d.einheiten[an],
            skalierung=spitze,
            antwort=an,
            referenz=rf,
            **roh,
        )
    paare_meta: dict[str, Any] = {}
    for (an, rf), pa in auswertung.paare.items():
        k = paar_schluessel(an, rf)
        angewandt = {
            "angewandt": (
                f"s_a = {pa.paar.vorzeichen_antwort:+d}, s_b = {pa.paar.vorzeichen_referenz:+d}, "
                f"konjugieren = {pa.paar.konjugiert}"
            ),
            "antwort": an,
            "referenz": rf,
        }
        frf = pa.frf
        s.komplex(
            f"abgeleitet.{k}.h1",
            frf.h1,
            groesse=frf.bezeichnung_h1,
            einheit=frf.einheit,
            **angewandt,
        )
        s.komplex(f"abgeleitet.{k}.h2", frf.h2, groesse="H2", einheit=frf.einheit, **angewandt)
        s.reell(f"abgeleitet.{k}.kohaerenz", frf.kohaerenz, groesse="γ²", einheit="1", **angewandt)
        s.komplex(
            f"abgeleitet.{k}.spektrum_kohaerent",
            pa.paar.cph,
            groesse="spektrum_kohaerent",
            einheit=pa.paar.einheit_antwort,
            skalierung=spitze,
            seitig="einseitig",
            cph_berechnet=pa.paar.cph_berechnet,
            **angewandt,
        )
        s.reell(
            f"abgeleitet.{k}.spektrum_leistung",
            pa.spektren.spektrum_leistung,
            groesse="spektrum_leistung",
            einheit=pa.paar.einheit_antwort,
            skalierung=spitze,
            seitig="einseitig",
            **angewandt,
        )
        assert (
            pa.mittel_h1.mittel_betrag is not None and pa.mittel_h1.mittel_quadratisch is not None
        )
        s.reell(
            f"abgeleitet.{k}.mittel_betrag_h1",
            pa.mittel_h1.mittel_betrag,
            groesse=f"Betragsmittel |{frf.bezeichnung_h1}|",
            einheit=frf.einheit,
            **angewandt,
        )
        s.reell(
            f"abgeleitet.{k}.mittel_quadratisch_h1",
            pa.mittel_h1.mittel_quadratisch,
            groesse=f"quadratisches Mittel |{frf.bezeichnung_h1}|",
            einheit=frf.einheit,
            **angewandt,
        )
        s.reell(
            f"abgeleitet.{k}.n_mittel",
            pa.mittel_h1.n_mittel,
            groesse="Anzahl Punkte",
            einheit="1",
            **angewandt,
        )
        assert pa.mittel_kohaerenz.mittel_arithmetisch is not None
        s.reell(
            f"abgeleitet.{k}.mittel_kohaerenz",
            pa.mittel_kohaerenz.mittel_arithmetisch,
            groesse="arithmetisches Mittel γ²",
            einheit="1",
            **angewandt,
        )
        for name, m in (
            ("kohaerent", pa.mittel_spektrum_kohaerent),
            ("leistung", pa.mittel_spektrum_leistung),
        ):
            assert m.mittel_betrag is not None and m.mittel_quadratisch is not None
            s.reell(
                f"abgeleitet.{k}.mittel_betrag_spektrum_{name}",
                m.mittel_betrag,
                groesse=f"Betragsmittel spektrum_{name}",
                einheit=pa.paar.einheit_antwort,
                skalierung=spitze,
                **angewandt,
            )
            s.reell(
                f"abgeleitet.{k}.mittel_quadratisch_spektrum_{name}",
                m.mittel_quadratisch,
                groesse=f"quadratisches Mittel spektrum_{name}",
                einheit=pa.paar.einheit_antwort,
                skalierung=spitze,
                **angewandt,
            )
        paare_meta[k] = {
            "antwort": an,
            "referenz": rf,
            "einheit_frf": frf.einheit,
            "bezeichnung_h1": frf.bezeichnung_h1,
            "vorzeichen_antwort": pa.paar.vorzeichen_antwort,
            "vorzeichen_referenz": pa.paar.vorzeichen_referenz,
            "konjugiert": pa.paar.konjugiert,
            "cph_berechnet": pa.paar.cph_berechnet,
            "kohaerenz_min": frf.kohaerenz_min,
            "hinweise_frf": list(frf.hinweise),
            "spitzen": _spitzen(pa.spitzen),
        }
    schwingform_meta: dict[str, Any] | None = None
    sf = auswertung.schwingform
    if sf is not None:
        if sf.amplitude is not None:
            s.komplex(
                "schwingform.amplitude",
                sf.amplitude,
                groesse="Amplitude X, Y, Z",
                einheit=sf.einheit,
                skalierung=spitze,
            )
        s.reell("schwingform.betrag", sf.betrag, groesse="Betrag X, Y, Z", einheit=sf.einheit)
        s.reell(
            "schwingform.betrag_3d_psv",
            sf.betrag_3d_psv,
            groesse="betrag_3d_psv",
            einheit=sf.einheit,
        )
        s.reell(
            "schwingform.auslenkung_max",
            sf.auslenkung_max,
            groesse="auslenkung_max",
            einheit=sf.einheit,
        )
        s.reell(
            "schwingform.auslenkung_min",
            sf.auslenkung_min,
            groesse="auslenkung_min",
            einheit=sf.einheit,
        )
        schwingform_meta = {
            "f_wahl_hz": sf.f_wahl_hz,
            "f_hz": sf.f_hz,
            "linie": sf.linie,
            "quelle": sf.quelle,
            "referenz": sf.referenz,
            "einheit": sf.einheit,
            "phase_gueltig": sf.phase_gueltig,
            "hinweise": list(sf.hinweise),
        }
    meta: dict[str, Any] = {
        "format": FORMAT,
        "format_version": FORMAT_VERSION,
        "konventionen": {
            "zeitkonvention": ZEITKONVENTION,
            "kreuzspektrum": KREUZSPEKTRUM,
            "spektren": "einseitig, Spitzenwert (0-to-peak); Effektivwert = Spitzenwert/√2",
            "frequenzachse": "f_k = (k + k0)·Δf, k = Linienindex 0-basiert",
            "delta_f_hz": d.delta_f_hz,
            "k0": a.k0,
            "k0_status": a.status_von("M2"),
            "w_rbw": a.w_rbw,
            "n_d": a.n_d if isinstance(a.n_d, int) else list(a.n_d),
            "indizes": "0-basiert; Punktlabel getrennt",
            "komplex": "Real- und Imaginärteil getrennt als float64 (….re, ….im)",
            "vorverarbeitung": (
                "abgeleitete Größen mit CP ← s_a·s_b·C(CP_roh), CPH ← s_a·s_b·C(CPH_roh)"
            ),
            "einheiten": dict(d.einheiten),
        },
        "annahmen": [asdict(e) for e in auswertung.annahmen_liste],
        "schwellen": asdict(auswertung.schwellen),
        "felder": s.katalog,
        "paare": paare_meta,
        "pruefungen": [_pruefung(e) for e in auswertung.pruefungen],
        "baender": [_band(b) for b in auswertung.baender],
        "schwingform": schwingform_meta,
    }
    return s.felder, meta


def exportiere(
    auswertung: Auswertung,
    basis: Path,
    *,
    build_info: BuildInfo | None = None,
    jetzt: Callable[[], dt.datetime] | None = None,
    ueberschreiben: bool = False,
) -> tuple[Path, Path]:
    """Schreibt ``<basis>.npz`` und ``<basis>.json`` (FG-02 Abschnitt 5).

    Parameters
    ----------
    auswertung : Auswertung
        Ergebnis von :func:`~.gesamt.werte_aus`.
    basis : pathlib.Path
        Pfad ohne Endung; der Ordner muss existieren.
    build_info : BuildInfo, optional
        Versionsangaben der Software; Voreinstellung :func:`ermittle_build_info`.
    jetzt : callable, optional
        Zeitquelle (für Tests); Voreinstellung lokale Zeit mit Zeitzone.
    ueberschreiben : bool
        Vorhandene Exportdateien ersetzen (Voreinstellung: nein).

    Returns
    -------
    tuple of pathlib.Path
        Pfade der ``.npz``- und ``.json``-Datei.

    Raises
    ------
    FileExistsError
        Wenn eine Zieldatei existiert und ``ueberschreiben`` falsch ist.
    FileNotFoundError
        Wenn der Zielordner fehlt.
    """
    npz = basis.with_name(basis.name + ".npz")
    js = basis.with_name(basis.name + ".json")
    if not basis.parent.is_dir():
        raise FileNotFoundError(f"Zielordner fehlt: {basis.parent}")
    if not ueberschreiben:
        for pfad in (npz, js):
            if pfad.exists():
                raise FileExistsError(f"Exportdatei existiert bereits: {pfad}")
    felder, meta = baue_export(auswertung)
    build = build_info if build_info is not None else ermittle_build_info()
    zeit = (jetzt or (lambda: dt.datetime.now().astimezone()))()
    herkunft = auswertung.daten.herkunft
    meta["herkunft"] = {
        "messdatei": None if herkunft is None else herkunft.pfad,
        "messdatei_sha256": None if herkunft is None else herkunft.sha256,
        "software": asdict(build),
        "erstellt": zeit.isoformat(),
    }
    # Erst temporäre Dateien im Zielordner schreiben, dann je Datei atomar umbenennen. Ein
    # Fehler beim Schreiben hinterlässt keine Exportdatei. Bricht der Lauf zwischen den
    # beiden os.replace ab, kann beim ersten Export eine verwaiste .npz ohne .json bleiben;
    # beim Überschreiben passt die alte .json nicht zur neuen .npz, was lese_export über
    # den SHA-256 erkennt (ValueError).
    npz_tmp = npz.with_name(f".{npz.name}.tmp")
    js_tmp = js.with_name(f".{js.name}.tmp")
    try:
        with npz_tmp.open("wb") as datei:
            np.savez_compressed(datei, **felder)  # type: ignore[arg-type]
        meta["npz_datei"] = npz.name
        meta["npz_sha256"] = sha256_datei(npz_tmp)
        js_tmp.write_text(
            json.dumps(_json_wert(meta), ensure_ascii=False, indent=1, allow_nan=False) + "\n",
            encoding="utf-8",
        )
        os.replace(npz_tmp, npz)
        os.replace(js_tmp, js)
    finally:
        npz_tmp.unlink(missing_ok=True)
        js_tmp.unlink(missing_ok=True)
    return npz, js


def lese_export(basis: Path) -> tuple[dict[str, npt.NDArray[Any]], dict[str, Any]]:
    """Liest einen Export (ohne Pickle) und prüft den SHA-256 der ``.npz``-Datei.

    Raises
    ------
    ValueError
        Bei falschem Format oder abweichender Prüfsumme.
    """
    npz = basis.with_name(basis.name + ".npz")
    js = basis.with_name(basis.name + ".json")
    meta: dict[str, Any] = json.loads(js.read_text(encoding="utf-8"))
    if meta.get("format") != FORMAT:
        raise ValueError(f"kein Export von {FORMAT}: {js}")
    if sha256_datei(npz) != meta.get("npz_sha256"):
        raise ValueError(f"SHA-256 von {npz.name} passt nicht zu den Metadaten")
    with np.load(npz, allow_pickle=False) as archiv:
        felder = {name: archiv[name] for name in archiv.files}
    return felder, meta
