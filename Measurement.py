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
        if Base.get_verbose() >= 2:
            print('Decision Diagram before measurement\n', self.state_dd_object)

        p_0 = 0
        p_1 = 0
        for node in self.state_dd_object.list_of_all_nodes[self.qubit_to_measure]:

            #   An der Stelle wird mal geprüft, das der Knoten wirklich nur zwei ausgehende Kanten hat. Das DDObject
            #   geht auch für Matrizen, aber die Messung soll nur für Vektroren funktionieren
            if np.size(node.list_outgoing_edges) != 2:
                raise Exception('Error: expected 2 outgoing edges for one Node. For meassurement the decision diagram '
                                'have to represent a vector. Then, each node need 2 outgoing edges. ')

            #   Für das zu messende Qubit wird die Wahrscheinlichkeit berechnet für den Zustand 0 oder 1 (Summe der
            #   jeweiligen Äste aller Knoten auf einer Ebene).
            #   Die Summe der normalen Kantenwahrscheinlcihkeit, kann auch im Spezialfall normal berechnet werden
            p_0 += node.list_outgoing_edges[0].edge_probability
            p_1 += node.list_outgoing_edges[1].edge_probability

        #   Test, dass die Wahrscheinlichkeit p_0 + p_1 gleich 1 ist.
        if Base.get_verbose() == 3:
            print('Testing measurement: the probability for qubit', self.qubit_to_measure,
                  'equal to 0\nin addition with the probability equal to 1 have to be 100%:', p_0 * 100 + p_1 * 100,
                  '\n')

        #   Erzeuge eine Zufallszahl zwischen 0 und 1 mit 6 Nachkommastellen
        random_value = random.randint(0, 1000000) / 1000000

        #   Für jeden Knoten auf der Ebene des zu messenden Qubits, wird das Entscheidungsdiagramm durch die
        #   Messung angepasst (Messung 0 oder 1)
        node_to_delete = []
        list_inidzes_of_nodes_for_normalization = []
        for node in self.state_dd_object.list_of_all_nodes[self.qubit_to_measure]:

            #   Spezialfall:
            #   (Verwendung der bedingten Wahrscheinlichkeit der Kanten)
            #   Hat der eine Knoten für die linke Ausgehende Kante die Wahrscheinlichkeit 0 und für die rechte
            #   Ausgehende Kante die Wahrscheinlichkeit 1, kann ein anderer Knoten auf der Ebene trotzdem für seine
            #   Nachfolgeäste die Wahrscheinlichkeit 0.5 haben. Auch wenn man bei alleiniger Betrachtung des ersten Knotens
            #   zu 100% für dieses Qubtis eine 1 (rechter Ast) messen würde, da in diesem Teilbaum ja nur diese Möglichkeit
            #   der Äste existert, kann aber bei der Betrachtung des gesamten Diagramms auch das Qubits zu 0 gemessen
            #   werden. In diesem Fall wird also beim zweiten Knoten der linke Nachfolgeast zu 100% durchlaufen, im ersten
            #   Knoten wird jetzt aber keine von den beiden Kanten durchlaufen! Also haben jetzt schon die eingehenden
            #   Kanten dieses Knotens die Wahrscheinlichkeit 0, und führen auf den Endknoten.

            d = False
            #   Es wird geprüft, ob der Spezialfall an diesem Knoten zum tragen kommt (das eine Kante mit
            #   Wahrscheinlichkeit 0 gemessen wird)
            for i, edge in enumerate(node.list_outgoing_edges):

                #   Für jede ausgehende Kante speichert is_special_case True, falls die bedingte Wahrscheinlichkeit
                #   der linken Kante 0 ist und 0 gemessen wurde(linke Kante) oder falls die bedingte Wahrscheinlichkeit
                #   der rechten Kante 0 ist und 1 gemessen wurde(rechte Kante). Also das eine Kante mit
                #   Wahrscheinlichkeit 0 gemessen wurde. In den anderen Fällen, kann normal weiter gemacht werden.
                #   ToDo: Genauigkeit
                if round(edge.conditional_probability, 13) == 0 and i == 0 and p_0 >= random_value \
                        or round(edge.conditional_probability, 13) == 0 and i == 1 and p_0 < random_value:

                    #   Index der jeweils anderen Kante. Diese hatte vorher die bedingte Wahrs. von 1 und hat ein
                    #   Kantengewicht, welches zur neuen Normierung benötigt wird, wenn diese Kante wegfällt
                    j = (i - 1) * -1

                    #   Speichere die Wurzel der bedingten Wahrsch. der anderen Kante des Knotens in der ersten
                    #   Schleife, zum normieren
                    #sum = 0
                    #for x in node.get_matrix(1):
                     #   sum += cmath.sqrt(abs(x))
                    #value_for_normalizing = sum
                    #value_for_normalizing = node.list_outgoing_edges[j].conditional_probability

                    d = True



                    """
                        #   Index dieser Kante, bei welcher der Spezialfall zum tragen kommt
                        i_of_edge_to_zero = np.where()

                        #   Index der jeweils anderen Kante. Diese hatte vorher die bedingte Wahrs. von 1 und hat ein
                        #   Kantengewicht, welches zur neuen Normierung benötigt wird, wenn diese Kante wegfällt
                        j = (i - 1) * -1

                        #   Speichere die Wurzel der bedingten Wahrsch. der anderen Kante des Knotens in der ersten
                        #   Schleife, zum normieren
                        value_for_normalizing = cmath.sqrt(node.list_outgoing_edges[j].conditional_probability)

                        qsim_obj.pull_edge_to_zero_and_check_source_node(parent_edge.source_node, i_of_edge_to_zero, value_for_normalizing)
                        """
            if d:

                for index_of_layer, layer in enumerate(self.state_dd_object.list_of_all_nodes):
                    try:
                        index_of_node = layer.index(node)
                        nodes_del, list_indizes = self.process_special_case(self.state_dd_object.list_of_all_nodes[index_of_layer][index_of_node], p_0, random_value)
                        node_to_delete += nodes_del
                        list_inidzes_of_nodes_for_normalization += list_indizes
                    except ValueError:
                        continue

            # Falls p_0 größer gleich wie die Zufallszahl ist, wurde das Qubit zu 0 gemessen.
            elif p_0 >= random_value:

                """ Schritt 12 - 13 """

                #   Speichere die zu 0 und die zu 1 gemessene Kante, nach else ist dies genau anders herum, so kann
                #   aber die selbe Funkton genutzt werden.
                edge_measured_to_0 = node.list_outgoing_edges[1]
                edge_measured_to_1 = node.list_outgoing_edges[0]

                value_for_normalization = cmath.sqrt(edge_measured_to_1.conditional_probability)

                #   Die Funktion update_decision_diagram() passt das Entscheidungsdiagramm an die Messung an (Schritt
                #   12-13) und gibt die beiden Kanten wieder als Liste zurück. Diese werden direkt getrennt gespeichert.
                edge_measured_to_0, edge_measured_to_1 = self.update_decision_diagram(edge_measured_to_0,
                                                                                      edge_measured_to_1,
                                                                                      value_for_normalization,
                                                                                      node_to_delete)

                #   Die neuen Kanten werden wieder den betreffenden Kanten zugewiesen.
                node.list_outgoing_edges[1] = edge_measured_to_0
                node.list_outgoing_edges[0] = edge_measured_to_1

            #   Sonst wurde das Qubit zu 1 gemessen
            else:

                """ Schritt 12 - 13 """

                #   Speichere die zu 0 und die zu 1 gemessene Kante
                edge_measured_to_0 = node.list_outgoing_edges[0]
                edge_measured_to_1 = node.list_outgoing_edges[1]

                value_for_normalization = cmath.sqrt(edge_measured_to_1.conditional_probability)

                #   Die Funktion update_decision_diagram() passt das Entscheidungsdiagramm an die Messung an (Schritt
                #   12-13) und gibt die beiden Kanten wieder als Liste zurück. Diese werden direkt getrennt gespeichert.
                edge_measured_to_0, edge_measured_to_1 = self.update_decision_diagram(edge_measured_to_0,
                                                                                      edge_measured_to_1,
                                                                                      value_for_normalization,
                                                                                      node_to_delete)

                #   Die neuen Kanten werden wieder den betreffenden Kanten zugewiesen.
                node.list_outgoing_edges[0] = edge_measured_to_0
                node.list_outgoing_edges[1] = edge_measured_to_1


        if list_inidzes_of_nodes_for_normalization:
            value_for_normalisation = 0
            k, l, i, j = [0, 0, 0, 0]
            for list_i in list_inidzes_of_nodes_for_normalization:
                k, l, i, j = list_i
                upstream_value = self.state_dd_object.list_of_all_edges[0].edge_weight
                asd = self.state_dd_object.list_of_all_nodes[0][0].get_matrix(upstream_value)
                for x in asd:
                    value_for_normalisation += pow(abs(x), 2)

                value_for_normalisation = cmath.sqrt(value_for_normalisation)
                self.state_dd_object.list_of_all_nodes[k][l].list_outgoing_edges[i].edge_weight /= value_for_normalisation
                break


        # Lösche den abgeschnittenen Baum, falls node_to_delete einen Knoten gespeichert hat
        if node_to_delete:
            for node in node_to_delete:
                node.delete_node()

        #   Möglicherweise kann jetzt das Entscheidungsdiagramm noch mal zusammengefasst werden
        #   ToDo: Vielleicht lohnt sich der aufwand nicht
        #   ToDo: Fehler in der Zusammenfassung (Kanten und Wert im Knoten ist gleich, aber nicht der gesamte nachfogende Ast)
        #qsim_obj.state_dd_object.merge_dd_step7()

        #   Für jede Kante wird die Anzahl berechnet, wie häufig sie in den Ästen vorkommt
        #   Dieser Wert muss jetzt aktualisiert werden, da das DD verändert wurde
        self.state_dd_object.list_of_all_edges[0].calc_count_of_paths()
        self.state_dd_object.set_is_calculated_false()

        #   Berechne alle Kanten-Wahrscheinlichkeiten neu
        self.state_dd_object.calc_probabilities_if_vector()

        if Base.get_verbose() >= 2:
            print('\nDecision Diagram after measurement\n', self.state_dd_object)

        """ Schritt 14 """
        #   Aus dem neuen Entscheidungsdiagramm wird ein Vektor ausgelesen
        output_state_vec = self.state_dd_object.create_matrix()

        #   Ausgabe mit welchem Zustand das Qubit gemessen wurde
        if Base.get_verbose() >= 0:
            if p_0 >= random_value:

                print('Qubit', self.qubit_to_measure, 'was measured to 0.')

            else:

                print('Qubit', self.qubit_to_measure, 'was measured to 1.')
        else:
            if p_0 >= random_value:

                print(str([self.qubit_to_measure, 0]))

            else:

                print(str([self.qubit_to_measure, 1]))

        #   Ausgabe der Summe aus den gadrierten Beträgen der Elemente aus dem Zustandsvektor
        #   Damit wird die Normiertheit gepfüft, diese Summe muss 1 ergeben
        if Base.get_verbose() == 3:

            sum_entries = 0
            for x in output_state_vec:
                sum_entries += pow(abs(x), 2)

            print('\n\nCheck normalization:')

            print('Sum of the squared magnitudes of the state vector:', sum_entries, '\n')

            #   Ausgabe des Entscheidungsdiagramms rekursiv über die Wurzelkante
            print('Recursive call of edges and nodes of the decision diagram:\n'
                  '(edge weight | saved value on node)\n', self.state_dd_object.list_of_all_edges[0])

        return output_state_vec

    def update_decision_diagram(self, edge_pull_to_zero, staying_edge, value_for_normalization, node_to_delete):

        """ Schritt 13 """
        #   Normierung des neuen Entscheidungsdiagramms erfolgt durch division des Kantengewichts durch die
        #   Wurzel aus der bedingten Wahrschinlichkeit, mit der dieser Zustand an diesem Knoten eingetreten ist.

        if value_for_normalization:
            staying_edge.edge_weight /= value_for_normalization

        """ Schritt 12 """

        #   Durch die Messung hat die linke Kante die bedingte Wahrscheinlichkeit 1, die Kantenwahrscheinlichkeit wird
        #   später neu berechnet
        staying_edge.edge_probability = 1
        staying_edge.conditional_probability = 1

        #   Die nicht gemessene Kante wird auf den 0-Knoten gezogen, und ihre Eigenschaften entsprechend
        #   angepasst
        edge_pull_to_zero.edge_probability = 0
        edge_pull_to_zero.conditional_probability = 0
        edge_pull_to_zero.edge_weight = 0

        #   Der Zielknoten der Kante die auf 0 zeigen soll, wird in der Liste aller Knoten gesucht, um ihn
        #   später zu löschen. Er selber kann nicht verwendet werden, da der Kante ein neuer Zielknoten
        #   zugewiesen wird, und sich dadurch auch der gemerkte Knoten ändert
        #   ( node_to_delete = staying_edge.target_node: geht nicht)
        #   Eine echte kopie von staying_edge.target_node bringt auch nichts, da dann alle objekte in diesem
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
                j = level.index(edge_pull_to_zero.target_node)
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
                self.state_dd_object.list_of_all_nodes[i][j].delete_edge_in_incoming_list(edge_pull_to_zero)

            #   Speichere den gefundenen Knoten mit neuen Namen (aber gleicher Adresse im Speicher), damit er
            #   später leichter verwendet werden kann um delete_node() aufzurufen.
            else:
                self.state_dd_object.list_of_all_nodes[i][j].list_incoming_edges = np.array([])
                node_to_delete += [self.state_dd_object.list_of_all_nodes[i][j]]

        else:
            raise Exception('Error: Node should occur only once in list_of_all_nodes.'
                            ' Error in decision diagram.')

        #   Ziehe die nicht gemessene Kante vom bisherigen Zielknoten auf den 0-Endknoten
        edge_pull_to_zero.target_node = self.state_dd_object.node_zero

        #   Füge diese Kante dem 0-Endknoten der Liste der eingehenden Kanten hinzu
        self.state_dd_object.node_zero.list_incoming_edges = \
            np.append(self.state_dd_object.node_zero.list_incoming_edges, edge_pull_to_zero)

        #   Anzahl der Kanten, die durch diese Kante dargestellt wird, wird berechnet
        edge_pull_to_zero.n_possible_paths_to_zero = pow(2, Base.getnqubits() - self.qubit_to_measure - 1)

        return [edge_pull_to_zero, staying_edge]

#    def pull_edge_to_zero_and_check_source_node(qsim_obj, node, i_of_edge_to_zero, value_for_normalizing):
    """
        Diese Funktion funktioniert noch nicht so, wie sie soll. Das Entscheidungsdigramm ist unnötig groß, aber das
        Ergebniss ist eigentlich richtig

        ToDo: Fehler suchen
        :param node:
        :param i_of_edge_to_zero:
        :param value_for_normalizing:
        :return:
        """
    """
        node_to_delete = []

        #   Index der anderen ausgehenden Kante von node, die nicht auf 0 gezogen wird (Es gibt zwei ausgehende Kanten)
        j_other_edge = (i_of_edge_to_zero - 1) * -1

        #   Prüfe ob beide ausgehenden Kanten des Knotens auf 0 gehen, wenn i_of_edge_to_zero auf 0 gezogen wird
        #   Hat die andere Kante die Kantenwahrscheinlichkeit 0, geht sie auf den 0-Endknoten
        if node.list_outgoing_edges[j_other_edge].edge_probability == 0:

            #   Dem übergebenen Wert zur Normierung wird die Wurzel der bedingten Wahrsch. der Kante hinzugefügt,
            #   die auf 0 gezogen werden soll, um dann das Diagramm richtig zu normieren
            value_for_normalizing *= cmath.sqrt(node.list_outgoing_edges[i_of_edge_to_zero].conditional_probability)

            #   Es wird rekursiv wieder die eingehende Kante dieses Knotens auf 0 gezogen
            for parent_edge in node.list_incoming_edges:

                if parent_edge.source_node:
                    #   Index dieser Kante in der Liste der ausgehenden Kanten vom Quellknoten dieser Kante
                    #   (parent_edge), die auf 0 gezogen werden soll, weil ihr Zielknoten durch den Spezialfall
                    #   wegfällt.
                    i_of_edge_to_zero = np.where(parent_edge.source_node.list_outgoing_edges == parent_edge)[0][0]

                    #   Rufe die Funktion rekursiv für die nächste Kante auf. Alle Knoten und Kanten auf dem Pfad
                    #   dorthin, werden am Ende der Rekursion gelöscht
                    qsim_obj.pull_edge_to_zero_and_check_source_node(parent_edge.source_node, i_of_edge_to_zero, value_for_normalizing)

                else:
                    #   Fehler, wenn Kante keinen Quellknoten hat. Im Wurzelknoten kann der Spezialfall nicht auftreten,
                    #   da er der einzige Knoten der Ebene ist und somit kann die Kante mit Wahrscheinlichkeit 0 auch
                    #   nicht gemessen werden. documentation "Spezialfall bei Messung.pdf"
                    if Base.get_verbose() > 0:
                        print('\nIn measurement.py by treating a special case: In '
                              'pull_edge_to_zero_and_check_source_node() a outgoing edge of the root-node was deleted.\n'
                              'Because of the special case (p_left=0, p_right=1, measurement to 0) all '
                              'edges goes to zero. This is not possible.\nError by handling this special case.')

                    #   Zielknoten ist jetzt der 0-Endknoten, wenn node keine ausgehenden Kanten auf einen anderen
                    #   Knoten hat
                    parent_edge.target_node = qsim_obj.state_dd_object.node_zero

                    #   Gibt es keinen Elternknoten, hat der Knoten auch nur eine eingehende Kante, die gelöscht werden
                    #   kann
                    node.list_incoming_edges = []

                    #   Dann kann der Knoten gelöscht werden
                    node_to_delete += [node]

        #   Geht die andere Kante nicht auf 0, kann der Knoten node bleiben, und nur die betreffende ausgehende Kante
        #   wird auf den 0-Knoten gezogen. Anschließend Endet die Rekursion und der Pfad nach unten wird durch
        #   delete_node() gelöscht
        else:
            staying_edge = node.list_outgoing_edges[j_other_edge]
            edge_pull_to_zero = node.list_outgoing_edges[i_of_edge_to_zero]
            node.list_outgoing_edges[j_other_edge], temp = qsim_obj.update_decision_diagram(staying_edge, edge_pull_to_zero, value_for_normalizing, node_to_delete)

        # Lösche den abgeschnittenen Baum, falls node_to_delete einen Knoten gespeichert hat
        if node_to_delete:
            for node in node_to_delete:
                node.delete_node()
    """

    def process_special_case(self, node, p_0, random_value):
        node_to_delete = []
        d = False
        list_inidzes_of_nodes_for_normalization = []

        for edge in node.list_incoming_edges:
            #   Es wird geprüft, ob der Spezialfall an diesem Knoten zum tragen kommt (das eine Kante mit
            #   Wahrscheinlichkeit 0 gemessen wird)
            for i, outgoing_edge in enumerate(edge.source_node.list_outgoing_edges):

                #   Für jede ausgehende Kante speichert is_special_case True, falls die bedingte Wahrscheinlichkeit
                #   der linken Kante 0 ist und 0 gemessen wurde(linke Kante) oder falls die bedingte Wahrscheinlichkeit
                #   der rechten Kante 0 ist und 1 gemessen wurde(rechte Kante). Also das eine Kante mit
                #   Wahrscheinlichkeit 0 gemessen wurde. In den anderen Fällen, kann normal weiter gemacht werden.
                #   ToDo: Genauigkeit
                if round(outgoing_edge.conditional_probability, 13) == 0 and i == 0 and p_0 >= random_value \
                        or round(outgoing_edge.conditional_probability, 13) == 0 and i == 1 and p_0 < random_value:
                    d = True

                    #   Index der jeweils anderen Kante. Diese hatte vorher die bedingte Wahrs. von 1 und hat ein
                    #   Kantengewicht, welches zur neuen Normierung benötigt wird, wenn diese Kante wegfällt
                    j = (i - 1) * -1

                    #   Speichere die Wurzel der bedingten Wahrsch. der anderen Kante des Knotens in der ersten
                    #   Schleife, zum normieren
                    #new_value = value_for_normalizing * cmath.sqrt(abs(edge.source_node.list_outgoing_edges[j].edge_weight))

            if d:

                for index_of_layer, layer in enumerate(self.state_dd_object.list_of_all_nodes):
                    try:
                        index_of_node = layer.index(edge.source_node)
                        nodes_del, list_indizes = self.process_special_case(
                            self.state_dd_object.list_of_all_nodes[index_of_layer][index_of_node], p_0,
                            random_value)
                        node_to_delete += nodes_del

                        #if list_indizes:
                        list_inidzes_of_nodes_for_normalization = list_indizes

                    except ValueError:
                        continue

            else:
                index_edge_to_del_node = np.where(edge.source_node.list_outgoing_edges == edge)[0][0]
                index_edge_not_to_del_node = (index_edge_to_del_node - 1) * -1

                for index_k, layer in enumerate(self.state_dd_object.list_of_all_nodes):

                    try:
                        index_l = layer.index(edge.source_node)

                        #qsim_obj.state_dd_object.list_of_all_nodes[index_k][index_l].list_outgoing_edges[
                         #   index_edge_not_to_del_node].edge_weight *= \
                          #  cmath.sqrt(abs(qsim_obj.state_dd_object.list_of_all_nodes[index_k][index_l].list_outgoing_edges[
                           #                    index_edge_to_del_node].conditional_probability))
                        #upstream_value = qsim_obj.state_dd_object.list_of_all_nodes[index_k][index_l].list_outgoing_edges[index_edge_not_to_del_node].edge_weight
                        #value = qsim_obj.state_dd_object.list_of_all_nodes[index_k][index_l].list_outgoing_edges[index_edge_not_to_del_node].target_node.get_matrix(upstream_value)
                        #new_value = 0
                        #for x in value:
                         #   new_value += pow(x, 2)
                        list_inidzes_of_nodes_for_normalization += [[index_k, index_l, index_edge_not_to_del_node, index_edge_to_del_node]]


                        #value_for_normalizing = cmath.sqrt(abs(qsim_obj.state_dd_object.list_of_all_nodes[index_k][index_l].list_outgoing_edges[index_edge_not_to_del_node].edge_weight))
                        #value_for_normalizing = cmath.sqrt(new_value)
                        #qsim_obj.state_dd_object.list_of_all_nodes[index_k][index_l].list_outgoing_edges[index_edge_not_to_del_node].edge_weight /= value_for_normalizing

                        #   Anzahl der Kanten, die durch diese Kante dargestellt wird, wird berechnet
                        self.state_dd_object.list_of_all_nodes[index_k][index_l].list_outgoing_edges[
                            index_edge_to_del_node].n_possible_paths_to_zero = pow(2,
                                                                                   Base.getnqubits() - index_k - 1) # index_k bezeichnet die aktuelle Ebene
                        self.state_dd_object.list_of_all_nodes[index_k][index_l].list_outgoing_edges[
                            index_edge_to_del_node].edge_probability = 0
                        self.state_dd_object.list_of_all_nodes[index_k][index_l].list_outgoing_edges[
                            index_edge_to_del_node].conditional_probability = 0
                        self.state_dd_object.list_of_all_nodes[index_k][index_l].list_outgoing_edges[
                            index_edge_to_del_node].edge_weight = 0

                        self.state_dd_object.list_of_all_nodes[index_k][index_l].list_outgoing_edges[
                            index_edge_to_del_node].target_node = self.state_dd_object.node_zero
                    except ValueError:
                        continue

                    for index_m, layer in enumerate(self.state_dd_object.list_of_all_nodes):

                        try:
                            index_n = layer.index(self.state_dd_object.node_zero)
                            self.state_dd_object.list_of_all_nodes[index_m][index_n].list_incoming_edges = \
                                np.append(
                                    self.state_dd_object.list_of_all_nodes[index_m][index_n].list_incoming_edges,
                                    [self.state_dd_object.list_of_all_nodes[index_k][index_l].list_outgoing_edges[
                                         index_edge_to_del_node]])
                        except ValueError:
                            continue

                node_to_delete += [node]

        return [node_to_delete, list_inidzes_of_nodes_for_normalization]
