"""Oberfläche der Mess-Warteschlange (PySide6, Qt Widgets; Paket U4, Design-Brief P3).

Aufbau:

* :mod:`.tokens`: Farben, Symbole, Schriften und Maße (Qt-frei).
* :mod:`.anzeige`: reine Funktionen, die ein ``Zustandsbild`` auf Anzeigewerte abbilden
  (Aktivierung, Hinweisband, Fortschritt, Zeilenstatus, Eingabeprüfung), Qt-frei.
* :mod:`.stil`, :mod:`.tabelle`, :mod:`.editor`, :mod:`.hinweisband`, :mod:`.dialoge`,
  :mod:`.hauptfenster`, :mod:`.start`: dünne Qt-Schicht.

Die Oberfläche importiert nur ``sitzung`` und ``domaene`` (Plan P2, 1; Importtest). Dieses
Paket-Modul importiert bewusst kein Qt, damit die Qt-freie Logik ohne Qt testbar bleibt.
"""
