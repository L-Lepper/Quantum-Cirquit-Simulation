#   Projektarbeit "Recherche und Tool zur Simulation von Quantenschaltungen im Bereich Quantencomputing"
#   Author: Lukas Lepper, 24.11.2020
#   Betreuer: Dipl.-Ing. Martin Hardieck
#   Dateiname: G_RotationX.py
#   Version: 0.6


import numpy as np
from QGate import QGate
import math


class RotationX(QGate):
    """
    Klasse für das RX Gatter. Rotation um theta um die X-Achse. Speichert den Typ und erweitert die Matrix dieses Gatters
    auf Größe des Zustandsvektors.
    """

    def __init__(self, list_affected_qubits, list_of_parameters):
        """
        Konstruktor erstellt Matrix in der Größe der Quantenschaltung (Anzahl der Qubits), die das Gatter auf ein
        bestimmtes Qubit beschreibt.

        :param list_affected_qubits: Index des Qubits, auf welches das Gatter angewendet wird
        :param list_of_parameters: Liste der Parameter, hier nur der Winkel Theta.
        """

        #   list_affected_qubits wird in der Elternklasse in qsim_obj.list_affected_qubits gespeichert
        super().__init__(list_affected_qubits)
        theta = list_of_parameters[0]

        #   Bezeichnung des Gatters
        self.type = 'rx'

        #   Spezifische Matrix des Gatters
        self.general_matrix = np.array([[math.cos(theta / 2), -math.sin(theta / 2) * 1j], [-math.sin(theta / 2) * 1j, math.cos(theta / 2)]], dtype=complex)

        #   Die Matrix wird auf die Größe der Quantenschaltung erweitert
        self.general_matrix = self.expandmatrix(self.getnqubits(), list_affected_qubits[0])
