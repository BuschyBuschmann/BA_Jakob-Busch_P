"""COM-Adapter für die Polytec-PSV-Software (Windows, pywin32, Late Binding).

Aufbau (Plan P2, Abschnitt 1):

* :mod:`.konstanten`: eigene ``IntEnum``-Spiegelung der benötigten Polytec-Werte (ADR-003).
* :mod:`.whitelist`: allgemeiner Whitelist-Proxy mit Default deny (ADR-007).
* :mod:`.richtlinie`: Produktiv-Richtlinie S1-S9 und „Nie“-Katalog (Plan P2, 3.3).
* :mod:`.bindung`: Schnittstelle zur COM-Laufzeit plus Auswertung der Prozessliste.
* :mod:`.adapter`: :class:`~.adapter.PsvComGeraet`, setzt ``Messgeraet`` um.
* :mod:`.pywin32_bindung`: einzige Datei mit pywin32-Import (nur Windows).
"""
