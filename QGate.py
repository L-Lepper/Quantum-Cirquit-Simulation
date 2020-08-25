#   Projektarbeit Literaturrecherche zu Simulationsalgorithmen für Quantencomputing
#   Author: Lukas Lepper, 25.08.2020
#   Betreuer: Martin Hardieck
#   Dateiname: QGate.py
#   Version: 0.3


import numpy as np
from QMatrix import QMatrix


class QGate(QMatrix):
    """
    Klasse für Operationen: Gatter und Messung. Speichert Qubit auf welches die Operation angewendet wird und hat eine
    Funktion mit der eine Matrix auf die Größe des Zustandsvektors erweitert werden kann.
    """

    def __init__(self, qubit_to_change):
        """
        Default-Konstruktor: Speichert welches Qubits betrachtet wird

        :param qubit_to_change: Index des zu verändernden Qubits
        """
        self.qubitToChange = qubit_to_change
        super().__init__()

    def expandmatrix(self, n_qubits, qubittochange):
        """
        U-Matrix (=general_matrix) des Gatters wird mit Idenditätsmatritzen auf alle Qubits erweitert.

        :param n_qubits: Anzahl der Qubits in der Quantenschaltung
        :param qubittochange: Index des Qubit, auf welches die Operation angewendet werden soll
        :return expmatrix: Mit Identitätsmatrix erweiterte Matrix
        """

        #   Auffüllen mit Idenditätsmatrizen durch Kronecker-Produkt bis spezifischem Gatter
        expmatrix = np.kron(np.identity(pow(2, qubittochange)), self.general_matrix)
        #   Auffüllen mit Idenditätsmatrizen nach spez. Gatter bis zum letzten Qubit
        expmatrix = np.kron(expmatrix, np.identity(pow(2, n_qubits - qubittochange - 1)))

        return expmatrix
