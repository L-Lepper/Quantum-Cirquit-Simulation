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
    Element ist Tupel mit Gatter und betreffendes Qbit.
    Die Funktion add_tuple_to_operation_list fügt weitere Elemente der Lliste hinzu.
    """

    def __init__(self):
        """
        Konstruktor erstellt Vorlage für Operation_List, und legt Datentyp fest.
        """

        #   Variable wird benötigt, um sich zu merken, ob die Funktion add_tuple_to_operation_list schon mal ausgeführt
        #   wurde
        self.call_function_first_time = True

        #   Erstelle Prototyp für die Liste
        self.list_tuple_operation_qubit_i = np.empty_like([('X', 0)])

        super().__init__()

    def add_tuple_to_operation_list(self, tuple_operation_qbit_i):
        """
        Fügt der Liste list_tuple_operation_qubit_i ein Tuple mit einem Objekt aus der Unterklasse von QGate, und
        dem Index von einem Qubit, auf das die Operation angewendet werden soll, hinzu. Die Unterklassen bestehen aus
        den Klassen der verschiedenen Gatter und einer Klasse für die Messung.

        :param tuple_operation_qbit_i: Tupel (Gatter/Messung , Index des betreffenden Qubits)
        :return self: Operation_Objekt indem die Liste gespeichert ist
        """

        #   Wird die Funktion das erste Mal aufgerufen, wird das erste Element des Prototyps überschrieben, welches
        #   den Datentyp festgelegt hat
        if self.call_function_first_time:
            self.list_tuple_operation_qubit_i = np.array(tuple_operation_qbit_i)
            self.call_function_first_time = False
        #   Sonst wird einfach ein Tupel angehängt
        else:
            self.list_tuple_operation_qubit_i = np.append(self.list_tuple_operation_qubit_i, tuple_operation_qbit_i, 0)

        return self
