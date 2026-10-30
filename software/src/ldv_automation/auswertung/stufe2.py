r"""Gesamtauswertung Stufe 2 und Export (FG-03, Paket W5-2).

:func:`werte_stufe2_aus` liest eine Stufe-1-Auswertung (:class:`~.gesamt.Auswertung`) und
bildet daraus zusätzliche Größen mit eigenen Namen; Stufe 1 bleibt unverändert (FG-03 1):

- B-1 Dämpfungsschätzung je gewähltem Kanalpaar (:mod:`.modenfit`),
- B-5 Drift innerhalb der Messung (:func:`.vergleich.drift_aus`),
- B-8 Normalenbezug der Schwingform der Stufe 1 (:mod:`.bezug3d`).

Der Vergleich zweier Messungen (B-5, :func:`.vergleich.vergleiche_messungen`) wird getrennt
gebildet und kann dem Export beigegeben werden.

:func:`exportiere_stufe2` schreibt über den bestehenden Exportweg
(:func:`.export.schreibe_export`) ``<basis>.npz`` und ``<basis>.json`` mit SHA-256 der
``.npz``-Datei, Herkunft der Messdatei(en) und Git-Hash der Software. Format
``ldv_automation.auswertung.export.stufe2``. Alle Annahmen M1–M15 stehen mit Status in
``annahmen``.
"""

from __future__ import annotations

import datetime as dt
from collections.abc import Callable, Sequence
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import numpy as np
import numpy.typing as npt

from ldv_automation.protokoll.version import BuildInfo

from .annahmen import AnnahmeEintrag, AnnahmenStufe2, SchwellenStufe2
from .bezug3d import Komponentenbezug, komponentenbezug
from .export import (
    KREUZSPEKTRUM,
    ZEITKONVENTION,
    Sammler,
    paar_schluessel,
    pruefe_ziel,
    schreibe_export,
)
from .gesamt import Auswertung
from .modenfit import ModenfitErgebnis, schaetze_daempfung
from .vergleich import Drift, Vergleich, drift_aus

FORMAT_STUFE2 = "ldv_automation.auswertung.export.stufe2"
FORMAT_STUFE2_VERSION = 1


@dataclass(frozen=True, kw_only=True, eq=False)
class Stufe2Ergebnis:
    """Ergebnisse der Stufe 2 einer Messung (FG-03 Datenvertrag 6.2).

    Attributes
    ----------
    auswertung : Auswertung
        Zugrunde liegende Stufe-1-Auswertung (unverändert).
    annahmen2 : AnnahmenStufe2
        M12–M15.
    schwellen2 : SchwellenStufe2
        Parameter und Schwellen (E6).
    daempfung : dict
        B-1 je Kanalpaar.
    drift : tuple of Drift
        B-5-Drift je gewählter Spitze.
    komponenten : Komponentenbezug or None
        B-8.
    annahmen_liste : tuple of AnnahmeEintrag
        M1–M11 (Stufe 1) und M12–M15.
    """

    auswertung: Auswertung
    annahmen2: AnnahmenStufe2
    schwellen2: SchwellenStufe2
    daempfung: dict[tuple[str, str], ModenfitErgebnis]
    drift: tuple[Drift, ...]
    komponenten: Komponentenbezug | None
    annahmen_liste: tuple[AnnahmeEintrag, ...]


def werte_stufe2_aus(
    auswertung: Auswertung,
    *,
    paare: Sequence[tuple[str, str]] = (),
    spitzen: dict[tuple[str, str], Sequence[int]] | None = None,
    zeit_s: npt.ArrayLike | None = None,
    drift_paar: tuple[str, str] | None = None,
    drift_antriebspunkt: bool = True,
    drift_spitzen_hz: Sequence[float] = (),
    elemente: Sequence[Sequence[int]] | None = None,
    annahmen2: AnnahmenStufe2 | None = None,
    schwellen2: SchwellenStufe2 | None = None,
) -> Stufe2Ergebnis:
    r"""Wertet eine Messung nach FG-03 aus (B-1, Drift, B-8).

    Parameters
    ----------
    auswertung : Auswertung
        Stufe-1-Auswertung.
    paare : sequence of tuple of str
        Kanalpaare für B-1.
    spitzen : dict, optional
        Je Paar die Stufe-1-Spitzenindizes, deren Gruppen gefittet werden (sonst alle).
    zeit_s : array_like, optional
        Zeit je Punkt in s (M15); nötig für die Drift.
    drift_paar : tuple of str, optional
        Datengrundlage der Drift (z. B. das Antriebspunkt-Paar).
    drift_antriebspunkt : bool
        ``True``: alle gültigen Punkte des Paars; ``False``: Punkte mit
        :math:`|H_1| \ge 0{,}3\max`.
    drift_spitzen_hz : sequence of float
        Frequenzen der Spitzen für die Drift.
    elemente : sequence of sequence of int, optional
        Elemente der Geometrie (M14) für B-8; B-8 nutzt die Schwingform der Stufe 1.
    annahmen2, schwellen2
        M12–M15 und Parameter (Voreinstellungen FG-03).

    Raises
    ------
    ValueError
        Drift ohne ``zeit_s`` oder ohne ``drift_paar``.
    """
    annahmen2 = annahmen2 if annahmen2 is not None else AnnahmenStufe2()
    schwellen2 = schwellen2 if schwellen2 is not None else SchwellenStufe2()
    daempfung = {
        paar: schaetze_daempfung(
            auswertung,
            paar,
            schwellen2=schwellen2,
            spitzen=None if spitzen is None else spitzen.get(paar),
        )
        for paar in paare
    }
    drift: list[Drift] = []
    if drift_spitzen_hz:
        if zeit_s is None or drift_paar is None:
            raise ValueError("Drift braucht zeit_s und drift_paar")
        for f in drift_spitzen_hz:
            d, _ = drift_aus(
                auswertung,
                zeit_s,
                f,
                drift_paar,
                antriebspunkt=drift_antriebspunkt,
                schwellen2=schwellen2,
            )
            drift.append(d)
    komponenten = None
    if elemente is not None:
        komponenten = komponentenbezug(
            auswertung.daten.punkte.koordinaten_m,
            elemente,
            auswertung.schwingform,
            annahmen2=annahmen2,
            schwellen2=schwellen2,
        )
    return Stufe2Ergebnis(
        auswertung=auswertung,
        annahmen2=annahmen2,
        schwellen2=schwellen2,
        daempfung=daempfung,
        drift=tuple(drift),
        komponenten=komponenten,
        annahmen_liste=(*auswertung.annahmen_liste, *annahmen2.eintraege()),
    )


def _komplex(z: complex) -> list[float]:
    return [z.real, z.imag]


def _b1_meta(b1: ModenfitErgebnis) -> dict[str, Any]:
    return {
        "antwort": b1.antwort,
        "referenz": b1.referenz,
        "frf_art": b1.frf_art,
        "einheit_fit": b1.einheit_fit,
        "einheit_modalkonstante": "1/kg (bei Mobilität)",
        "komplex": "[Realteil, Imaginärteil]",
        "gruppen": [asdict(g) for g in b1.gruppen],
        "ergebnisse": [
            {
                **{
                    k: v
                    for k, v in asdict(e).items()
                    if k not in ("modalkonstante", "residuum", "kennzeichen")
                },
                "modalkonstante": [_komplex(c) for c in e.modalkonstante],
                "residuum": _komplex(e.residuum),
                "kennzeichen": [list(k) for k in e.kennzeichen],
            }
            for e in b1.ergebnisse
        ],
        "zusammenfassung": [asdict(z) for z in b1.zusammenfassung],
        "hinweise": list(b1.hinweise),
        "grenzen": list(b1.grenzen),
    }


def _komponenten(s: Sammler, kb: Komponentenbezug) -> dict[str, Any]:
    en = kb.elemente
    s.reell("b8.normale_element", en.normale, groesse="normale_element", einheit="1")
    s.reell("b8.flaeche_element", en.flaeche_m2, groesse="flaeche_element", einheit="m^2")
    s.reell("b8.normale_punkt", kb.normale_punkt, groesse="normale_punkt", einheit="1")
    if kb.zerlegung is not None and kb.ellipse is not None:
        z = kb.zerlegung
        e = kb.ellipse
        s.komplex("b8.v_normal", z.v_normal, groesse="v_normal", einheit=kb.einheit)
        s.komplex("b8.v_tangential", z.v_tangential, groesse="v_tangential", einheit=kb.einheit)
        s.reell("b8.anteil_normal", z.anteil_normal, groesse="anteil_normal", einheit="1")
        s.reell("b8.achse_max", e.achse_max, groesse="achse_max", einheit="1")
        s.reell("b8.drehsinn", e.drehsinn, groesse="drehsinn", einheit="1")
        s.reell("b8.auslenkung_max", e.auslenkung_max, groesse="auslenkung_max", einheit=kb.einheit)
        s.reell("b8.auslenkung_min", e.auslenkung_min, groesse="auslenkung_min", einheit=kb.einheit)
    return {
        "f_hz": kb.f_hz,
        "einheit": kb.einheit,
        "elemente": [list(e) for e in en.elemente],
        "orientierung_unsicher": np.flatnonzero(en.orientierung_unsicher).tolist(),
        "entartet": np.flatnonzero(en.entartet).tolist(),
        "hinweise": list(kb.hinweise),
    }


def _vergleich(s: Sammler, v: Vergleich) -> dict[str, Any]:
    z = v.zuordnung
    s.reell("b5.index_a", z.index_a, groesse="Punktindex A", einheit="1")
    s.reell("b5.index_b", z.index_b, groesse="Punktindex B", einheit="1")
    s.reell("b5.abstand_m", z.abstand_m, groesse="Abstand", einheit="m")
    s.reell("b5.drehung", z.drehung, groesse="R", einheit="1")
    s.reell("b5.verschiebung_m", z.verschiebung_m, groesse="t", einheit="m")
    s.reell("b5.mac", v.mac, groesse="MAC je Spitzenpaar", einheit="1")
    s.reell("b5.auto_mac_a", v.auto_mac_a, groesse="Auto-MAC A", einheit="1")
    s.reell("b5.auto_mac_b", v.auto_mac_b, groesse="Auto-MAC B", einheit="1")
    for i, b in enumerate(v.frf):
        band = {"f_u_hz": b.f_u_hz, "f_o_hz": b.f_o_hz}
        s.reell(f"b5.band{i}.frac", b.frac, groesse="frac", einheit="1", **band)
        s.reell(f"b5.band{i}.pegel_db", b.pegel_db, groesse="pegel_db", einheit="dB", **band)
        s.reell(f"b5.band{i}.diff_rel", b.diff_rel, groesse="diff_rel", einheit="1", **band)
        s.reell(f"b5.band{i}.n_linien", b.n_linien, groesse="n_linien", einheit="1", **band)
    return {
        "paar": list(v.paar),
        "achsen_gleich": v.achsen_gleich,
        "mac_3d": v.mac_3d,
        "zuordnung": {
            "variante": z.variante,
            "rms_passpunkte_m": z.rms_passpunkte_m,
            "d_tol_m": z.d_tol_m,
            "ohne_partner_a": list(z.ohne_partner_a),
            "ohne_partner_b": list(z.ohne_partner_b),
            "kennzeichen": list(z.kennzeichen),
            "hinweise": list(z.hinweise),
        },
        "spitzenpaare": [asdict(p) for p in v.spitzen.paare],
        "spitzen_ohne_partner_a": list(v.spitzen.ohne_partner_a),
        "spitzen_ohne_partner_b": list(v.spitzen.ohne_partner_b),
        "df_tol_hz": v.spitzen.df_tol_hz,
        "frf_hinweise": [list(b.hinweise) for b in v.frf],
        "hinweise": list(v.hinweise),
    }


def baue_export_stufe2(
    ergebnis: Stufe2Ergebnis, vergleich: Vergleich | None = None
) -> tuple[dict[str, npt.NDArray[Any]], dict[str, Any]]:
    """Felder und Metadaten des Stufe-2-Exports (ohne Herkunftsangaben der Software)."""
    s = Sammler()
    a = ergebnis.auswertung
    meta: dict[str, Any] = {
        "format": FORMAT_STUFE2,
        "format_version": FORMAT_STUFE2_VERSION,
        "grundlage": "FG-03 (Stufe 2) auf Stufe-1-Auswertung nach FG-02",
        "konventionen": {
            "zeitkonvention": ZEITKONVENTION,
            "kreuzspektrum": KREUZSPEKTRUM,
            "modellform": "Y = sum i w R_r/(w_r^2 - w^2 + 2 i zeta_r w_r w) + C (Mobilität)",
            "indizes": "0-basiert",
            "delta_f_hz": a.daten.delta_f_hz,
            "einheiten": dict(a.daten.einheiten),
        },
        "annahmen": [asdict(e) for e in ergebnis.annahmen_liste],
        "schwellen": asdict(a.schwellen),
        "schwellen_stufe2": asdict(ergebnis.schwellen2),
        "b1": {paar_schluessel(*k): _b1_meta(v) for k, v in ergebnis.daempfung.items()},
        "drift": [asdict(d) for d in ergebnis.drift],
        "b8": None if ergebnis.komponenten is None else _komponenten(s, ergebnis.komponenten),
        "b5": None if vergleich is None else _vergleich(s, vergleich),
    }
    s.reell("frequenz_hz", a.daten.frequenz_hz, groesse="Frequenz", einheit="Hz")
    s.reell("punkte.label", a.daten.punkte.label.astype(np.int64), groesse="Label", einheit="1")
    s.reell(
        "punkte.koordinaten_m", a.daten.punkte.koordinaten_m, groesse="Koordinaten", einheit="m"
    )
    meta["felder"] = s.katalog
    return s.felder, meta


def exportiere_stufe2(
    ergebnis: Stufe2Ergebnis,
    basis: Path,
    *,
    vergleich: Vergleich | None = None,
    vergleich_auswertung: Auswertung | None = None,
    build_info: BuildInfo | None = None,
    jetzt: Callable[[], dt.datetime] | None = None,
    ueberschreiben: bool = False,
) -> tuple[Path, Path]:
    """Schreibt den Stufe-2-Export ``<basis>.npz`` + ``<basis>.json``.

    Parameters
    ----------
    ergebnis : Stufe2Ergebnis
        Ergebnis von :func:`werte_stufe2_aus` (Messung A).
    basis : pathlib.Path
        Pfad ohne Endung; der Ordner muss existieren.
    vergleich : Vergleich, optional
        B-5-Vergleich mit einer Messung B.
    vergleich_auswertung : Auswertung, optional
        Stufe-1-Auswertung von B (Herkunft im Export).
    build_info, jetzt, ueberschreiben
        Wie :func:`.export.exportiere`.
    """
    pruefe_ziel(basis, ueberschreiben)
    felder, meta = baue_export_stufe2(ergebnis, vergleich)
    herkunft = ergebnis.auswertung.daten.herkunft
    messdatei: dict[str, Any] = {
        "messdatei": None if herkunft is None else herkunft.pfad,
        "messdatei_sha256": None if herkunft is None else herkunft.sha256,
    }
    if vergleich_auswertung is not None:
        hb = vergleich_auswertung.daten.herkunft
        messdatei["vergleich_messdatei"] = None if hb is None else hb.pfad
        messdatei["vergleich_messdatei_sha256"] = None if hb is None else hb.sha256
    return schreibe_export(
        felder,
        meta,
        basis,
        messdatei=messdatei,
        build_info=build_info,
        jetzt=jetzt,
        ueberschreiben=ueberschreiben,
    )
