#   Projektarbeit Literaturrecherche zu Simulationsalgorithmen für Quantencomputing
#   Author: Lukas Lepper, 25.08.2020
#   Betreuer: Martin Hardieck
#   Dateiname: PauliZ.py
#   Version: 0.3


import numpy as np
from QGate import QGate


class PauliZ(QGate):
    """
    Klasse für das Pauli-Z Gatter. Speichert den Typ und erweitert die Matrix dieses Gatters auf Größe des
    Zustandsvektors.
    """

    def __init__(self, list_affected_qubits):
        """
        Konstruktor erstellt Matrix in der Größe der Quantenschaltung (Anzahl der Qubits), die das Gatter auf ein
        bestimmtes Qubit beschreibt.

        :param list_affected_qubits: Index des Qubits, auf welches das Gatter angewendet wird
        """

        #   list_affected_qubits wird in der Elternklasse in self.list_affected_qubits gespeichert
        super().__init__(list_affected_qubits)

        #   Bezeichnung des Gatters
        self.type = 'z'

        #   Spezifische Matrix des Gatters
        self.general_matrix = np.array([[1, 0], [0, -1]], dtype=complex)

        #   Die Matrix wird auf die Größe der Quantenschaltung erweitert
        self.general_matrix = self.expandmatrix(self.getnqubits(), list_affected_qubits[0])
