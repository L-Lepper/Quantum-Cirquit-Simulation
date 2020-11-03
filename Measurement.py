#   Projektarbeit Literaturrecherche zu Simulationsalgorithmen für Quantencomputing
#   Author: Lukas Lepper, 21.10.2020
#   Betreuer: Martin Hardieck
#   Dateiname: Measurement.py
#   Version: 0.5

import cmath
import random
import numpy as np
from Base import Base
from QGate import QGate
from DecisionDiagram import DecisionDiagram
from DDNode import DDNode


class Measurement(QGate):
    """
    Klasse zur Durchführung einer Messung an einem Qubit und zum Berechnen des aus der Messung
    resultierenden Zustandsvektors.
    """

    def __init__(self, state_vec_to_measure, list_affected_qubits):
        """
        Erstelle ein Objekt für die Messung, indem der Zustandsvektor, der Index des Qubits und das
        Entscheidungsdiagramm für diesen Vektor gespeichert sind. Für das Entscheidungsdiagramm werden die
        Wahrscheinlichkeiten berechnet.
        :param state_vec_to_measure: Vektor, der im Entscheidungsdiagramm dargestellt wird.
        :param list_affected_qubits: Index des Qubits, welches gemessen wird.
        """

        #   Speichere den zu Messenden Zustandsvektor und den index des Qubits in diesm Objekt
        self.state_vec_to_measure = state_vec_to_measure
        self.qubit_to_measure = list_affected_qubits[0]

        #   Erstelle das Entscheidungsdiagramm mit Kantengewichten
        self.state_dd_object = DecisionDiagram(self.state_vec_to_measure)

        #   Berechne alle Wahrscheinlichkeiten, wenn das Entscheidungsdiagramm einen Zustandsvektor darstellt.
        #   Für Matrizen sind die Ergebnisse der Berechnung nutzlos...
        self.state_dd_object.calc_probabilities_if_vector()

        super().__init__(list_affected_qubits)

    def measure(self):
        """
        Die Funktion misst das Qubit state_vec_to_measure.
        Die einzelnen Schritte, wie die Messung durchgeführt wird, sind in der Datei "Anleitung - Entscheidungsdiagramm
         und Messung - v4.pdf" gespeichert. ToDo: Dateiname überprüfen

        :return output_state_vec: Neuer Zustandsvektor nach der Messung wird zurückgegeben.
        """

        """ Schritt 11 """

        #   Ausgabe des Entscheidungsdiagramms vor der Messung
        if Base.get_debug() >= 1:
            print('\n---------------\t Test of measurement \t---------------\n\n'
                  'Decision Diagram before measurement', self.state_dd_object)

        #   Für das zu messende Qubit wird die Wahrscheinlichkeit berechnet für den Zustand 0 oder 1 (Summe der
        #   jeweiligen Äste aller Knoten auf einer Ebene).
        p_0 = 0
        p_1 = 0

        for node in self.state_dd_object.list_of_all_nodes[self.qubit_to_measure]:
            p_0 += node.list_outgoing_edges[0].edge_probability
            p_1 += node.list_outgoing_edges[1].edge_probability

        #   Test, dass die Wahrscheinlichkeit p_0 + p_1 gleich 1 ist.
        if Base.get_debug() == 3:
            print('Testing measurement: the probability for qubit', self.qubit_to_measure,
                  'equal to 0\nin addition with the probability equal to 1 have to be 100%:', p_0*100 + p_1*100, '\n')

        #   Erzeuge eine Zufallszahl zwischen 0 und 1 mit 6 Nachkommastellen
        random_value = random.randint(0, 1000000) / 1000000

        #   Falls p_0 größer gleich wie die Zufallszahl ist, wurde das Qubit zu 0 gemessen.
        node_to_delete = None
        if p_0 >= random_value:

            """ Schritt 12 - 13 """

            #   Für jeden Knoten auf der Ebene des zu messenden Qubits, wird das Entscheidungsdiagramm durch die
            #   Messung angepasst
            for node in self.state_dd_object.list_of_all_nodes[self.qubit_to_measure]:
                #   Speichere die zu 0 und die zu 1 gemessene Kante
                edge_measured_to_0 = node.list_outgoing_edges[1]
                edge_measured_to_1 = node.list_outgoing_edges[0]

                edge_measured_to_0, edge_measured_to_1 = self.update_decision_diagram(edge_measured_to_0,
                                                                                      edge_measured_to_1)
                node.list_outgoing_edges[1] = edge_measured_to_0
                node.list_outgoing_edges[0] = edge_measured_to_1


        else:

            """ Schritt 12 - 13 """

            #   Für jeden Knoten auf der Ebene des zu messenden Qubits, wird das Entscheidungsdiagramm durch die
            #   Messung angepasst
            for node in self.state_dd_object.list_of_all_nodes[self.qubit_to_measure]:
                #   Speichere die zu 0 und die zu 1 gemessene Kante
                edge_measured_to_0 = node.list_outgoing_edges[0]
                edge_measured_to_1 = node.list_outgoing_edges[1]

                edge_measured_to_0, edge_measured_to_1 = self.update_decision_diagram(edge_measured_to_0,
                                                                                      edge_measured_to_1)
                node.list_outgoing_edges[1] = edge_measured_to_0
                node.list_outgoing_edges[0] = edge_measured_to_1

        # Lösche den abgeschnittenen Baum, falls node_to_delete einen Knoten gespeichert hat
        if node_to_delete:
            node_to_delete.delete_node()

        #   Möglicherweise kann jetzt das Entscheidungsdiagramm noch mal zusammengefasst werden
        #   ToDo: Vielleicht lohnt sich der aufwand nicht
        self.state_dd_object.merge_dd_step7()

        #   Für jede Kante wird die Anzahl berechnet, wie häufig sie in den Ästen vorkommt
        #   Dieser Wert muss jetzt aktualisiert werden, da das DD verändert wurde
        self.state_dd_object.list_of_all_edges[0].calc_count_of_paths()
        self.state_dd_object.set_is_calculated_false()

        if Base.get_debug() >= 1:
            print('\nDecision Diagram after measurement\n', self.state_dd_object)

        """ Schritt 14 """
        #   Aus dem neuen Entscheidungsdiagramm wird ein Vektor ausgelesen
        output_state_vec = self.state_dd_object.create_matrix()

        #   Ausgabe der Summe aus den gadrierten Beträge der Elemente aus dem Zustandsvektor
        if Base.get_debug() == 3:
            sum_entries = 0
            for x in output_state_vec:
                sum_entries += pow(abs(x), 2)
            print('Check normalization:')
            if p_0 >= random_value:
                print('Qubit', self.qubit_to_measure, 'was measured to 0.')
            else:
                print('Qubit', self.qubit_to_measure, 'was measured to 1.')
            print('Sum of the squared magnitudes of the state vector:', sum_entries, '\n')
            print('Recursive call of edges and nodes of the decision diagram:\n'
                  '(edge weight | saved value on node)\n', self.state_dd_object.list_of_all_edges[0])

        return output_state_vec

    def update_decision_diagram(self, edge_measured_to_1, edge_measured_to_0):

        """ Schritt 13 """
        #   Normierung des neuen Entscheidungsdiagramms erfolgt durch division des Kantengewichts durch die
        #   Wurzel aus der bedingten Wahrschinlichkeit, mit der dieser Zustand an diesem Knoten eingetreten ist.
        edge_measured_to_1.edge_weight /= cmath.sqrt(edge_measured_to_1.conditional_probability)

        """ Schritt 12 """

        #   Durch die Messung hat die linke Kante die Wahrscheinlichkeit 1
        edge_measured_to_1.edge_probability = 1
        edge_measured_to_1.conditional_probability = 1

        #   Die nicht gemessene Kante wird auf den 0-Knoten gezogen, und ihre Eigenschaften entsprechend
        #   angepasst
        edge_measured_to_0.edge_probability = 0
        edge_measured_to_0.conditional_probability = 0
        edge_measured_to_0.edge_weight = 0

        #   Der Zielknoten der Kante die auf 0 zeigen soll, wird in der Liste aller Knoten gesucht, um ihn
        #   später zu löschen. Er selber kann nicht verwendet werden, da der Kante ein neuer Zielknoten
        #   zugewiesen wird, und sich dadurch auch der gemerkte Knoten ändert
        #   ( node_to_delete = edge_measured_to_1.target_node: geht nicht)
        #   Eine echte kopie von edge_measured_to_1.target_node bringt auch nichts, da dann alle objekte in diesem
        #   Knoten auch neu sind, und somit kann man damit nicht mehr das Teildiagramm lsöchen, welches man
        #   eigentlich löschen wollte (sondern nur die erstellte Kopie).
        #
        #   Der Knoten, der in der Liste aller Knoten gefunden wurde, kann mit delete_node() gelöscht werden, da
        #   er selber in der Liste vorkommt (delete_node() löscht ihn dann in der Liste)
        #   (Ein neues Objekt mit den richtigen Kantenobjekten müsste in der Liste aller Knoten diesen Knoten
        #   überschreiben, damit es funktioniert. Das wäre also aufwendiger.)
        index = []
        for i, level in enumerate(self.state_dd_object.list_of_all_nodes):

            #   Durchsuche eine Ebene, falls der Knoten dort nicht ist, gibt es einen ValueError, sodass
            #   einfach in der nächsten Ebene wetier gesucht werden kann.
            try:
                j = level.index(edge_measured_to_0.target_node)
            except ValueError:
                continue

            #   Index wird gespeichert, andem sich der Knoten befindet
            index += [i, j]

        #   Es wird geprüft, das für i und j jeweiln nur ein Element gefunden wurde. Der Knoten sollte genau
        #   einmal in der Liste vorkommen.
        if len(index) == 2:

            i, j = index

            #   Falls sich der Knoten in der letzten Ebene befindet, muss er nicht gelöscht werden, da er
            #   entweder der 0 oder 1 Endknoten ist.
            if i == Base.getnqubits() or np.size(self.state_dd_object.list_of_all_nodes[i][j].list_incoming_edges) > 1:
                node_to_delete = None
                self.state_dd_object.list_of_all_nodes[i][j].delete_edge_in_incoming_list(edge_measured_to_0)

            #   Speichere den gefundenen Knoten mit neuen Namen (aber gleicher Adresse im Speicher), damit er
            #   später leichter verwendet werden kann um delete_node() aufzurufen.
            else:
                node_to_delete = self.state_dd_object.list_of_all_nodes[i][j]
                node_to_delete.list_incoming_edges = np.array([])

        else:
            raise Exception('Error: Node should occur only once in list_of_all_nodes.'
                            ' Error in decision diagram.')

        #   Ziehe die nicht gemessene Kante vom bisherigen Zielknoten auf den 0-Endknoten
        edge_measured_to_0.target_node = self.state_dd_object.node_zero


        #   Füge diese Kante dem 0-Endknoten der Liste der eingehenden Kanten hinzu
        self.state_dd_object.node_zero.list_incoming_edges = \
            np.append(self.state_dd_object.node_zero.list_incoming_edges, edge_measured_to_0)

        #   Anzahl der Kanten, die durch diese Kante dargestellt wird, wird berechnet
        edge_measured_to_0.n_possible_paths_to_zero = pow(2, Base.getnqubits() - self.qubit_to_measure - 1)

        return [edge_measured_to_0, edge_measured_to_1]
