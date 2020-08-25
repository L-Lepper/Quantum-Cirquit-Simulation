#   Projektarbeit Literaturrecherche zu Simulationsalgorithmen für Quantencomputing
#   Author: Lukas Lepper, 25.08.2020
#   Betreuer: Martin Hardieck
#   Dateiname: Base.py
#   Version: 0.3


class Base:
    """
    Basisklasse, von der alle anderen Klassen direkt oder indirekt erben. Somit können alle Objekte auf die hier
    gespeicherte Anzahl der Qubits zugreifen.
    """

    #   Private Attribute: Zugriff über Funktion / Klassenmethode.
    __nqubits = 0

    def __init__(self):
        pass

    #   get Anzahl der Qubits
    @staticmethod
    def getnqubits():
        return Base.__nqubits

    #   set Anzahl der Qubits
    @staticmethod
    def set_n_qubits(n_qubits):
        Base.__nqubits = n_qubits
