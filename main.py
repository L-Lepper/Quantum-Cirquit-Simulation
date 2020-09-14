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


#   ToDo: Warte auf Befehl "von Datei einlesen" oder "aus Befehlen einlesen"
#   Jetzt erfolgt Eingabe fest vorprogrammiert über die Konsole
#read_from_file = False

#   QuantumSimulation Objekt erstellen
#q_sim = QuantumSimulation()

#   Je nach vorheriger Eingabe, wird aus Konsole oder von Datei eingelesen
#   ToDo: Kann auch im Konstruktor von QuantumSimulation() erfolgen:
#if read_from_file:
#    q_sim.read_input_from_file()
#else:
#    q_sim.read_input_from_cmd()

#   Führe Berechnung der eingelesenen Eingabe durch
#q_sim.qstate_obj = q_sim.calculate()

#   gebe Ergebnis des Zustandsvektors aus
#print(q_sim.qstate_obj)


from DecisionDiagram import DecisionDiagram
from Base import Base
import numpy as np


Base.set_n_qubits(3)
arr = np.array([[5,7,1,0,6,4,5,0],[8,7,2,3,0,1,7,6],[1,0,5,7,3,8,4,0],[2,3,8,7,7,9,3,1],[5,5,5,5,5,7,1,0],[5,5,5,5,8,7,2,3],[5,5,5,5,1,0,5,7],[5,5,5,5,2,3,8,7]])
#Base.set_n_qubits(4)
#arr = np.array([0.3082207001, 0.05477225575, 0.1760681686, 0.242899156, 0.3082207001, 0.05477225575, 0.2236067977, 0.3464101615, 0.3082207001, 0.05477225575, 0.2236067977, 0.3464101615, 0.2626785107, 0.2626785107, 0.2626785107, 0.2626785107])
#Base.set_n_qubits(4)
#arr = np.array([1, 2, 2, 5, 2, 1, 5, 1, 1, 2, 2, 5, 1, 1, 5, 5])
#Base.set_n_qubits(2)
#arr = np.array([1, 2, 1, 2])

obj = DecisionDiagram(arr)
print('\n\nTest des Aufbaus des Entscheidungsdiagramms. Die jeder Knoten hat 4 Nachfolgekanten, \ndie Knoten werden'
      'durch die jeweiligen Matrizen dargestellt:\n')
print(obj.list_of_all_edges[0])
print('\n\n\nTest der Anzahl an verschiedenen Knoten. Redundante Knoten sind zusammengefasst:\n')
for x in obj.list_of_all_nodes:
    print(x.saved_value_on_node)
