#   Projektarbeit Literaturrecherche zu Simulationsalgorithmen für Quantencomputing
#   Author: Lukas Lepper, 24.11.2020
#   Betreuer: Martin Hardieck
#   Dateiname: G_negRotationY.py
#   Version: 0.6


import numpy as np
from QGate import QGate
import math


class negRotationY(QGate):
    """
    Klasse für das -RY Gatter. -90°-Rotation um die Y-Achse. Speichert den Typ und erweitert die Matrix dieses Gatters
    auf Größe des Zustandsvektors.
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
        self.type = '-ry'

        #   Spezifische Matrix des Gatters
        self.general_matrix = 1/math.sqrt(2) * np.array([[1, 1], [-1, 1]], dtype=complex)

        #   Die Matrix wird auf die Größe der Quantenschaltung erweitert
        self.general_matrix = self.expandmatrix(self.getnqubits(), list_affected_qubits[0])
