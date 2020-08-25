#   Projektarbeit Literaturrecherche zu Simulationsalgorithmen für Quantencomputing
#   Author: Lukas Lepper, 25.08.2020
#   Betreuer: Martin Hardieck
#   Dateiname: PauliX.py
#   Version: 0.3


import numpy as np
from QGate import QGate


class PauliX(QGate):
    """
    Klasse für das Pauli-X Gatter. Speichert den Typ und erweitert die Matrix dieses Gatters auf Größe des
    Zustandsvektors.
    """

    def __init__(self, qubit_to_change):
        """
        Konstruktor erstellt Matrix in der Größe der Quantenschaltung (Anzahl der Qubits), die das Gatter auf ein
        bestimmtes Qubit beschreibt.

        :param qubit_to_change: Index des Qubits, auf welches das Gatter angewendet wird
        """

        super().__init__(qubit_to_change)
        self.type = 'x'
        self.general_matrix = np.array([[0, 1], [1, 0]], dtype=complex)
        self.general_matrix = self.expandmatrix(self.getnqubits(), qubit_to_change)
