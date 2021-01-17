#   Projektarbeit "Recherche und Tool zur Simulation von Quantenschaltungen im Bereich Quantencomputing"
#   Author: Lukas Lepper, 24.11.2020
#   Betreuer: Dipl.-Ing. Martin Hardieck
#   Dateiname: Operation.py
#   Version: 0.6


import numpy as np
from Base import Base


class Operation(Base):
    """
    Diese Klasse enhält die Quantenschaltung in Form einer Liste mit allen Operationen (seriell): Reihenfolge in der
    Gatter angewendet werden. Ein Element kann eine Liste mit Gatter und betreffenden Qbits sein, aber auch andere
    Befehle wie print state_vec, um an einer bestimmten Stelle den aktuellen Zustand auszugeben.
    Die Funktion add_operation_to_list fügt weitere Elemente der Liste hinzu.
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
