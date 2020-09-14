#   Projektarbeit Literaturrecherche zu Simulationsalgorithmen für Quantencomputing
#   Author: Lukas Lepper, 14.09.2020
#   Betreuer: Martin Hardieck
#   Dateiname: DDEdge.py
#   Version: 0.4

import cmath
import numpy as np
from QGate import QGate
from DecisionDiagram import DecisionDiagram


class Measurement(QGate):
    """
    Klasse zur Durchführung einer Messung an einem Qubit und zum Berechnen des aus der Messung
    resultierenden Zustandsvektors.
    """

    def __init__(self, state_vec_to_measure, qubit_to_measure):
        #self.state_vec_to_measure = np.array([0, 1/cmath.sqrt(2), 0, 0, 0, 1/2, 1/cmath.sqrt(8), 1/cmath.sqrt(8)])
        self.state_vec_to_measure = state_vec_to_measure
        self.qubit_to_measure = qubit_to_measure

        self.state_dd_object = DecisionDiagram(self.state_vec_to_measure)
        #self.probability_after_node = self.state_dd_object.dd_with_decision_probability()

        super().__init__(qubit_to_measure)

#    def measure(self):
        output_state_vec = np.empty_like(self.state_vec_to_measure)
#        for x in self.probability_after_node:

            # ToDo: Anhand von Wahrscheinlichkeiten und Rand() eine Entscheidung treffen

#            new_dd_after_measurement_obj = self.state_dd_object
#            i = 0
#            for x in self.state_dd_object.dd:
#                i += 1
#                if x == 0:  # ToDo: Ist in Stuktur von x das Qbit 0 oder 1, entsprechend der Messung zuvor, wird neuer
                    # ToDo: Zustand 0 gesetzt
#                    new_dd_after_measurement_obj.dd[i] = 0

#            output_state_vec = DecisionDiagram.create_vector_from_dd(new_dd_after_measurement_obj.dd)

#        return output_state_vec
