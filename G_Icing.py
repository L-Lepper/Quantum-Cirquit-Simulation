#   Projektarbeit Literaturrecherche zu Simulationsalgorithmen für Quantencomputing
#   Author: Lukas Lepper, 30.11.2020
#   Betreuer: Martin Hardieck
#   Dateiname: G_Icing.py
#   Version: 0.6


import numpy as np
import math
from QGate import QGate


class IcingGate(QGate):
    """
    Klasse für das Icing Gatter (XX, YY oder ZZ). Speichert den Typ und erweitert die Matrix dieses Gatters auf Größe des
    Zustandsvektors.
    """

    def __init__(self, list_affected_qubits, list_of_parameters, int_in):
        """
        Konstruktor erstellt Matrix in der Größe der Quantenschaltung (Anzahl der Qubits), die das Gatter auf ein
        bestimmtes Qubit beschreibt.

        :param list_affected_qubits: Index des Qubits, auf welches das Gatter angewendet wird
        """

        #   list_affected_qubits wird in der Elternklasse in qsim_obj.list_affected_qubits gespeichert
        super().__init__(list_affected_qubits)

        #   Bezeichnung des Gatters
        if int_in == 0:
            self.type = 'xx'
        elif int_in == 1:
            self.type = 'yy'
        else:
            self.type = 'zz'

        #   Werte, die im Konstruktor mehrmals verwendet werden
        n_qubits = self.getnqubits()
        q_index_1 = list_affected_qubits[0]
        q_index_2 = list_affected_qubits[1]
        phi = list_of_parameters[0]

        #   Um die spezifische Matrix des CNOT Gatters in Abhängigkeit des Kontroll- und Zielqubits aufzubauen, wird
        #   eine 0_Matrix in der richtigen Größe erstellt
        self.general_matrix = np.zeros([pow(2, n_qubits), pow(2, n_qubits)], dtype=complex)

        #   Entsprechend des Kontroll- und Zielqubits sollen 1en an die richtigen Stellen der Matrix gesetzt werden.
        #   Es entsteht eine Matrix, die das CNOT Gate für die aktuelle Anzahl an Qubits und den betreffenden Qubits
        #   beschreibt.
        for i in range(pow(2, n_qubits)):

            #   Für jede Ebene in der Matrix (Anzahl der Ebenen = n_qubits) wird der Index der Ebene, der identisch mit
            #   dem Index im Zustandsvektor ist, in eine binäre Zahl umgewandelt. Diese wird in einer Liste gespeichert
            #   und mit führenden 0en, entsprechend der Differenz der Anzahl an Zustände und der Länge der binären Zahl,
            #   ergänzt.
            #   Die binäre Zahl beschreibt den Zustand im Zustandsvektor.
            bit_pattern = (n_qubits - len( list(bin(i)[2:]) )) * ['0'] + list(bin(i)[2:])

            if int_in == 0:  # (XX)

                #   Werte auf der Diagonalen
                self.general_matrix[i][i] = math.cos(phi)

                #   Für Qubit 1 und 2 werden die Zustände getauscht, wenn diese unterschiedlich sind.
                #   Wenn beide Zustände gleich sind, werden sie invertiert. Das neue Bitmuster in eine ganze Zahl
                #   umgewandelt, gibt wieder den Index an, beidem besondere Terme des XX Gatters stehen.
                if bit_pattern[q_index_1] != bit_pattern[q_index_2]:
                    bit_pattern[q_index_1], bit_pattern[q_index_2] = bit_pattern[q_index_2], bit_pattern[q_index_1]
                elif bit_pattern[q_index_1] == '0':
                    bit_pattern[q_index_1], bit_pattern[q_index_2] = ['1', '1']
                else:
                    bit_pattern[q_index_1], bit_pattern[q_index_2] = ['0', '0']

                #   Wandle geänderte Bitmuster in eine ganze Zahl um 0*2^3 + 1*2^2 + 1*2^1 + 0*2^0
                j = 0
                for index, x in enumerate(bit_pattern):
                    #   n_qubits - 1, da 3,2,1,0 gezählt werden soll und nicht 4,3,2,1
                    j += int(x) * int(pow(2, n_qubits - index - 1))

                self.general_matrix[i][j] = -1j * math.sin(phi)

            elif int_in == 1:  # (yy)
                #   Werte auf der Diagonalen
                self.general_matrix[i][i] = math.cos(phi)

                #   Für Qubit 1 und 2 werden die Zustände getauscht, wenn diese unterschiedlich sind.
                #   Wenn beide Zustände gleich sind, werden sie invertiert. Das neue Bitmuster in eine ganze Zahl
                #   umgewandelt, gibt wieder den Index an, beidem besondere Terme des XX Gatters stehen.
                if bit_pattern[q_index_1] != bit_pattern[q_index_2]:
                    bit_pattern[q_index_1], bit_pattern[q_index_2] = bit_pattern[q_index_2], bit_pattern[q_index_1]

                    #   Wandle geänderte Bitmuster in eine ganze Zahl um 0*2^3 + 1*2^2 + 1*2^1 + 0*2^0
                    j = 0
                    for index, x in enumerate(bit_pattern):
                        #   n_qubits - 1, da 3,2,1,0 gezählt werden soll und nicht 4,3,2,1
                        j += int(x) * int(pow(2, n_qubits - index - 1))

                    #   Sind beide Zustände unterschiedlich, ist der Eintrag -sin(phi) j
                    self.general_matrix[i][j] = -1j * math.sin(phi)

                #   Sind die Zustände gleich, ist der Eintrag sin(phi) j
                else:
                    if bit_pattern[q_index_1] == '0':
                        bit_pattern[q_index_1], bit_pattern[q_index_2] = ['1', '1']
                    else:
                        bit_pattern[q_index_1], bit_pattern[q_index_2] = ['0', '0']

                    #   Wandle geänderte Bitmuster in eine ganze Zahl um 0*2^3 + 1*2^2 + 1*2^1 + 0*2^0
                    j = 0
                    for index, x in enumerate(bit_pattern):
                        #   n_qubits - 1, da 3,2,1,0 gezählt werden soll und nicht 4,3,2,1
                        j += int(x) * int(pow(2, n_qubits - index - 1))

                    self.general_matrix[i][j] = 1j * math.sin(phi)

            else:  # (zz)
                #   Es befinden sich nur Einträge auf der Diagonalen der Matrix. Sind beide Zustände des Qubits 1 und 2
                #   identisch, wird cos(phi) gespeichert, sonst -cos(phi)
                if bit_pattern[q_index_1] == bit_pattern[q_index_2]:
                    self.general_matrix[i][i] = math.cos(phi)
                else:
                    self.general_matrix[i][i] = -math.cos(phi)
