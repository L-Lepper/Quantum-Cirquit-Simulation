#   Projektarbeit "Recherche und Tool zur Simulation von Quantenschaltungen im Bereich Quantencomputing"
#   Author: Lukas Lepper, 30.11.2020
#   Betreuer: Dipl.-Ing. Martin Hardieck
#   Dateiname: G_RotationZ.py
#   Version: 0.6


import numpy as np
from QGate import QGate
import cmath


class RotationZ(QGate):
    """
    Klasse für das RZ Gatter. Rotation des Winkels Phi um die Z-Achse. Speichert den Typ und erweitert die Matrix
    dieses Gatters auf Größe des Zustandsvektors.
    """

    def __init__(self, list_affected_qubits, list_of_parameters):
        """
        Konstruktor erstellt Matrix in der Größe der Quantenschaltung (Anzahl der Qubits), die das Gatter auf ein
        bestimmtes Qubit beschreibt.

        :param list_affected_qubits: Index des Qubits, auf welches das Gatter angewendet wird
        :param list_of_parameters: Winkel Phi, um den das Qubits um die Z-Achse gedreht wird.
        """

        #   list_affected_qubits wird in der Elternklasse in qsim_obj.list_affected_qubits gespeichert
        super().__init__(list_affected_qubits)

        #   Bezeichnung des Gatters
        self.type = 'rz'

        phi = list_of_parameters[0]

        #   Spezifische Matrix des Gatters
        self.general_matrix = np.array([[cmath.exp(phi / 2 * -1j), 0], [0, cmath.exp(phi / 2 * 1j)]],
                                       dtype=complex)

        #   Die Matrix wird auf die Größe der Quantenschaltung erweitert
        self.general_matrix = self.expandmatrix(self.getnqubits(), list_affected_qubits[0])
