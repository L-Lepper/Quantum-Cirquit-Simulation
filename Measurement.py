#   Projektarbeit Literaturrecherche zu Simulationsalgorithmen für Quantencomputing
#   Author: Lukas Lepper, 24.11.2020
#   Betreuer: Martin Hardieck
#   Dateiname: Measurement.py
#   Version: 0.6

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

        #   Rekusrives aufrufen des Entscheidungsdiagramms von unten nach oben, um Fehler im Aufbau zu erkennen
        #   ToDo: Ausgabe sollte irgendwie besser gemacht werden, so ist es sehr unübersichtlich
        if Base.get_verbose() >= 4:
            #   Für jeden Knoten der letzten Ebene ( 0/1 ) müssen die eingehenden Kanten aufgerufen werden
            for node in self.state_dd_object.list_of_all_nodes[Base.getnqubits()]:
                print(node.call_upstream(''))

        #   Messung: Für jeden Knoten auf der Ebene, auf der gemessen wird
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
                  'equal to 0 in addition with the probability equal to 1 have to be 100%:', p_0 * 100 + p_1 * 100,
                  '\n')

        #   Erzeuge eine Zufallszahl zwischen 0 und 1 mit 6 Nachkommastellen
        random_value = random.randint(0, 1000000) / 1000000

        #   Für jeden Knoten auf der Ebene des zu messenden Qubits, wird das Entscheidungsdiagramm durch die
        #   Messung angepasst (Messung 0 oder 1)
        list_inidzes_of_nodes_to_delete = []
        for node in self.state_dd_object.list_of_all_nodes[self.qubit_to_measure]:

            #   Spezialfall:
            #   (Verwendung der bedingten Wahrscheinlichkeit der Kanten)
            #   Hat der eine Knoten für die linke Ausgehende Kante die Wahrscheinlichkeit 0 und für die rechte
            #   Ausgehende Kante die Wahrscheinlichkeit 1, kann ein anderer Knoten auf der Ebene trotzdem für seine
            #   Nachfolgeäste die Wahrscheinlichkeit 0.5 haben. Auch wenn man bei alleiniger Betrachtung des ersten
            #   Knotens zu 100% für dieses Qubtis eine 1 (rechter Ast) messen würde, da in diesem Teilbaum ja nur diese
            #   Möglichkeit der Äste existert, kann aber bei der Betrachtung des gesamten Diagramms auch das Qubits zu
            #   0 gemessen werden. In diesem Fall wird also beim zweiten Knoten der linke Nachfolgeast zu 100%
            #   durchlaufen, im ersten Knoten wird jetzt aber keine von den beiden Kanten durchlaufen! Also haben jetzt
            #   schon die eingehenden Kanten dieses Knotens die Wahrscheinlichkeit 0, und führen auf den Endknoten.

            is_special_case = False
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
                    is_special_case = True

            #   Falls der Spezialfall eingetreten ist wird der Knoten und darüberliegende Knoten gelöscht, wenn sie
            #   durch den Spezialfall wegfallen.
            if is_special_case:

                #   Suche betrachteten Knoten node, für den der Spezialfall festgestellt wurde, in der Liste aller
                #   Knoten. In der Funktion process_special_case() wird dann der Fall direkt auf dem Knoten in der Liste
                #   bearbeitet. Das passiert rekursiv für alle weiteren Knoten, die auf dem wegfallenden Ast liegen.
                for index_of_layer, layer in enumerate(self.state_dd_object.list_of_all_nodes):

                    #   Falls es den Knoten auf der aktuellen Ebene gibt, wird der Index gespeichert, sonst gibt es
                    #   einen ValueError und die nächste Ebene wird probiert.
                    try:
                        index_of_node = layer.index(node)

                        #   Führe die Funktion für den aktuellen Knoten aus
                        self.process_special_case(index_of_layer, index_of_node, list_inidzes_of_nodes_to_delete)

                    #   Gehe in die nächste Ebende, wenn ValueError in layer.index(node) (node wurde nicht gefunden)
                    except ValueError:
                        continue

            # Falls p_0 größer gleich wie die Zufallszahl ist, wurde das Qubit zu 0 gemessen.
            elif p_0 >= random_value:

                """ Schritt 12 - 13 """

                #   Speichere die zu 0 und die zu 1 gemessene Kante, nach else ist dies genau anders herum, so kann
                #   aber die selbe Funkton genutzt werden.
                edge_measured_to_0 = node.list_outgoing_edges[1]
                edge_measured_to_1 = node.list_outgoing_edges[0]

                #   Die Funktion update_decision_diagram() passt das Entscheidungsdiagramm an die Messung an (Schritt
                #   12-13) und gibt die beiden Kanten wieder als Liste zurück. Diese werden direkt getrennt gespeichert.
                edge_measured_to_0, edge_measured_to_1 = self.update_decision_diagram(edge_measured_to_0,
                                                                                      edge_measured_to_1,
                                                                                      list_inidzes_of_nodes_to_delete)

                #   Die neuen Kanten werden wieder den betreffenden Kanten zugewiesen.
                node.list_outgoing_edges[1] = edge_measured_to_0
                node.list_outgoing_edges[0] = edge_measured_to_1

            #   Sonst wurde das Qubit zu 1 gemessen
            else:

                """ Schritt 12 - 13 """

                #   Speichere die zu 0 und die zu 1 gemessene Kante
                edge_measured_to_0 = node.list_outgoing_edges[0]
                edge_measured_to_1 = node.list_outgoing_edges[1]

                #   Die Funktion update_decision_diagram() passt das Entscheidungsdiagramm an die Messung an (Schritt
                #   12-13) und gibt die beiden Kanten wieder als Liste zurück. Diese werden direkt getrennt gespeichert.
                edge_measured_to_0, edge_measured_to_1 = self.update_decision_diagram(edge_measured_to_0,
                                                                                      edge_measured_to_1,
                                                                                      list_inidzes_of_nodes_to_delete)

                #   Die neuen Kanten werden wieder den betreffenden Kanten zugewiesen.
                node.list_outgoing_edges[0] = edge_measured_to_0
                node.list_outgoing_edges[1] = edge_measured_to_1

        #   Lösche den abgeschnittenen Baum, falls node_to_delete Knoten gespeichert hat
        #   Indizes der Knoten in der Liste aller Knoten, um sicherzugehen, dass die gewünschten Knoten angesprochen
        #   werden können
        if any(list_inidzes_of_nodes_to_delete):

            list_nodes = []
            n = 0
            #   Ein Element besteht immer aus den beiden Indizes für die Ebene und den Knoten in der Ebene, diese werden
            #   direkt getrennt gespeichert
            for i, j in list_inidzes_of_nodes_to_delete:

                #   Jetzt wird der gemerkte Knoten in einer Liste gespeichert, ich war mit nicht sicher ob es auch
                #   funktioniert hätte, wenn die Knoten schon in einer Funktion in der Liste gespeichert wurden.
                list_nodes += [self.state_dd_object.list_of_all_nodes[i][j]]

            #   Die einzelnen Knoten in der eben erstellten Liste, werden in der mehrdimensionalen Liste aller Knoten
            #   gesucht. Da die Knoten gelöscht werden, ändern sich nämlich die weiter oben gespeicherten Indizes,
            #   sodass man mit ihnen nicht mehr arbeiten kann.
            for node_del in list_nodes:
                for i, layer_of_nodes in enumerate(self.state_dd_object.list_of_all_nodes):

                    #   Wird der Knoten in der aktuellen Ebene gefunden, wird er gelöscht
                    try:
                        j = layer_of_nodes.index(node_del)
                        self.state_dd_object.list_of_all_nodes[i][j].delete_node()
                        n += 1

                        #   Beende die Schleife, da der Knoten nur einmal vorkommt
                        break

                    #   Ansonsten wird in der nächsten Ebene weiter gesucht
                    except ValueError:
                        continue

                #   Falls der Knoten nicht gefunden wurde (oder falls er mehmals gefunden wurde und Schleife nicht durch
                #   break beendet wird)
                if n != 1:
                    if Base.get_verbose() >= 0:
                        print('Error, Node after measurement was not deleted.')
                n = 0

        #   Möglicherweise kann jetzt das Entscheidungsdiagramm noch mal zusammengefasst werden
        #   ToDo: Vielleicht lohnt sich der Aufwand nicht
        self.state_dd_object.merge_dd_step7()

        #   Für jede Kante wird die Anzahl berechnet, wie häufig sie in den Ästen vorkommt
        #   Dieser Wert muss jetzt aktualisiert werden, da das DD verändert wurde
        self.state_dd_object.list_of_all_edges[0].calc_count_of_paths()
        self.state_dd_object.set_is_calculated_false()

        if Base.get_verbose() >= 2:
            print('\n---------------\t Calculate probabilities after measurement \t---------------\n')

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

        #   Ausgabe bei --quiet
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

    def update_decision_diagram(self, edge_pull_to_zero, staying_edge, list_inidzes_of_nodes_to_delete):
        """
        Diese Funktion bearbeitet das Entscheidungsdiagramm nach einer Messung: Eine Kante, die nicht gemessen wurde,
        bekommt die Wahrscheinlichkeit 0 und wird auf den 0 Endknoten gezogen, die andere Kante bleibt bestehen, hat
        jetzt aber die Wahrscheinlichkeit 1. Die Funktion wird jeweils für die Messung 0 und 1 aufgerufen, es ändert
        sich aber welche Kante zu 0 und welche Kante zu 1 gemessen wurde.

        :param edge_pull_to_zero: Die Kante die auf den 0 Knoten gesetzt wird, die zu 0 gemessen wurde.
        :param staying_edge: Die Kante die bleibt und die Wahrscheinlichkeit 1 bekommt.
        :param list_inidzes_of_nodes_to_delete: In dieser Liste, die außerhalb der Funktion definiert wurde, werden die
            Indizes der Ebene und des Knotens der Knoten gespeichert, die anschließend gelöscht werden sollen. (Das
            Löschen erfolgt erst später, da in anderen Situationen sich die Anzahl der Knoten und damit der Index
            ändert.)
        :return:
        """

        """ Schritt 13 """
        #   Bestimme den Wert, mit dem das Entscheidungsdiagramm neu normiert wird
        value_for_normalization = cmath.sqrt(staying_edge.conditional_probability)

        #   Normierung des neuen Entscheidungsdiagramms erfolgt durch division des Kantengewichts durch die
        #   Wurzel aus der bedingten Wahrschinlichkeit, mit der dieser Zustand an diesem Knoten eingetreten ist.
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
            #   einfach in der nächsten Ebene weiter gesucht werden kann.
            try:
                j = level.index(edge_pull_to_zero.target_node)

                #   Index wird gespeichert, andem sich der Knoten befindet
                index += [i, j]

            except ValueError:
                continue

        #   Es wird geprüft, das für i und j jeweils nur ein Element gefunden wurde. Der Knoten sollte genau
        #   einmal in der Liste vorkommen.
        if len(index) == 2:

            i, j = index

            #   Falls sich der Knoten in der letzten Ebene befindet, muss er nicht gelöscht werden, da er
            #   entweder der 0 oder 1 Endknoten ist.
            #   Oder wenn mehrere eingehende Kanten sind, wird nur die Kante entfernt
            if i == Base.getnqubits() or np.size(self.state_dd_object.list_of_all_nodes[i][j].list_incoming_edges) > 1:
                self.state_dd_object.list_of_all_nodes[i][j].delete_edge_in_incoming_list(edge_pull_to_zero)

            #   Speichere den gefundenen Knoten
            else:
                self.state_dd_object.list_of_all_nodes[i][j].list_incoming_edges = np.array([])
                list_inidzes_of_nodes_to_delete += [[i, j]]

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

    def process_special_case(self, index_o, index_p, list_inidzes_of_nodes_to_delete):
        """
        Funktion um den Spezialfall zu bearbeiten, dass an einem Knoten die Kante gemessen wurde, die eigentlich die
        Wahrscheinlichkeit 0 hat. In diesem Fall fällt der Knoten und der darunterliegende Baum weg. Es wird geprüft,
        ob der Quellknoten ebenfalls nur eine ausgehende Kante ungleich 0 hat, die nähmlich auf den aktuellen Knoten
        zeigt. Dann tritt dort nähmlich ebenfalls dieser Spezialfall ein, und der Knoten fällt weg. Es Wird also für
        jeden Knoten rekursiv an den eingehenden Kanten geprüft, ob an dem Quellknoten wieder der Spezialfall ist, oder
        ob die Rekursion endet.

        :param index_o: Index der Ebene, des aktuellen Knotens in der Liste aller Knoten
        :param index_p: Index des Knotens in der Ebene
        :param list_inidzes_of_nodes_to_delete: Liste die außerhalb der Funktion definiert wurde, in der die Indizes
            des zu löschenden Knotens gespeichert werden. Der zu löschende Knoten befindet sich immer am Ende einer
            Rekursion, durch ihn wird der nachfolgende Baum ebenfalls gelöscht.
        :return:
        """

        #   Speichere den Knoten aus der Liste aller Knoten, der mit den Indizes übergeben wurde
        node = self.state_dd_object.list_of_all_nodes[index_o][index_p]

        #   Für jede eingehende Kante des Knotens, wird geprüft ob am Quellkknoten ebenfalls der Spezialfall eintritt
        is_special_case = False
        for index_incoming_edge, edge in enumerate(node.list_incoming_edges):

            # Suche den Index der Kante, in der Liste der ausgehenden Kanten des Quellknotens, die gelöscht wird.
            index_edge_to_del_node = np.where(edge.source_node.list_outgoing_edges == edge)[0][0]
            # Index der andere Kante, die nicht gelöscht wird
            index_edge_not_to_del_node = (index_edge_to_del_node - 1) * -1

            #   Es wird geprüft, ob der Spezialfall an diesem Knoten zum tragen kommt (das eine Kante mit
            #   Wahrscheinlichkeit 0 gemessen wird)
            for i, outgoing_edge in enumerate(edge.source_node.list_outgoing_edges):

                #   Für jede ausgehende Kante speichert is_special_case True, falls die bedingte Wahrscheinlichkeit
                #   der aktuellen Kante 0 ist und diese Kante die bleibende ist, die nicht auf 0 geändert werden
                #   soll (Da der nachfolgende Baum der anderen Kante durch den Spezialfall wegggefallen ist)
                #   ToDo: Genauigkeit
                if round(outgoing_edge.conditional_probability, 13) == 0 and i == index_edge_not_to_del_node:
                    is_special_case = True

            #   Falls der Spezialfall eingetretenist, wird dieser Quellknoten in der Liste aller Knoten gesucht und die
            #   Funktion erneut rekursiv aufgerufen.
            if is_special_case:

                #   In der Ebene, in welcher der Knoten gespeichert ist, kommt es nicht zu einem ValueError und der
                #   nachfolgende Code nach layer.index() wird ausgeführt. Dann zeigen die Indizes auf den Knoten in der
                #   Liste aller Knoten.
                for index_of_layer, layer in enumerate(self.state_dd_object.list_of_all_nodes):
                    try:
                        index_of_node = layer.index(edge.source_node)

                        #   Die Funktion wird neu rekusiv aufgerufen, mit dem Index des Knotens in der Liste und
                        #   der Liste, in der die gefundenen Knoten gespeichert werden (Indizes) um sie später zu
                        #   löschen
                        self.process_special_case(index_of_layer, index_of_node, list_inidzes_of_nodes_to_delete)
                        break

                    except ValueError:
                        continue

            #   Tritt am Quellknoten der Spezialfall nicht auf, endet die Rekursion (kein neuer Aufruf dieser Funktion)
            #   und die aktuelle Kante wird in der Liste der ausgehenden Kanten der Quellknotens gesucht. Diese wird
            #   auf 0 geändert, die andere bleibende Kante des Quellknotens wird mit ihrer bedingten Wahrscheinlichkeit
            #   neu normiert.
            else:

                # Suche den Quellknoten der eingehenden Kanten des übergebenen Knotens in der Liste aller Knoten
                for index_k, layer in enumerate(self.state_dd_object.list_of_all_nodes):

                    try:
                        index_l = layer.index(edge.source_node)

                        #   wurde der Knoten gefunden, wird folgender Code ausgeführt und die Indizes zeigen auf diesen
                        #   Knoten.
                        #   Normiere die Kante die nicht auf 0 geht, mit der Wurzel aus der bedingten Wahrscheinlichkeit
                        value_for_normalization = cmath.sqrt(self.state_dd_object.list_of_all_nodes[index_k][index_l].
                                                             list_outgoing_edges[index_edge_not_to_del_node].
                                                             conditional_probability)

                        self.state_dd_object.list_of_all_nodes[index_k][index_l].list_outgoing_edges[
                            index_edge_not_to_del_node].edge_weight /= value_for_normalization

                        #   Anzahl der Kanten, die durch diese Kante dargestellt wird, wird berechnet
                        #   index_k bezeichnet die aktuelle Ebene
                        self.state_dd_object.list_of_all_nodes[index_k][index_l].list_outgoing_edges[
                            index_edge_to_del_node].n_possible_paths_to_zero = pow(2, Base.getnqubits() - index_k - 1)

                        self.state_dd_object.list_of_all_nodes[index_k][index_l].list_outgoing_edges[
                            index_edge_to_del_node].edge_probability = 0

                        self.state_dd_object.list_of_all_nodes[index_k][index_l].list_outgoing_edges[
                            index_edge_to_del_node].conditional_probability = 0

                        self.state_dd_object.list_of_all_nodes[index_k][index_l].list_outgoing_edges[
                            index_edge_to_del_node].edge_weight = 0

                        #   Die Kante, die auf 0 geht, wird auf den 0 Knoten gezogen
                        self.state_dd_object.list_of_all_nodes[index_k][index_l].list_outgoing_edges[
                            index_edge_to_del_node].target_node = self.state_dd_object.node_zero

                        #       Nicht notwendig, da die Objekte in der Liste aller Kanten Referenzen auf die Kanten in
                        #       den Knoten der Liste aller Knoten sind oder so, und in diesem Fall auch die Liste der
                        #       Kanten die neue Kante von oben auf den 0 Knoten hat
                        """ 
                        #   Suche die zu änderte Kante, die auf 0 führen soll, in der Liste aller Kanten und aktualisiere sie
                        #   in der Liste aller Kanten.
                        # index_in_list = np.where(self.state_dd_object.list_of_all_edges == edge)[0]
                        new_incoming_list = []
                        for edg in self.state_dd_object.list_of_all_edges:
                            new_incoming_list += [edg]
                        index_in_list = [new_incoming_list.index(self.state_dd_object.list_of_all_nodes[
                            index_k][index_l].list_outgoing_edges[index_edge_not_to_del_node])]

                        #   Falls die Kante genau einmal vorkommt, kann der Index gespeichert werden (Sie soll nur einmal
                        #   vorkommen)
                        if np.size(index_in_list) == 1:
                            index_in_list = index_in_list[0]
                        else:
                            raise ValueError

                        #   Aktualisiere diese Kante in der Liste aller Kanten
                        self.state_dd_object.list_of_all_edges[index_in_list] = self.state_dd_object.list_of_all_nodes[
                            index_k][index_l].list_outgoing_edges[index_edge_not_to_del_node]
                        """

                        #   Suche den 0 Knoten in der Liste aller Knoten und aktualisiere die eingehende Kante
                        for index_m, layer_2 in enumerate(self.state_dd_object.list_of_all_nodes):

                            try:
                                index_n = layer_2.index(self.state_dd_object.node_zero)

                                #   Hänge dem 0 Knoten in der Liste aller Knoten die bearbeitete Kante des oben
                                #   betrachteten Quellknotens k,l hinzu (list_outgoing_edges[index_edge_to_del_node])
                                self.state_dd_object.list_of_all_nodes[index_m][index_n]. \
                                    list_incoming_edges = np.append(
                                    self.state_dd_object.list_of_all_nodes[index_m][index_n].list_incoming_edges, [
                                        self.state_dd_object.list_of_all_nodes[index_k][index_l].list_outgoing_edges[
                                            index_edge_to_del_node]])
                                break

                            except ValueError:
                                continue

                        #   Falls der zu löschende Knoten mehrere eingehende Kanten hat, wird nur die aktuelle Kante
                        #   entfernt
                        if np.size(self.state_dd_object.list_of_all_nodes[index_o][index_p].list_incoming_edges) != 1:

                            #   Suche den index der aktuellen Kante in der Liste der ausgehenden Kanten des zu
                            #   löschenden Knotens
                            index_in_incoming_list = np.where(
                                self.state_dd_object.list_of_all_nodes[index_o][index_p].list_incoming_edges == edge)

                            #   Lösche diese Kante in der Liste der eingehenden Kanten
                            self.state_dd_object.list_of_all_nodes[index_o][index_p].list_incoming_edges = \
                                np.delete(self.state_dd_object.list_of_all_nodes[index_o][index_p].list_incoming_edges,
                                          index_in_incoming_list)

                        #   Speichere den zu löschenden Knoten, der jetzt keine Kanten mehr hat die auf ihn zeigen.
                        #   Daher wird die noch die Liste der eingehenden Kanten geleert. (Hier ist die Rekursion für
                        #   einen Zweig zuende, es muss nur ein Knoten gelöscht werden)
                        else:
                            self.state_dd_object.list_of_all_nodes[index_o][index_p].list_incoming_edges = np.array([])
                            list_inidzes_of_nodes_to_delete += [[index_o, index_p]]

                        break

                    except ValueError:
                        continue
