#   Projektarbeit Literaturrecherche zu Simulationsalgorithmen für Quantencomputing
#   Author: Lukas Lepper, 25.08.2020
#   Betreuer: Martin Hardieck
#   Dateiname: Operation.py
#   Version: 0.3


import numpy as np
from Base import Base


class Operation(Base):
    """
    Diese Klasse enhält die Quantenschaltung in Form einer Operation_List: Reihenfolge in der Gatter angewendet werden.
    Ein Element ist eine Liste mit Gatter und betreffenden Qbits.
    Die Funktion add_operation_to_list fügt weitere Elemente der Lliste hinzu.
    """

    def __init__(self):
        """
        Konstruktor erstellt Vorlage für Operation_List, und legt Datentyp fest.
        """

        #   Erstelle Prototyp für die Liste
        self.list_of_operations = []

        super().__init__()

    def add_operation_to_list(self, operation_element):
        """
        Fügt der Liste list_of_operations eine weitere Liste hinzu. Haupsächlich besteht die Liste aus einem
        Gatter und den betreffenden Qubits, sie kann aber auch weitere Befehle wie print enthalten, die nacheinander in
        QuantumSimulation abgearbeitet werden.

        :param operation_element: Liste der einer Operation (Gatter/Messung/Print) und den Indizes der
        betreffenden Qubits)
        :return qsim_obj: Operation_Objekt indem die Liste gespeichert ist
        """

        #   Gültige Eingeben werden bereits im Parsor geprüft, die übergebene Liste sollte verarbeitet werden können.
        self.list_of_operations += operation_element

        return self
