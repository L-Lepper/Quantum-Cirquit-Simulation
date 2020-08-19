#   Projektarbeit Literaturrecherge zu Simulationsalgorithmen für Quantencomputing
#   Author: Lukas Lepper, 19.08.2020
#   Betreuer: Martin Hardieck
#   Dateiname: QState.py
#   Version: 0.2

from getdiracnotation import getdiracnotation
import numpy as np
from QuantumSimulation import QuantumSim


class QState(QuantumSim):
    """Klasse für Quantenzustandsvektoren: enthält verschedene Darstellungen und überladenen Operator für
    Matrix-Vektor-Produkt"""

    #   Default-Konstruktor
    def __init__(self, phi_in):
        """Erstellt Zustandsvektor aus eingegebenen Zustand"""

#        #   Liste in der die möglichen Zuständen gespeichert werden sollen (10011: [1, 0, 0, 1, 1])
#        self.possible_states = np.empty([pow(2, QuantumSim.getnqubits()), QuantumSim.getnqubits()], dtype=str)

        #   Leeren Zustandsvektor erstellen
        self.phi_vec = np.zeros(pow(2, QuantumSim.getnqubits()), dtype=complex)

        #   Position des Eingegebenen Zustandes im Zustandsvektor finden: Rekursives Vorgehen. Index wird auf 0 gesetzt.
        #   Dann wird ein Zeichen des Eingabezustandes betrachtet. Bei 0 wird index beibehalten, bei 1 wird dem Index
        #   die Zahl der Hälfte der möglichen Zustände, die sich aus den verbleibenden Qubits einschließlich des
        #   Betrachteten ergibt, hinzu addiert.
        index_phi_vec = 0
        n = QuantumSim.getnqubits()
        for x in phi_in:
            if x == '1':
                index_phi_vec += pow(2, n) // 2
            n -= 1

        #   Die Quantenschaltung soll mit der Eingabe initialisiert werden, daher ist nur dieser eine Zustand mit der
        #   Wahrscheinlichkeit 1 vorhanden.
        self.phi_vec[index_phi_vec] = 1.+0.j

        super().__init__()

    #   Über print(qstate_object) werden alle möglichen Zustände und Wahrscheinlichkeiten ausgegeben
    def __str__(self):
        """Ausgabe alle möglichen Zustände und zugehörigen Wahrscheinlichkeiten"""

        return_str = ''
        index = 0

        #   Ausgabe für jeden einzelnen Wert ungleich 0, im Zustandsvektor
        for value in self.phi_vec:

            if value != 0. + 0.j:
                #   Umwandlung des Indexes in ein Bitmuster (3 --> 0011)
                diracnotation = getdiracnotation(index, self.getnqubits())
                #   Berechnung der Wahrscheinlichkeit in %
                probability = round(pow(abs(value), 2) * 100, 13)

                return_str += 'Der Zustand {} hat die Wahrscheinlichkeit von {}%.\n'.format(diracnotation, probability)

            index += 1

        return return_str
