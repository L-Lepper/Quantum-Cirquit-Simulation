#   Projektarbeit Literaturrecherche zu Simulationsalgorithmen für Quantencomputing
#   Author: Lukas Lepper, 25.11.2020
#   Betreuer: Martin Hardieck
#   Dateiname: G_Deutsch.py
#   Version: 0.6


import numpy as np
import cmath
from QGate import QGate


class Deutsch(QGate):
    """
    Klasse für das Deutsch Gatter. Speichert den Typ und erweitert die Matrix dieses Gatters auf Größe des
    Zustandsvektors.
    """

    def __init__(self, list_affected_qubits, list_of_parameters):
        """
        Konstruktor erstellt Matrix in der Größe der Quantenschaltung (Anzahl der Qubits), die das Gatter auf ein
        bestimmtes Qubit beschreibt.

        :param list_affected_qubits: Index des Qubits, auf welches das Gatter angewendet wird
        """

        #   list_affected_qubits wird in der Elternklasse in qsim_obj.list_affected_qubits gespeichert
        super().__init__(list_affected_qubits)

        #   Bezeichnung des Gatters
        self.type = 'deutsch'

        #   Werte, die im Konstruktor mehrmals verwendet werden
        n_qubits = self.getnqubits()
        q_control_1 = list_affected_qubits[0]
        q_control_2 = list_affected_qubits[1]
        q_target = list_affected_qubits[2]
        theta = list_of_parameters[0]

        #   Um die spezifische Matrix des Toffoli-Gatters in Abhängigkeit der Kontroll- und Zielqubits aufzubauen, wird
        #   eine 0_Matrix in der richtigen Größe erstellt
        self.general_matrix = np.zeros([pow(2, n_qubits), pow(2, n_qubits)], dtype=complex)

        #   Entsprechend der Kontroll- und Zielqubits sollen 1en, cos(theta)*1j und sin(theta) an die richtigen Stellen
        #   in der Matrix gesetzt werden. Es entsteht eine Matrix, die das Deutsch Gate für die aktuelle Anzahl an
        #   Qubits und den betreffenden Qubits beschreibt.
        for i in range(pow(2, n_qubits)):

            #   Für jede Ebene in der Matrix (Anzahl der Ebenen = n_qubits) wird der Index der Ebene, der identisch mit
            #   dem Index im Zustandsvektor ist, in eine binäre Zahl umgewandelt. Diese wird in einer Liste gespeichert
            #   und mit führenden 0en, entsprechend der Differenz der Anzahl an Zustände und der Länge der binären Zahl,
            #   ergänzt.
            #   Die binäre Zahl beschreibt den Zustand im Zustandsvektor.
            bit_pattern = (n_qubits - len( list(bin(i)[2:]) )) * ['0'] + list(bin(i)[2:])

            #   Es wird geprüft, ob die Liste die einen Zustand beschreibt an den Stellen wo sich die Kontrollqubits
            #   befinden, 1 ist.
            if bit_pattern[q_control_1] == '1' and bit_pattern[q_control_2] == '1':

                #   Auf der Diagonale bei dem Index, wo beide Kontrollqubits 1 sind, hat die Matrix den Wert
                #   cos(theta)*1j
                self.general_matrix[i][i] = cmath.cos(theta) * 1j

                #   Es wird geprüft, ob das Zielqubit im aktuellen Zustand 0 oder 1 ist. Zu dem aktuellen Zustand wird
                #   der Eintrag im Zustandsvektor an der Stelle wo das Zielqubit invertiert ist, mit sin(theta)
                #   multipliziert und dem aktuellen Zustand hinzugefügt.
                if bit_pattern[q_target] == '0':
                    bit_pattern[q_target] = '1'
                else:
                    bit_pattern[q_target] = '0'

                #   Wandle geändertes Bitmuster in eine ganze Zahl um 0*2^3 + 1*2^2 + 1*2^1 + 0*2^0
                #   Sie gibt den Index an, bei dem in der Matrix auf der aktuellen Ebene die Abbildung des oben
                #   gesuchten Zustand, mit dem invertierten Zielqubit, auf den aktuellen Zustand repräsentiert wird.
                j = 0
                for index, x in enumerate(bit_pattern):
                    #   n_qubits - 1, da 3,2,1,0 gezählt werden soll und nicht 4,3,2,1
                    j += int(x) * int(pow(2, n_qubits - index - 1))

                #   An dieser Stelle in der Matix steht der Wert sin(theta)
                self.general_matrix[i][j] = cmath.sin(theta)
            else:
                self.general_matrix[i][i] = 1
