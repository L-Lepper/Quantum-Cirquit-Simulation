#   Projektarbeit Literaturrecherche zu Simulationsalgorithmen für Quantencomputing
#   Author: Lukas Lepper, 14.09.2020
#   Betreuer: Martin Hardieck
#   Dateiname: DDEdge.py
#   Version: 0.4


from Base import Base
import numpy as np


class DDEdge(Base):
    """
    Klasse für die Kantenobjekte. Jede Kante kennt ihren Ziel- und Quellknoten und hat ein Kantengewicht und eine
    Wahrscheinlichkeit. In count_calc ist die Anzahl gespeichert, wie oft die Kante in allen möglichen Ästen des
    Entscheidungsdiagramms vorkommt (bei mehreren eingehenden Kanten, wenn Knoten zusammengefasst wurden). Sie enthält
    die Memberfunktionen, die zb. das Kantengewicht für alle Kanten rekursiv berechnen.
    """

    def __init__(self, source_node, target_node, dd_obj_in):
        self.dd_obj = dd_obj_in
        self.edge_weight = 1
        self.edge_probability = 0
        self.old_edge_probability = 0
        self.conditional_probability = 0
        self.source_node = source_node
        self.target_node = target_node
        #   Speichert die Anzahl, wie oft die Kante in verschiedenen Ästen vorkommt. Wird bisher nur für die Kanten zum
        #   0-Endknoten benötigt
        self.n_possible_paths_to_zero = 0
        self.count_of_paths = 0
        #   is_calculated wird benötigt, damit durch die rekursiven Funktionsaufrufe jedes Objekt nur einmal berechnet
        #   wird
        self.is_calculated = False
        super().__init__()

    def __str__(self):
        """
        Ausgabe des Entscheidungsdiagramms, wenn die Wurzelkante aufgerufen wird.
        :return:
        """

        print(self.target_node.saved_value_on_node, '\t', self.edge_weight, '\t', self.edge_probability, '\n')

        #   Ausgabestring, der für return benötigt wird
        str_out = ''

        if any(self.target_node.list_outgoing_edges):
            for element in self.target_node.list_outgoing_edges:
                str_out += (element.__str__())
            return str_out
        else:
            return str_out

    def delete_edge(self, dd_obj):
        edge_in = self
        if np.size(self.target_node.list_incoming_edges) == 1:
            self.target_node.delete_node(dd_obj)
        else:
            index = np.where(self.target_node.list_incoming_edges == edge_in)[0][0]
            if np.size(index) == 1:
                self.target_node.list_incoming_edges = np.delete(self.target_node.list_incoming_edges, index)
            else:
                print('Fehler in DDedge.py in def __del__(self, dd_obj). target_node.list_incoming_edges sollte die'
                      'Kante die gelöscht werden soll, genau einmal gespeichert haben.')

        index = np.where(dd_obj.list_of_all_edges == edge_in)[0][0]
        if np.size(index) == 1:
            dd_obj.list_of_all_edges = np.delete(dd_obj.list_of_all_edges, index)
        else:
            print('Fehler in DDedge.py in def __del__(self, dd_obj). dd_obj.list_of_all_edges sollte die Kante die'
                  'gelöscht werden soll, genau einmal gespeichert haben.')

    def calc_edge_weight(self):
        """
        Funktion berechnet das Kantengewicht der einzelnen Kanten. Zuvor muss Schritt 3 in "instructions_for_decision_
        diagram.doocx" ausgeführt worden sein, damit in den Knoten in saved_value_on_node die benötigten Werte stehen.
        ToDo: Dateiname überprüfen
        :return:
        """

        #   Falls Funktion schon durch einen anderen Ast aufgerufen wurde, muss Berechnung nicht nochmal durchgeführt
        #   werden.
        if self.is_calculated:
            return
        else:
            #   Falls ein Quellknoten existiert, wird Division von saved_value_on_node in Ziel- durch Quellknoten
            #   durchgeführt.
            if self.source_node:
                #   Falls Nenner 0 ist, soll Berechnung 0 sein
                if self.source_node.saved_value_on_node == 0:
                    self.edge_weight = 0
                else:
                    self.edge_weight = self.target_node.saved_value_on_node / self.source_node.saved_value_on_node
            #   Sonst wird für die Wurzelkante als Kantengewicht der im Zielknoten gespeicherte Wert verwendet.
            else:
                self.edge_weight = self.target_node.saved_value_on_node
            self.is_calculated = True

            #   Für jede ausgehende Kante des Zielknotens wird wieder das Kantengewicht berechnet
            for edge in self.target_node.list_outgoing_edges:
                edge.calc_edge_weight()

    def calc_product_of_weights(self, upstream_value):
        """
        Die Funktion berechnet als Zwischenergebniss das Produkt aller Kantengewichte, von der betrachteten Kante, hoch
        zur Wurzelkante. Zuvor muss Schritt 6 in "instructions_for_decision_diagram.doocx" ausgeführt worden sein,
        damit in den Knoten in saved_value_on_node die benötigten Werte stehen.
        ToDo: Dateiname überprüfen
        :param upstream_value: Bei Funktionsaufruf der Wurzelkante muss diesem Parameter 1 übergeben werden. Jede Kante
        ruft diese Funktion rekursiv für Nachfolgekanten auf, diese Verwenden den berechneten Wert aus der Elternkante.
        :return:
        """

        #   Falls Funktion schon durch einen anderen Ast aufgerufen wurde, muss Berechnung nicht nochmal durchgeführt
        #   werden
        if self.is_calculated:
            self.edge_probability += pow(abs(self.edge_weight), 2) * upstream_value

            #   Für jede ausgehende Kante des Zielknotens wird wieder dieses Produkt berechnet
            for edge in self.target_node.list_outgoing_edges:
                edge.calc_product_of_weights(self.old_edge_probability)

        else:
            #   In edge_probability wird das Produkt aus dem übergebenen Wert der vorherigen Kante und dem quadrierten
            #   Betrag des Kantengewichts der aktuellen Kante, gespeichert.
            self.edge_probability = pow(abs(self.edge_weight), 2) * upstream_value
            self.old_edge_probability = self.edge_probability
            self.is_calculated = True

            #   Für jede ausgehende Kante des Zielknotens wird wieder dieses Produkt berechnet
            for edge in self.target_node.list_outgoing_edges:
                edge.calc_product_of_weights(self.edge_probability)

    def calc_edge_propability(self):
        """
        Die Funktion berechnet die Wahrscheinlichkeit der Kanten. Zuvor muss Schritt 7 in "instructions_for_decision_
        diagram.doocx" ausgeführt worden sein, damit in den Kanten und Knoten die benötigten Werte stehen.
        ToDo: Dateiname überprüfen
        :return:
        """

        #   Falls Funktion schon durch einen anderen Ast aufgerufen wurde, muss Berechnung nicht nochmal durchgeführt
        #   werden
        if self.is_calculated:
            return
        else:
            #   Für die Wahrscheinlichkeit wird anschließend das Produkt aus dem Wert des Zielknotens mit dem
            #   Zwischenergebniss in der Kante berechnet.
            self.edge_probability *= self.target_node.saved_value_on_node
            self.is_calculated = True

            #   Die Funktion wird für alle ausgehenden Kanten rekursiv aufgerufen
            for edge in self.target_node.list_outgoing_edges:
                edge.calc_edge_propability()

    def calc_conditional_probabilities(self):
        if self.is_calculated:
            return
        else:
            if self.source_node:
                sum_incoming_ep = 0
                for edge in self.source_node.list_incoming_edges:
                    sum_incoming_ep += edge.edge_probability
                self.conditional_probability = self.edge_probability / sum_incoming_ep
            else:
                self.conditional_probability = self.edge_probability / 1

            if any(self.target_node.list_outgoing_edges):
                for edge in self.target_node.list_outgoing_edges:
                    edge.calc_conditional_probabilities()

            self.is_calculated = True

    def calc_count_of_paths(self):
        if not self.is_calculated:
            self.count_of_paths = self.n_possible_paths_to_zero
            self.is_calculated = True

        self.count_of_paths += 1

        for edge in self.target_node.list_outgoing_edges:
            edge.calc_count_of_paths()

    """
    def get_matrix(self, upstream_edge_weight):
        if any(self.target_node.list_outgoing_edges):
            if self.dd_obj.is_vector:
                for edge in self.target_node.list_outgoing_edges:
                    

                

                return vec_out

            elif not self.dd_obj.is_vector:
                list_of_submatrizes = []

                for i in range(4):
                    upstream_ew = upstream_edge_weight * self.list_outgoing_edges[i].edge_weight
                    submatrix = self.list_outgoing_edges[i].target_node.get_matrix(upstream_ew)

                    if np.array_equal(submatrix, [[0]]):
                        n = int(cmath.sqrt(self.list_outgoing_edges[i].n_possible_paths_to_zero).real)
                        submatrix = np.zeros((n, n))

                    list_of_submatrizes += [submatrix]

                m_0x = np.append(list_of_submatrizes[0], list_of_submatrizes[1], 0)
                m_1x = np.append(list_of_submatrizes[2], list_of_submatrizes[3], 0)

                matrix_out = np.append(m_0x, m_1x, 1)

                return matrix_out

            else:
                print('Fehler beim Umwandeln des Entscheidungsdiagramms in einen Vektor oder Matrix.'
                      '\nKnoten müssen entweder 2 oder 4 ausgehende Kanten haben.')

        else:
            if self.dd_obj.is_vector:
                return np.array([self.target_node.saved_value_on_node * upstream_edge_weight])
            else:
                return np.array([[self.target_node.saved_value_on_node * upstream_edge_weight]])
    """
