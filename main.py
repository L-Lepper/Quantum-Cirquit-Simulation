#!/usr/bin/env python3
#   Projektarbeit Literaturrecherche zu Simulationsalgorithmen für Quantencomputing
#   Author: Lukas Lepper, 21.10.2020
#   Betreuer: Martin Hardieck
#   Dateiname: main.py
#   Version: 0.5

#   Klassen importieren, mit deren Memberfunktionen gearbeitet werden muss.
#   Die Klasse QuantumSimulation bietet die Hauptfunktionen für die Simulation an, die in der main gesteuert wird.
#   Sie benötigt daher Zugriff auf alle anderen Unterklassen der untersten Ebene. In den Funktionen dieser Hauptklasse
#   werden daher Objekte der untersten Ebene erzeugt. Die Klassen dieser Ebene erben von den darüber liegenden Klassen,
#   sodass alle Funktionen/Variablen in der Hauptklasse erreichbar sind.
from QuantumSimulation import QuantumSimulation

# Modul sys wird importiert:
import sys

from Base import Base


if __name__ == '__main__':
    #   QuantumSimulation Objekt erstellen
    q_sim = QuantumSimulation()

    #   Starte Eingabeaufforderung für Parameter der Klasse QuantumSimulation
    q_sim.cmd_line_parser(sys.argv)
