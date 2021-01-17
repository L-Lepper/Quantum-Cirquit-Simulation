#   Projektarbeit "Recherche und Tool zur Simulation von Quantenschaltungen im Bereich Quantencomputing"
#   Author: Lukas Lepper, 24.11.2020
#   Betreuer: Dipl.-Ing. Martin Hardieck
#   Dateiname: G_Hadamard.py
#   Version: 0.6


import numpy as np
import cmath
from QGate import QGate


class HadamardH(QGate):
    """
    Klasse für das Hadarmard Gatter. Speichert den Typ und erweitert die Matrix dieses Gatters auf Größe des
    Zustandsvektors.
    """

    def __init__(self, list_affected_qubits):
        """
        Konstruktor erstellt Matrix in der Größe der Quantenschaltung (Anzahl der Qubits), die das Gatter auf ein
        bestimmtes Qubit beschreibt.

        :param list_affected_qubits: Index des Qubits, auf welches das Gatter angewendet wird
        """

        super().__init__(list_affected_qubits)
        #   Typ und spezifische Matrix des Hadarmard Gatters
        self.type = 'h'
        self.general_matrix = np.array([[1 / cmath.sqrt(2), 1 / cmath.sqrt(2)], [1 / cmath.sqrt(2),
                                                                                 -1 / cmath.sqrt(2)]], dtype=complex)
        #   Erweitere die Matrix auf die Anzahl der Qubits
        self.general_matrix = self.expandmatrix(self.getnqubits(), list_affected_qubits[0])
