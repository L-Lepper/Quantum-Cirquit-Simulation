#   Projektarbeit Literaturrecherche zu Simulationsalgorithmen für Quantencomputing
#   Author: Lukas Lepper, 14.12.2020
#   Betreuer: Martin Hardieck
#   Dateiname: G_Rotation.py
#   Version: 0.6


import numpy as np
from QGate import QGate
import cmath


class Rotation(QGate):
    """
    Klasse für das algemeine Rotations-Gatter. Rotation um phi und theta. Speichert den Typ und erweitert die Matrix
    dieses Gatters auf Größe des Zustandsvektors.
    """

    def __init__(self, list_affected_qubits, list_of_parameters):
        """
        Konstruktor erstellt Matrix in der Größe der Quantenschaltung (Anzahl der Qubits), die das Gatter auf ein
        bestimmtes Qubit beschreibt.

        :param list_affected_qubits: Index des Qubits, auf welches das Gatter angewendet wird
        :param list_of_parameters: Liste der Parameter, hier die Winkel Theta und Phi.
        """

        #   list_affected_qubits wird in der Elternklasse in qsim_obj.list_affected_qubits gespeichert
        super().__init__(list_affected_qubits)
        theta = list_of_parameters[0]
        phi = list_of_parameters[1]

        #   Bezeichnung des Gatters
        self.type = 'r'

        #   Spezifische Matrix des Gatters
        self.general_matrix = np.array([[cmath.cos(theta / 2), -1j * cmath.exp(-1j * phi) * cmath.sin(theta / 2)],
                                        [-1j * cmath.exp(1j * phi) * cmath.sin(theta / 2), cmath.cos(theta / 2)]], dtype=complex)

        #   Die Matrix wird auf die Größe der Quantenschaltung erweitert
        self.general_matrix = self.expandmatrix(self.getnqubits(), list_affected_qubits[0])
