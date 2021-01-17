#   Projektarbeit "Recherche und Tool zur Simulation von Quantenschaltungen im Bereich Quantencomputing"
#   Author: Lukas Lepper, 30.11.2020
#   Betreuer: Dipl.-Ing. Martin Hardieck
#   Dateiname: G_controlledRphi.py
#   Version: 0.6


import numpy as np
import cmath
from QGate import QGate


class CRphi(QGate):
    """
    Klasse für das kontrollierte R-Gatter. Speichert den Typ und erweitert die Matrix dieses Gatters auf Größe des
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
        self.type = 'cp'

        #   Werte, die im Konstruktor mehrmals verwendet werden
        n_qubits = self.getnqubits()
        q_control = list_affected_qubits[0]
        q_target = list_affected_qubits[1]
        phi = list_of_parameters[0]

        #   Um die spezifische Matrix des Toffoli-Gatters in Abhängigkeit der Kontroll- und Zielqubits aufzubauen, wird
        #   eine 0_Matrix in der richtigen Größe erstellt
        self.general_matrix = np.zeros([pow(2, n_qubits), pow(2, n_qubits)], dtype=complex)

        #   Entsprechend der Kontroll- und Zielqubits sollen 1en, oder e^phi*j an die richtigen Stellen in der Matrix
        #   gesetzt werden. Es entsteht eine Matrix, die das kontrollierte Rphi Gate für die aktuelle Anzahl an
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
            if bit_pattern[q_control] == '1' and bit_pattern[q_target] == '1':

                #   Auf der Diagonale bei dem Index, wo das Kontrollqubit und das Zielqubits 1 sind, hat die Matrix den
                #   Wert e^phi*j
                self.general_matrix[i][i] = cmath.exp(phi * 1j)

            else:
                self.general_matrix[i][i] = 1
