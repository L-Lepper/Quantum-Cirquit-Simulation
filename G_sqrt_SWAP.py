#   Projektarbeit Literaturrecherche zu Simulationsalgorithmen für Quantencomputing
#   Author: Lukas Lepper, 26.11.2020
#   Betreuer: Martin Hardieck
#   Dateiname: G_sqrt_SWAP.py
#   Version: 0.6


import numpy as np
import math
from QGate import QGate


class sqrtSwap(QGate):
    """
    Klasse für das sqrtSwap Gatter. Speichert den Typ und erweitert die Matrix dieses Gatters auf Größe des
    Zustandsvektors.
    """

    def __init__(self, list_affected_qubits):
        """
        Konstruktor erstellt Matrix in der Größe der Quantenschaltung (Anzahl der Qubits), die das Gatter auf ein
        bestimmtes Qubit beschreibt.

        :param list_affected_qubits: Index des Qubits, auf welches das Gatter angewendet wird
        """

        #   list_affected_qubits wird in der Elternklasse in qsim_obj.list_affected_qubits gespeichert
        super().__init__(list_affected_qubits)

        #   Bezeichnung des Gatters
        self.type = 'sqrt_swap'

        #   Werte, die im Konstruktor mehrmals verwendet werden
        n_qubits = self.getnqubits()
        index_1 = list_affected_qubits[0]
        index_2 = list_affected_qubits[1]

        #   Um die spezifische Matrix des Swap-Gatters in Abhängigkeit der zu teuschenden Qubits aufzubauen, wird
        #   eine 0_Matrix in der richtigen Größe erstellt
        self.general_matrix = np.zeros([pow(2, n_qubits), pow(2, n_qubits)], dtype=complex)

        #   Entsprechend der Qubits sollen 1en an die richtigen Stellen der Matrix gesetzt werden.
        #   Es entsteht eine Matrix, die das sqrtSwap-Gatter für die aktuelle Anzahl an Qubits und den betreffenden
        #   Qubits beschreibt.
        for i in range(pow(2, n_qubits)):

            #   Für jede Ebene in der Matrix (Anzahl der Ebenen = n_qubits) wird der Index der Ebene, der identisch mit
            #   dem Index im Zustandsvektor ist, in eine binäre Zahl umgewandelt. Diese wird in einer Liste gespeichert
            #   und mit führenden 0en, entsprechend der Differenz der Anzahl an Zustände und der Länge der binären Zahl,
            #   ergänzt.
            #   Die binäre Zahl beschreibt den Zustand im Zustandsvektor.
            bit_pattern = (n_qubits - len( list(bin(i)[2:]) )) * ['0'] + list(bin(i)[2:])

            #   Es wird geprüft, ob die Zustande der beiden Qubits ungleich sind, dann werden ihre Zustände getauscht
            if bit_pattern[index_1] != bit_pattern[index_2]:

                #   Auf der Diagonale bei dem Index, wo beide Kontrollqubits 1 sind, hat die Matrix den Wert
                #   cos(theta)*1j
                self.general_matrix[i][i] = 0.5 + 0.5j

                #   Falls der Index der aktuellen Ebene, also der Index im Zustand, identisch ist mit index_1, wird der
                #   konjugiert komplexe Anteil bei index_2 gespeichert, sonst umgekehrt.
                bit_pattern[index_1], bit_pattern[index_2] = bit_pattern[index_2], bit_pattern[index_1]

                #   Wandle geändertes Bitmuster in eine ganze Zahl um 0*2^3 + 1*2^2 + 1*2^1 + 0*2^0
                #   Sie gibt den Index an, bei dem in der Matrix auf der aktuellen Ebene die Abbildung des oben
                #   gesuchten Zustand, mit dem invertierten Zielqubit, auf den aktuellen Zustand repräsentiert wird.
                j = 0
                for index, x in enumerate(bit_pattern):
                    #   n_qubits - 1, da 3,2,1,0 gezählt werden soll und nicht 4,3,2,1
                    j += int(x) * int(pow(2, n_qubits - index - 1))

                self.general_matrix[i][j] = 0.5 - 0.5j

            else:
                self.general_matrix[i][i] = 1
