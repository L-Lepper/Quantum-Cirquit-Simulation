#   Projektarbeit Literaturrecherche zu Simulationsalgorithmen für Quantencomputing
#   Author: Lukas Lepper, 30.11.2020
#   Betreuer: Martin Hardieck
#   Dateiname: G_controlledUgate.py
#   Version: 0.6


import numpy as np
from QGate import QGate


class CUgate(QGate):
    """
    Klasse für das allgemeine kontrollierte U-Gatter. Speichert den Typ und erweitert die Matrix dieses Gatters auf
    Größe des Zustandsvektors.
    """

    def __init__(self, list_affected_qubits, qb1_gate_obj):
        """
        Konstruktor erstellt Matrix in der Größe der Quantenschaltung (Anzahl der Qubits), die das Gatter auf ein
        bestimmtes Qubit beschreibt.

        :param list_affected_qubits: Index des Qubits, auf welches das Gatter angewendet wird
        """

        #   list_affected_qubits wird in der Elternklasse in qsim_obj.list_affected_qubits gespeichert
        super().__init__(list_affected_qubits)

        #   Bezeichnung des Gatters setzt sich aus dem c für controlled und der Bezeichnung des ausgewählten Gatters
        #   (X, Y, Z) zusammen.
        self.type = 'c' + qb1_gate_obj.type

        #   Werte, die im Konstruktor mehrmals verwendet werden
        n_qubits = self.getnqubits()
        q_control = list_affected_qubits[0]
        q_target = list_affected_qubits[1]

        #   Um die spezifische Matrix des kontrollierten U-Gatters in Abhängigkeit des Kontroll- und Zielqubits
        #   aufzubauen, wird eine 0_Matrix in der richtigen Größe erstellt
        self.general_matrix = np.zeros([pow(2, n_qubits), pow(2, n_qubits)], dtype=complex)

        #   Entsprechend des Kontroll- und Zielqubits sollen die Werte der U Matrix an die richtigen Stellen der Matrix
        #   gesetzt werden. Es entsteht eine Matrix, die das CNOT Gate für die aktuelle Anzahl an Qubits und den
        #   betreffenden Qubits beschreibt.
        for i in range(pow(2, n_qubits)):

            #   Für jede Ebene in der Matrix (Anzahl der Ebenen = n_qubits) wird der Index der Ebene, der identisch mit
            #   dem Index im Zustandsvektor ist, in eine binäre Zahl umgewandelt. Diese wird in einer Liste gespeichert
            #   und mit führenden 0en, entsprechend der Differenz der Anzahl an Zustände und der Länge der binären Zahl,
            #   ergänzt.
            #   Die binäre Zahl beschreibt den Zustand im Zustandsvektor.
            bit_pattern = (n_qubits - len( list(bin(i)[2:]) )) * ['0'] + list(bin(i)[2:])

            #   Ist das Kontrollqubit 1, werden in dieser Ebene an den Stellen der Kontroll und Zielqubits die Matrix-
            #   einträge des ausgewählten U-Gaters gespeichert.
            if bit_pattern[q_control] == '1':

                #   Ist das Zielqubit 0, werden U_00 und U_01 gespeichert
                if bit_pattern[q_target] == '0':

                    self.general_matrix[i][i] = qb1_gate_obj.general_matrix[0][0]

                    bit_pattern[q_target] = '1'

                    #   Wandle geänderte Bitmuster in eine ganze Zahl um 0*2^3 + 1*2^2 + 1*2^1 + 0*2^0
                    j = 0
                    for index, x in enumerate(bit_pattern):
                        #   n_qubits - 1, da 3,2,1,0 gezählt werden soll und nicht 4,3,2,1
                        j += int(x) * int(pow(2, n_qubits - index - 1))

                    self.general_matrix[i][j] = qb1_gate_obj.general_matrix[0][1]

                #   Ist das Zielqubits 1, werden U_10 und U_11 gespeichert
                else:

                    self.general_matrix[i][i] = qb1_gate_obj.general_matrix[1][1]

                    bit_pattern[q_target] = '0'

                    #   Wandle geänderte Bitmuster in eine ganze Zahl um 0*2^3 + 1*2^2 + 1*2^1 + 0*2^0
                    j = 0
                    for index, x in enumerate(bit_pattern):
                        #   n_qubits - 1, da 3,2,1,0 gezählt werden soll und nicht 4,3,2,1
                        j += int(x) * int(pow(2, n_qubits - index - 1))

                    self.general_matrix[i][j] = qb1_gate_obj.general_matrix[1][0]

            else:
                #   Die Zahl j gibt jetzt den Index in der aktuellen Ebene an, wo eine 1 gespeichert werden soll.
                #   Würde das Bitmuster nicht verändert werden, wäre j immer i, sodass am Ende eine Diagonalmatrix
                #   heraus kommen würde.
                self.general_matrix[i][i] = 1
