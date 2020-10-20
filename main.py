#   Projektarbeit Literaturrecherche zu Simulationsalgorithmen für Quantencomputing
#   Author: Lukas Lepper, 19.10.2020
#   Betreuer: Martin Hardieck
#   Dateiname: main.py
#   Version: 0.5

#   Klassen importieren, mit deren Memberfunktionen gearbeitet werden muss.
#   Die Klasse QuantumSimulation bietet die Hauptfunktionen für die Simulation an, die in der main gesteuert wird.
#   Sie benötigt daher Zugriff auf alle anderen Unterklassen der untersten Ebene. In den Funktionen dieser Hauptklasse
#   werden daher Objekte der untersten Ebene erzeugt. Die Klassen dieser Ebene erben von den darüber liegenden Klassen,
#   sodass alle Funktionen/Variablen in der Hauptklasse erreichbar sind.
from QuantumSimulation import QuantumSimulation
from Base import Base


#   QuantumSimulation Objekt erstellen
q_sim = QuantumSimulation()

#   Hinweis, was das Programm berechnet. ToDo: An aktuelle Funktionen anpassen
print('\nSimulation von Quantenschaltungen, für eine kleine Anzahl an Qubits.')

#   Starte Eingabeaufforderung für Parameter der Klasse QuantumSimulation
q_sim.cmd_input_for_qsim()

#   Führe Berechnung der eingelesenen Eingabe durch
q_sim.qstate_obj = q_sim.calculate()

#   gebe Ergebnis des Zustandsvektors aus
print(q_sim.qstate_obj)

