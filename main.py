#   Projektarbeit Literaturrecherche zu Simulationsalgorithmen für Quantencomputing
#   Author: Lukas Lepper, 14.09.2020
#   Betreuer: Martin Hardieck
#   Dateiname: DDEdge.py
#   Version: 0.4

#   Klassen importieren, mit deren Memberfunktionen gearbeitet werden muss.
#   Die Klasse QuantumSimulation bietet die Hauptfunktionen für die Simulation an, die in der main gesteuert wird.
#   Sie benötigt daher Zugriff auf alle anderen Unterklassen der untersten Ebene. In den Funktionen dieser Hauptklasse
#   werden daher Objekte der untersten Ebene erzeugt. Die Klassen dieser Ebene erben von den darüber liegenden Klassen,
#   sodass alle Funktionen/Variablen in der Hauptklasse erreichbar sind.
from QuantumSimulation import QuantumSimulation
from Base import Base


#   ToDo: Warte auf Befehl "von Datei einlesen" oder "aus Befehlen einlesen"
#   Jetzt erfolgt Eingabe fest vorprogrammiert über die Konsole
read_from_file = False

Base.enable_debug(3)

#   QuantumSimulation Objekt erstellen
q_sim = QuantumSimulation()

#   Je nach vorheriger Eingabe, wird aus Konsole oder von Datei eingelesen
#   ToDo: Kann auch im Konstruktor von QuantumSimulation() erfolgen:
if read_from_file:
    q_sim.read_input_from_file()
else:
    q_sim.read_input_from_cmd()

#   Führe Berechnung der eingelesenen Eingabe durch
q_sim.qstate_obj = q_sim.calculate()

#   gebe Ergebnis des Zustandsvektors aus
print(q_sim.qstate_obj)

