#   Projektarbeit "Recherche und Tool zur Simulation von Quantenschaltungen im Bereich Quantencomputing"
#   Author: Lukas Lepper, 24.11.2020
#   Betreuer: Dipl.-Ing. Martin Hardieck
#   Dateiname: G_CNOT.py
#   Version: 0.6


import numpy as np
from QGate import QGate


class CNOT(QGate):
    """
    Klasse für das CNOT Gatter. Speichert den Typ und erweitert die Matrix dieses Gatters auf Größe des
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
        self.type = 'cnot'

        #   Werte, die im Konstruktor mehrmals verwendet werden
        n_qubits = self.getnqubits()
        q_control = list_affected_qubits[0]
        q_target = list_affected_qubits[1]

        #   Um die spezifische Matrix des CNOT Gatters in Abhängigkeit des Kontroll- und Zielqubits aufzubauen, wird
        #   eine 0_Matrix in der richtigen Größe erstellt
        self.general_matrix = np.zeros([pow(2, n_qubits), pow(2, n_qubits)])

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

            #   Es wird geprüft ob die Liste, die einen Zustand beschreibt, an der Stelle wo das Kontrollqubit ist 1
            #   ist.
            if bit_pattern[q_control] == '1':

                #   Entsprechend dem Verhalten eines CNOT Gatters wird an der Stelle des Zielqubit der Zustand
                #   invertiert
                if bit_pattern[q_target] == '0':
                    bit_pattern[q_target] = '1'
                else:
                    bit_pattern[q_target] = '0'

            #   Wandle geänderte Bitmuster in eine ganze Zahl um 0*2^3 + 1*2^2 + 1*2^1 + 0*2^0
            j = 0
            for index, x in enumerate(bit_pattern):

                #   n_qubits - 1, da 3,2,1,0 gezählt werden soll und nicht 4,3,2,1
                j += int(x) * int( pow(2, n_qubits - index - 1) )

            #   Die Zahl j gibt jetzt den Index in der aktuellen Ebene an, wo eine 1 gespeichert werden soll.
            #   Würde das Bitmuster nicht verändert werden, wäre j immer i, sodass am Ende eine Diagonalmatrix heraus
            #   kommen würde. Da das CNOT aber das Bitmuster verändert, die Indizes sozusagen vertauscht, bekommt man
            #   die Matrix, welche das aktuelle CNOT Gate beschreibt.
            self.general_matrix[i][j] = 1
