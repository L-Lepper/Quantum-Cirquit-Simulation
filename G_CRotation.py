#   Projektarbeit "Recherche und Tool zur Simulation von Quantenschaltungen im Bereich Quantencomputing"
#   Author: Lukas Lepper, 12.01.2021
#   Betreuer: Dipl.-Ing. Martin Hardieck
#   Dateiname: G_CRotation.py
#   Version: 1.0


import numpy as np
import cmath
from QGate import QGate


class CRotation(QGate):
    """
    Klasse für das CRotations Gatter. Speichert den Typ und erweitert die Matrix dieses Gatters auf Größe des
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
        self.type = 'cr'

        #   Werte, die im Konstruktor mehrmals verwendet werden
        n_qubits = self.getnqubits()
        q_control = list_affected_qubits[0]
        q_target = list_affected_qubits[1]
        theta = list_of_parameters[0]
        phi = list_of_parameters[1]

        #   Um die spezifische Matrix des CRotations Gatters in Abhängigkeit des Kontroll- und Zielqubits aufzubauen, wird
        #   eine 0_Matrix in der richtigen Größe erstellt
        self.general_matrix = np.zeros([pow(2, n_qubits), pow(2, n_qubits)], dtype=complex)

        #   Entsprechend des Kontroll- und Zielqubits sollen 1en an die richtigen Stellen der Matrix gesetzt werden.
        #   Es entsteht eine Matrix, die das CRotations Gate für die aktuelle Anzahl an Qubits und den betreffenden Qubits
        #   beschreibt.
        for i in range(pow(2, n_qubits)):

            #   Für jede Ebene in der Matrix (Anzahl der Ebenen = n_qubits) wird der Index der Ebene, der identisch mit
            #   dem Index im Zustandsvektor ist, in eine binäre Zahl umgewandelt. Diese wird in einer Liste gespeichert
            #   und mit führenden 0en, entsprechend der Differenz der Anzahl an Zustände und der Länge der binären Zahl,
            #   ergänzt.
            #   Die binäre Zahl beschreibt den Zustand im Zustandsvektor.
            bit_pattern = (n_qubits - len( list(bin(i)[2:]) )) * ['0'] + list(bin(i)[2:])

            #   Es wird geprüft ob die Liste, die einen Zustand beschreibt, an der Stelle wo das Kontrollqubit ist 1
            #   ist.
            if bit_pattern[q_control] == '1':

                #   Ist das Kontrollqubit 1, wird auf der Diagonale der Matrix der cos Wert gespeichert (Abbildung von
                #   0 nach 0 und von 1 nach 1 wird in der Matrix durch den cos beschrieben)
                self.general_matrix[i][i] = cmath.cos(theta / 2)

                #   Die Sinus Abbildung erfolgt an den Stellen in der Matrix, wo das Zielqubit von 0 nach 1 oder von 1
                #   nach 0 abgebildet wird.
                if bit_pattern[q_target] == '0':
                    #   Ist das aktuelle Bitmuster an der Stelle des Zielqubits 0, wird das Bitmuster dort auf 1 geändert
                    bit_pattern[q_target] = '1'

                    #   Wandle geänderte Bitmuster in eine ganze Zahl um 0*2^3 + 1*2^2 + 1*2^1 + 0*2^0
                    j = 0
                    for index, x in enumerate(bit_pattern):
                        #   n_qubits - 1, da 3,2,1,0 gezählt werden soll und nicht 4,3,2,1
                        j += int(x) * int(pow(2, n_qubits - index - 1))

                    #   Diese Zahl aus dem geänderten Bitmuster gibt nun den Index in der Matrix an, wo die Abbildung
                    #   0 nach 1 für das Zielqubit steht.
                    self.general_matrix[i][j] = -1j * cmath.exp(-1j * phi) * cmath.sin(theta / 2)

                else:
                    #   Andernfalls ist der Zustand für das Zielqubit im Bitmuster 1. Dann wird die Stelle in der Matrix
                    #   gesucht, wo für das Zielqubit die Abbildung von 1 nach 0 erfolgt. Dazu wir das Bitmuster an der
                    #   Stelle auf 0 geändert.
                    bit_pattern[q_target] = '0'

                    #   Wandle geänderte Bitmuster in eine ganze Zahl um 0*2^3 + 1*2^2 + 1*2^1 + 0*2^0
                    j = 0
                    for index, x in enumerate(bit_pattern):
                        #   n_qubits - 1, da 3,2,1,0 gezählt werden soll und nicht 4,3,2,1
                        j += int(x) * int(pow(2, n_qubits - index - 1))

                    # Die Zahl aus dem geänderten Bitmuster gibt jetzt den Index an, wo für das Zielqubit die Abbildung
                    # 1 nach 0 in der Matrix steht.
                    self.general_matrix[i][j] = -1j * cmath.exp(1j * phi) * cmath.sin(theta / 2)


            #   Ist das Kontrollqubit 0, wird auf der Diagonalen der Matrix eine 1 gespeichert, Die Zustände wo dies
            #   gilt, werden nicht verändert. --> Abbildung 1 nach 1 oder 0 nach 0
            else:
                self.general_matrix[i][i] = 1
