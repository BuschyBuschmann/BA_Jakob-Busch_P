"""Parameterkatalog: welche Messparameter gegenüber der Einstellungsdatei änderbar sind.

Der Katalog ist bewusst erweiterbar (offener Punkt O3 der Anforderungen): Neue Parameter
werden mit :meth:`Parameterkatalog.registrieren` ergänzt, ohne Domäne, Ablauf oder Adapter
zu ändern. Die Wertebereiche hier sind die Grenzen, die die Software selbst prüft. Das Gerät
kann zusätzlich einrasten (z. B. Bandbreite); deshalb wird nach dem Setzen zurückgelesen
(siehe :meth:`ParameterSpec.stimmt_ueberein`).

Der Generator ist absichtlich nicht im Katalog (Sicherheitsvorgabe).
"""

from __future__ import annotations

import math
from collections.abc import Iterable, Iterator, Mapping
from dataclasses import dataclass
from typing import Literal, TypeAlias

ParameterWert: TypeAlias = int | float | str
"""Zulässiger Wert eines Parameters. Gleitkommawerte sind ``float`` (float64)."""

# Relative Toleranz für den Soll/Ist-Vergleich von Gleitkommawerten. Doubles werden über COM
# als VT_R8 ohne Rundung übertragen; die Toleranz fängt nur Darstellungsunterschiede ab.
# Einrastsprünge des Geräts liegen um Größenordnungen darüber (Plan P2, M5).
REL_TOL_ZURUECKLESEN = 1e-9


def _zahl_text(zahl: float) -> str:
    """Kurztext einer Zahl für Meldungen; kein Überlauf bei riesigen Ganzzahlen."""
    text = str(zahl) if isinstance(zahl, int) else f"{zahl:g}"
    return text if len(text) <= 30 else text[:27] + "..."


@dataclass(frozen=True, kw_only=True)
class ParameterSpec:
    """Beschreibung eines änderbaren Parameters.

    Parameters
    ----------
    schluessel : str
        Eindeutiger Name, Schreibweise ``gruppe.name`` (Einheit im Namen, z. B. ``_hz``).
    typ : {"int", "float", "str"}
        Werttyp. ``bool`` ist nie zulässig.
    einheit : str
        Einheit des Werts (SI); leer bei einheitenlosen Werten.
    com_gruppe : str
        Zuordnung zur Gruppe der Geräteeinstellungen (z. B. ``"fft"``, ``"mittelung"``).
        Wird nur vom Adapter ausgewertet.
    beschreibung : str
        Kurztext für Oberfläche und Protokoll.
    minimum, maximum : float or None
        Numerische Grenzen (``None`` = unbeschränkt).
    minimum_exklusiv : bool
        Ist ``True``, ist ``minimum`` selbst nicht zulässig (Bedingung ``> minimum``).
    erlaubt : tuple of str or None
        Erlaubte Werte bei ``typ == "str"``.
    """

    schluessel: str
    typ: Literal["int", "float", "str"]
    einheit: str
    com_gruppe: str
    beschreibung: str = ""
    minimum: float | None = None
    maximum: float | None = None
    minimum_exklusiv: bool = False
    erlaubt: tuple[str, ...] | None = None

    def bereich_text(self) -> str:
        """Lesbare Beschreibung des zulässigen Bereichs (für Fehlermeldungen)."""
        if self.typ == "str":
            return "{" + ", ".join(self.erlaubt) + "}" if self.erlaubt else "beliebiger Text"
        einheit = f" {self.einheit}" if self.einheit else ""
        if self.minimum is not None and self.maximum is not None:
            return f"{self.minimum:g} … {self.maximum:g}{einheit}"
        if self.minimum is not None:
            op = ">" if self.minimum_exklusiv else "≥"
            return f"{op} {self.minimum:g}{einheit}"
        if self.maximum is not None:
            return f"≤ {self.maximum:g}{einheit}"
        return f"beliebig{einheit}"

    def pruefe(self, wert: object) -> ParameterWert:
        """Prüft einen Wert gegen Typ und Bereich und gibt ihn normalisiert zurück.

        Parameters
        ----------
        wert : object
            Zu prüfender Wert. Bei ``typ == "float"`` sind ``int`` und ``float`` zulässig
            (Ergebnis ist ``float``), bei ``"int"`` nur ``int``.

        Returns
        -------
        int or float or str
            Der normalisierte Wert.

        Raises
        ------
        ValueError
            Bei falschem Typ, NaN/Inf oder Wert außerhalb des Bereichs. Die Meldung nennt
            Schlüssel, Wert und zulässigen Bereich.
        """
        schluessel = self.schluessel
        if self.typ == "str":
            if not isinstance(wert, str):
                raise ValueError(
                    f"Parameter '{schluessel}': Text erwartet, erhalten {type(wert).__name__}"
                )
            if self.erlaubt is not None and wert not in self.erlaubt:
                raise ValueError(
                    f"Parameter '{schluessel}': Wert {wert!r} außerhalb des Bereichs "
                    f"{self.bereich_text()}"
                )
            return wert

        if isinstance(wert, bool):
            raise ValueError(f"Parameter '{schluessel}': Zahl erwartet, erhalten bool")
        zahl: int | float
        if self.typ == "int":
            if not isinstance(wert, int):
                raise ValueError(
                    f"Parameter '{schluessel}': Ganzzahl erwartet, erhalten {type(wert).__name__}"
                )
            zahl = wert
        else:
            if not isinstance(wert, int | float):
                raise ValueError(
                    f"Parameter '{schluessel}': Zahl erwartet, erhalten {type(wert).__name__}"
                )
            try:
                zahl = float(wert)
            except OverflowError:
                raise ValueError(
                    f"Parameter '{schluessel}': Wert {_zahl_text(wert)} ist nicht darstellbar"
                ) from None
            if not math.isfinite(zahl):
                raise ValueError(f"Parameter '{schluessel}': Wert {zahl} ist nicht endlich")

        zu_klein = self.minimum is not None and (
            zahl <= self.minimum if self.minimum_exklusiv else zahl < self.minimum
        )
        zu_gross = self.maximum is not None and zahl > self.maximum
        if zu_klein or zu_gross:
            raise ValueError(
                f"Parameter '{schluessel}': Wert {_zahl_text(zahl)} außerhalb des Bereichs "
                f"{self.bereich_text()}"
            )
        return zahl

    def _hat_typ(self, wert: object) -> bool:
        """Prüft, ob ``wert`` zum Werttyp passt (``bool`` ist nie eine Zahl)."""
        if self.typ == "str":
            return isinstance(wert, str)
        if isinstance(wert, bool):
            return False
        if self.typ == "int":
            return isinstance(wert, int)
        return isinstance(wert, int | float)

    def stimmt_ueberein(self, soll: object, ist: object) -> bool:
        """Vergleicht Sollwert und zurückgelesenen Wert.

        Ganzzahlen und Text werden exakt verglichen, Gleitkommawerte mit
        ``math.isclose(rel_tol=1e-9, abs_tol=0.0)`` (Begründung siehe
        ``REL_TOL_ZURUECKLESEN``).

        Ein Wert mit falschem Typ (``bool``, ``None``, Text statt Zahl, Zahl statt Text,
        Gleitkomma statt Ganzzahl), NaN oder ein nicht darstellbarer Wert ist **keine
        Übereinstimmung**: Die Methode gibt dann ``False`` zurück und wirft nie. Die
        Steuerung behandelt ``False`` als Abweichung (M5).
        """
        if not (self._hat_typ(soll) and self._hat_typ(ist)):
            return False
        if self.typ == "float":
            try:
                return math.isclose(
                    float(soll),  # type: ignore[arg-type]  # Typ in _hat_typ geprüft
                    float(ist),  # type: ignore[arg-type]
                    rel_tol=REL_TOL_ZURUECKLESEN,
                    abs_tol=0.0,
                )
            except OverflowError:
                return False
        return bool(soll == ist)


class Parameterkatalog:
    """Erweiterbare Menge von :class:`ParameterSpec`.

    Parameters
    ----------
    specs : iterable of ParameterSpec
        Anfangsbestand.
    """

    def __init__(self, specs: Iterable[ParameterSpec] = ()) -> None:
        self._specs: dict[str, ParameterSpec] = {}
        for spec in specs:
            self.registrieren(spec)

    def registrieren(self, spec: ParameterSpec, *, ersetzen: bool = False) -> None:
        """Nimmt einen Parameter in den Katalog auf.

        Raises
        ------
        ValueError
            Wenn der Schlüssel schon existiert und ``ersetzen`` nicht gesetzt ist.
        """
        if spec.schluessel in self._specs and not ersetzen:
            raise ValueError(f"Parameter '{spec.schluessel}' ist bereits im Katalog")
        self._specs[spec.schluessel] = spec

    def __contains__(self, schluessel: object) -> bool:
        return schluessel in self._specs

    def __iter__(self) -> Iterator[ParameterSpec]:
        return iter(tuple(self._specs.values()))

    def __len__(self) -> int:
        return len(self._specs)

    def spec(self, schluessel: str) -> ParameterSpec:
        """Gibt die Beschreibung zu einem Schlüssel zurück.

        Raises
        ------
        ValueError
            Bei unbekanntem Schlüssel (Meldung nennt die bekannten Schlüssel).
        """
        try:
            return self._specs[schluessel]
        except (KeyError, TypeError):
            bekannt = ", ".join(sorted(self._specs))
            raise ValueError(f"Unbekannter Parameter '{schluessel}' (bekannt: {bekannt})") from None

    def pruefe(self, parameter: Mapping[str, object]) -> dict[str, ParameterWert]:
        """Prüft und normalisiert eine Parameterzuordnung.

        Raises
        ------
        ValueError
            Bei unbekanntem Schlüssel oder ungültigem Wert (siehe :meth:`ParameterSpec.pruefe`).
        """
        if not isinstance(parameter, Mapping):
            raise ValueError(
                f"Parameter müssen eine Zuordnung sein, erhalten {type(parameter).__name__}"
            )
        return {k: self.spec(k).pruefe(v) for k, v in parameter.items()}


_STANDARD_SPECS = (
    ParameterSpec(
        schluessel="fft.bandbreite_hz",
        typ="float",
        einheit="Hz",
        com_gruppe="fft",
        beschreibung="FFT-Bandbreite",
        minimum=0.0,
        minimum_exklusiv=True,
    ),
    ParameterSpec(
        schluessel="fft.linien",
        typ="int",
        einheit="",
        com_gruppe="fft",
        beschreibung="Anzahl FFT-Linien",
        minimum=1,
    ),
    ParameterSpec(
        schluessel="mittelung.anzahl",
        typ="int",
        einheit="",
        com_gruppe="mittelung",
        beschreibung="Anzahl Mittelungen",
        minimum=3,
        maximum=10000,
    ),
    ParameterSpec(
        schluessel="mittelung.typ",
        typ="str",
        einheit="",
        com_gruppe="mittelung",
        beschreibung="Mittelungsart (Namen nach PTCAverageType)",
        erlaubt=("Off", "Magnitude", "Complex", "Time", "Peakhold"),
    ),
)

KATALOG = Parameterkatalog(_STANDARD_SPECS)
"""Standardkatalog des Prototyps (vom Nutzer bestätigt, 2026-10-26); erweiterbar."""
