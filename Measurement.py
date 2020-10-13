#   Projektarbeit Literaturrecherche zu Simulationsalgorithmen für Quantencomputing
#   Author: Lukas Lepper, 14.09.2020
#   Betreuer: Martin Hardieck
#   Dateiname: DDEdge.py
#   Version: 0.4

import cmath
import numpy as np
import random
from copy import deepcopy
from Base import Base
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

        if Base.get_debug():
            print('\n\n\n\t\t---------- komplexeres Beispiel ----------\n\n')
            remember_old_number_qubits = Base.getnqubits()
            #Base.set_n_qubits(3)
            #arr = np.array([2, 2, 4, 4, 6, 6, 12, 12])
            #arr = np.array([[5,7,1,0,6,4,5,0],[8,7,2,3,0,1,7,6],[1,0,5,7,3,8,4,0],[2,3,8,7,7,9,3,1],[0,0,0,0,0,7,1,0],[0,0,0,0,8,7,2,3],[0,0,0,0,1,0,5,7],[0,0,0,0,2,3,8,7]])
            Base.set_n_qubits(4)
            arr = np.array([0.3082207, 0.054772256, 0.176068169, 0.242899156, 0.3082207, 0.054772256, 0.223606798, 0.346410162, 0.3082207, 0.054772256, 0.223606798, 0.346410162, 0.262678511, 0.262678511, 0.262678511, 0.262678511])
            #arr = np.array([-0.25364695+0.535476894j, -0.366378928+0j, 0+0j, 0.591842883-0.028182994j, 0.140914972+0.028182994j, 0.056365989+0.084548983j, 0.084548983+0.140914972j, -0.056365989+0.084548983j, 0.084548983-0.140914972j, -0.056365989-0.084548983j, 0.028182994-0.056365989j, 0.056365989+0.056365989j, 0.084548983-0.140914972j, -0.056365989-0.084548983j, 0.028182994-0.056365989j, 0.056365989+0.056365989j])
            # Base.set_n_qubits(4)
            # arr = np.array([1, 2, 2, 5, 2, 1, 5, 1, 1, 2, 2, 5, 0, 0, 5, 0])
            # Base.set_n_qubits(2)
            # arr = np.array([1, 0, 0, 0])
            # arr = np.array([0, 0, 0, 0])


            self.state_vec_to_measure = arr

            self.state_dd_object = DecisionDiagram(arr)

            #   Berechne alle Wahrscheinlichkeiten, wenn das Entscheidungsdiagramm einen Zustandsvektor darstellt.
            #   Für Matrizen sind die Ergebnisse der Berechnung nutzlos...
            self.state_dd_object.calc_probabilities_if_vector()

                # ----------
            #   Gebe eingegebene und ausgelesene Matrix/Vektor aus
            if Base.get_debug():
                print('\nEingegebener Vektor/Matrix:\n', arr)
                #   Erstelle Matrix/Vektor aus Entscheidungsdiagramm
                print('\nAusgelesener Vektor/Matrix:\n', self.state_dd_object.create_matrix(), '\n')
                # ----------

            print('Gemessenes Qubit:', self.qubit_to_measure)
            print('Ursprünglicher Zustandsvektor:\n', arr)
            print('Zustandsvektor nach der Messung:\n', self.measure())
            Base.set_n_qubits(remember_old_number_qubits)
            print('\n\t\t---------- Fortsetzung mit eingegebenen Werten: ----------')


            self.state_vec_to_measure = state_vec_to_measure

            self.state_dd_object = DecisionDiagram(self.state_vec_to_measure)

            #   Berechne alle Wahrscheinlichkeiten, wenn das Entscheidungsdiagramm einen Zustandsvektor darstellt.
            #   Für Matrizen sind die Ergebnisse der Berechnung nutzlos...
            self.state_dd_object.calc_probabilities_if_vector()



        super().__init__(qubit_to_measure)

    def __mul__(self, other):
        return self.measure()

    def measure(self):
        output_state_vec = np.empty_like(self.state_vec_to_measure)

        p_0 = 0
        p_1 = 0
        for node in self.state_dd_object.list_of_all_nodes[self.qubit_to_measure]:
            p_0 += node.list_outgoing_edges[0].edge_probability
            p_1 += node.list_outgoing_edges[1].edge_probability

            # ----------
        if Base.get_debug():
            print('Teste Messung: Wahrscheinlichkeit für Qubit', self.qubit_to_measure, 'gleich 0 + die '
                                                        'Wahrscheinlichkeit für 1, muss 1 ergeben:', p_0 + p_1, '\n')
            # ----------


        random_value = random.randint(0, 1000000) / 1000000

        new_dd_after_measurement_obj = deepcopy(self.state_dd_object)
        if p_0 >= random_value:
            for node in new_dd_after_measurement_obj.list_of_all_nodes[self.qubit_to_measure]:


                edge_0 = node.list_outgoing_edges[0]
                edge_1 = node.list_outgoing_edges[1]

                edge_0.edge_probability = 1
                edge_0.edge_weight /= cmath.sqrt(edge_0.conditional_probability)

                edge_1.edge_probability = 0
                edge_1.conditional_probability = 0
                edge_1.edge_weight = 0
                edge_1.target_node = new_dd_after_measurement_obj.node_zero
                edge_1.n_possible_paths_to_zero = pow(2, Base.getnqubits() - self.qubit_to_measure - 1)
                #edge_1.n_possible_paths_to_zero *= edge_1.count_of_paths
                # ToDo: Lösche den abgeschnittenen Baum
        else:
            for node in new_dd_after_measurement_obj.list_of_all_nodes[self.qubit_to_measure]:
                edge_0 = node.list_outgoing_edges[0]
                edge_1 = node.list_outgoing_edges[1]

                edge_1.edge_probability = 1
                edge_1.edge_weight /= cmath.sqrt(edge_1.conditional_probability)

                edge_0.edge_probability = 0
                edge_0.conditional_probability = 0
                edge_0.edge_weight = 0
                edge_0.target_node = new_dd_after_measurement_obj.node_zero
                edge_0.n_possible_paths_to_zero = pow(2, Base.getnqubits() - self.qubit_to_measure - 1)
                #edge_0.n_possible_paths_to_zero *= edge_1.count_of_paths
                # ToDo: Lösche den abgeschnittenen Baum

        print(new_dd_after_measurement_obj)

        output_state_vec = new_dd_after_measurement_obj.create_matrix()

            # ----------
        #   Ausgabe der Summe aus den gadrierten Beträge der Elemente aus dem Zustandsvektor
        if Base.get_debug():
            sum_entries = 0
            for x in output_state_vec:
                sum_entries += pow(abs(x), 2)
            print('\nPrüfe Normiertheit')
            if p_0 >= random_value:
                print('Qubit', self.qubit_to_measure, 'wurde zu 0 gemessen.')
            else:
                print('Qubit', self.qubit_to_measure, 'wurde zu 1 gemessen.')
            print('Summe der quadrierten Beträge:', sum_entries)
            # ----------


        return output_state_vec
