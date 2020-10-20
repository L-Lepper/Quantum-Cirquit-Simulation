#   Projektarbeit Literaturrecherche zu Simulationsalgorithmen für Quantencomputing
#   Author: Lukas Lepper, 19.10.2020
#   Betreuer: Martin Hardieck
#   Dateiname: Measurement.py
#   Version: 0.5

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
        """
        Erstelle ein Objekt für die Messung, indem der Zustandsvektor, der Index des Qubits und das
        Entscheidungsdiagramm für diesen Vektor gespeichert sind. Für das Entscheidungsdiagramm werden die
        Wahrscheinlichkeiten berechnet.
        :param state_vec_to_measure: Vektor, der im Entscheidungsdiagramm dargestellt wird.
        :param qubit_to_measure: Index des Qubits, welches gemessen wird.
        """

        #   Speichere den zu Messenden Zustandsvektor und den index des Qubits in diesm Objekt
        self.state_vec_to_measure = state_vec_to_measure
        self.qubit_to_measure = qubit_to_measure

        #   Erstelle das Entscheidungsdiagramm mit Kantengewichten
        self.state_dd_object = DecisionDiagram(self.state_vec_to_measure)

        #   Berechne alle Wahrscheinlichkeiten, wenn das Entscheidungsdiagramm einen Zustandsvektor darstellt.
        #   Für Matrizen sind die Ergebnisse der Berechnung nutzlos...
        self.state_dd_object.calc_probabilities_if_vector()

        super().__init__(qubit_to_measure)

    def measure(self):
        """
        Die Funktion erstellt eine echte Kopie von dem Entscheidungsdiagramm state_dd_object, welches gemessen werden
        soll, und misst das Qubit state_vec_to_measure. ToDo gebe das neue Entscheidungsdiagramm zurück oder
        ToDo überschreibe das Originale
        Die einzelnen Schritte, wie die Messung durchgeführt wird, sind in der
        Datei "Anleitung - Entscheidungsdiagramm und Messung - v4.pdf" gespeichert. ToDo: Dateiname überprüfen

        :return output_state_vec: Neuer Zustandsvektor nach der Messung wird zurückgegeben.
        """

        """ Schritt 11 """

        #   ToDo: Ausgabe erfolgt anders(siehe Todo oben)
        print('--------------- Entscheidungsdiagramm vor der Messung ---------------', self.state_dd_object)

        #   Für das zu messende Qubit wird die Wahrscheinlichkeit berechnet für den Zustand 0 oder 1 (Summe der
        #   jeweiligen Äste aller Knoten auf einer Ebene).
        p_0 = 0
        p_1 = 0
        for node in self.state_dd_object.list_of_all_nodes[self.qubit_to_measure]:
            p_0 += node.list_outgoing_edges[0].edge_probability
            p_1 += node.list_outgoing_edges[1].edge_probability

            # ----------
        #   Test, dass die Wahrscheinlichkeit p_0 + p_1 gleich 1 ist.
        if Base.get_debug()[0] and Base.get_debug()[1] == 3:
            print('Teste Messung: Wahrscheinlichkeit für Qubit', self.qubit_to_measure, 'gleich 0 + die '
                                                        'Wahrscheinlichkeit für 1, muss 1 ergeben:', p_0 + p_1, '\n')
            # ----------


        #   Erzeuge eine Zufallszahl zwischen 0 und 1 mit 6 Nachkommastellen
        random_value = random.randint(0, 1000000) / 1000000

        #   Erstelle eine echte Kopie, des originalen Entscheidungsdiagramms
        new_dd_after_measurement_obj = deepcopy(self.state_dd_object)

        #   Falls p_0 größer gleich wie die Zufallszahl ist, wurde das Qubit zu 0 gemessen.
        if p_0 >= random_value:

            """ Schritt 12 """

            #   Für jeden Knoten auf der Ebene des zu messenden Qubits, wird das Entscheidungsdiagramm durch die
            #   Messung angepasst
            for node in new_dd_after_measurement_obj.list_of_all_nodes[self.qubit_to_measure]:

                #   Speichere die linke (0) und die rechte Kante (1)
                edge_0 = node.list_outgoing_edges[0]
                edge_1 = node.list_outgoing_edges[1]

                #   Durch die Messung hat die linke Kante die Wahrscheinlichkeit 1
                edge_0.edge_probability = 1

                """ Schritt 13 """
                #   Normierung des neuen Entscheidungsdiagramms erfolgt durch division des Kantengewichts durch die
                #   Wurzel aus der bedingten Wahrschinlichkeit, mit der dieser Zustand an diesem Knoten eingetreten ist.
                edge_0.edge_weight /= cmath.sqrt(edge_0.conditional_probability)

                #   Die nicht gemessene Kante wird auf den 0-Knoten gezogen, und ihre Eigenschagten entsprechend
                #   angepasst
                edge_1.edge_probability = 0
                edge_1.conditional_probability = 0
                edge_1.edge_weight = 0
                edge_1.target_node = new_dd_after_measurement_obj.node_zero

                #   Anzahl der Kanten, die durch diese Kante dargestellt wird, wird berechnet
                edge_1.n_possible_paths_to_zero = pow(2, Base.getnqubits() - self.qubit_to_measure - 1)
                #   Diese Anzahl wird mit der Häufigkeit multipliziert, mit der die Kante in allen Ästen aufgetreten ist
                edge_1.n_possible_paths_to_zero *= edge_1.count_of_paths

                # ToDo: Lösche den abgeschnittenen Baum

        #   Falls p_0 < als die Zufallszahl, wird der Zustand 1 gemessen
        else:

            """ Schritt 12 """

            #   Für jeden Knoten auf der Ebene des zu messenden Qubits, wird das Entscheidungsdiagramm durch die
            #   Messung angepasst
            for node in new_dd_after_measurement_obj.list_of_all_nodes[self.qubit_to_measure]:

                #   Speichere die linke (0) und die rechte Kante (1)
                edge_0 = node.list_outgoing_edges[0]
                edge_1 = node.list_outgoing_edges[1]

                #   Durch die Messung hat die rechte Kante die Wahrscheinlichkeit 1
                edge_1.edge_probability = 1

                """ Schritt 13 """
                #   Normierung des neuen Entscheidungsdiagramms erfolgt durch division des Kantengewichts durch die
                #   Wurzel aus der bedingten Wahrschinlichkeit, mit der dieser Zustand an diesem Knoten eingetreten ist.
                edge_1.edge_weight /= cmath.sqrt(edge_1.conditional_probability)

                #   Die nicht gemessene Kante wird auf den 0-Knoten gezogen, und ihre Eigenschagten entsprechend
                #   angepasst
                edge_0.edge_probability = 0
                edge_0.conditional_probability = 0
                edge_0.edge_weight = 0
                edge_0.target_node = new_dd_after_measurement_obj.node_zero

                #   Anzahl der Kanten, die durch diese Kante dargestellt wird, wird berechnet
                edge_0.n_possible_paths_to_zero = pow(2, Base.getnqubits() - self.qubit_to_measure - 1)
                #   Diese Anzahl wird mit der Häufigkeit multipliziert, mit der die Kante in allen Ästen aufgetreten ist
                edge_0.n_possible_paths_to_zero *= edge_1.count_of_paths

                # ToDo: Lösche den abgeschnittenen Baum

        #   ToDo: Ausgabe erfolgt anders(siehe Todo oben)
        print('--------------- Entscheidungsdiagramm nach der Messung ---------------', new_dd_after_measurement_obj)

        """ Schritt 14 """
        #   Aus dem neuen Entscheidungsdiagramm wird ein Vektor ausgelesen
        output_state_vec = new_dd_after_measurement_obj.create_matrix()

        #   ToDo: Ausgabe erfolgt anders(siehe Todo oben)
            # ----------
        #   Ausgabe der Summe aus den gadrierten Beträge der Elemente aus dem Zustandsvektor
        if Base.get_debug()[0] and Base.get_debug()[1] == 3:
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
