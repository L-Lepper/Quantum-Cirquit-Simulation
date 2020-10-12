#   Projektarbeit Literaturrecherche zu Simulationsalgorithmen für Quantencomputing
#   Author: Lukas Lepper, 14.09.2020
#   Betreuer: Martin Hardieck
#   Dateiname: DDEdge.py
#   Version: 0.4


import numpy as np
import cmath
from Base import Base


class DDNode(Base):
    """
    Klasse für die Knoten-Objekte. Jeder Knoten hat eine Liste mit allen eingehenden und allen ausgehenden Kanten.
    In saved_value_on_node können auf dem Knoten Zwischenergebnisse gespeichert werden.
    """

    #   remember_node wird bei der Überprüfung der Teilmatrizen beim Zusammenfassen der Knoten benötigt
    remember_node = None

    def __init__(self, list_incoming_edges, list_outgoing_edges, dd_obj_in):
        """
        :param list_incoming_edges: numpy liste mit Objekten der eingehenden Kanten
        :param list_outgoing_edges: numpy liste mit Objekten der ausgehenden Kanten
        """

        self.saved_value_on_node = 0
        self.list_incoming_edges = list_incoming_edges
        self.list_outgoing_edges = list_outgoing_edges
        self.is_calculated = False
        self.dd_obj = dd_obj_in
        super().__init__()

    def delete_node(self):
        for edge in self.list_outgoing_edges:
            edge.delete_edge(self.dd_obj)

        #dd_obj.list_of_all_nodes.remove(self)

    def get_max_value_of_target_nodes(self):
        """
        Bestimmt den betragsmäßig größten Wert. Funktion wird rekursiv für Nachfolgeknoten aufgerufen.
        :return: Gibt betragsmäßig größten Wert, aus den Zielknoten der ausgehenden Kanten, zurück (die negative Zahl
        des betragsmäßig größten Wertes).
        """

        #   Falls Funktion schon durch einen anderen Ast aufgerufen wurde, muss Berechnung nicht nochmal durchgeführt
        #   werden.
        if self.is_calculated:
            return self.saved_value_on_node

        else:
            temp = []
            self.is_calculated = True

            #   Falls in list_outgoing_edges Kanten gespeichert sind, wird der Liste temp der betragsmäßig größte Wert
            #   der bereits in den Zielknoten gespeichert ist, für jede Kante hinzugefügt.
            if any(self.list_outgoing_edges):
                for edge in self.list_outgoing_edges:
                    temp += [edge.target_node.get_max_value_of_target_nodes()]

                abs_temp = []
                for value in temp:
                    abs_temp += [abs(value)]

                abs_max_index = abs_temp.index(max(abs_temp))

                #   Speichere den betragsmäßig größten Wert aus der Liste temp im aktuellen Knoten
                self.saved_value_on_node = temp[abs_max_index]

                #   Gebe den gespeicherten Wert zurück
                return self.saved_value_on_node

            #   Falls der aktuelle Knoten ein Endknoten ist, wird der in ihm gespeicherte Wert zurückgegeben
            #   (entspricht dem betragsmäßig größten Wert, da es keine Nachfolgewerte gibt)
            else:
                return self.saved_value_on_node

    def get_weighted_propability_of_node(self):
        """
        Zwischenergebnis zur Berechnung der Kantengewichte. Zuvor muss Schritt 5 in "instructions_for_decision_
        diagram.doocx" ausgeführt worden sein, damit in den Kanten und Knoten die benötigten Werte stehen. Funktion
        ruft rekursiv die Nachfolger auf.
        :return: Gibt die gewichtete Wahrscheinlichkeit des aktuellen Knoten zurück (p=p_left * w_left^2 +
        p_right * w_right^2)
        """

        #   Falls Funktion schon durch einen anderen Ast aufgerufen wurde, muss Berechnung nicht nochmal durchgeführt
        #   werden.
        if self.is_calculated:
            return self.saved_value_on_node

        else:
            temp = 0.0
            self.is_calculated = True

            #   Falls in list_outgoing_edges Kanten gespeichert sind, wird der Zahl temp für alle ausgehenden Kanten,
            #   das Produkt aus der gewichteten Wahrscheinlichkeit des Zielknotens und dem quadrierten Betrag des
            #   jeweiligen Kantengewichts, hinzuaddiert.
            if any(self.list_outgoing_edges):
                for edge in self.list_outgoing_edges:
                    temp += edge.target_node.get_weighted_propability_of_node() * pow(abs(edge.edge_weight), 2)

                #   Das Ergebnis wird gespeichert und zurückgegeben
                self.saved_value_on_node = temp
                return self.saved_value_on_node

            #   Sonst wird für die Endknoten nur der gespeicherte Wert (0 oder 1) zurückgegeben
            else:
                return self.saved_value_on_node

    def get_matrix(self, upstream_edge_weight):
        if any(self.list_outgoing_edges):
            if self.dd_obj.is_vector:
                upstream_ew_0 = upstream_edge_weight * self.list_outgoing_edges[0].edge_weight
                upstream_ew_1 = upstream_edge_weight * self.list_outgoing_edges[1].edge_weight

                v_0 = self.list_outgoing_edges[0].target_node.get_matrix(upstream_ew_0)
                v_1 = self.list_outgoing_edges[1].target_node.get_matrix(upstream_ew_1)

                vec_out = np.append(v_0, v_1)

                return vec_out

            elif not self.dd_obj.is_vector:
                list_of_submatrizes = []

                for i in range(4):
                    upstream_ew = upstream_edge_weight * self.list_outgoing_edges[i].edge_weight
                    submatrix = self.list_outgoing_edges[i].target_node.get_matrix(upstream_ew)

                    if np.array_equal(submatrix, [[0]]):
                        n = int(cmath.sqrt(self.list_outgoing_edges[i].n_possible_paths).real)
                        submatrix = np.zeros((n, n))

                    list_of_submatrizes += [submatrix]

                #upstream_ew_0 = upstream_edge_weight * self.list_outgoing_edges[0].edge_weight
                #upstream_ew_1 = upstream_edge_weight * self.list_outgoing_edges[1].edge_weight
                #upstream_ew_2 = upstream_edge_weight * self.list_outgoing_edges[2].edge_weight
                #upstream_ew_3 = upstream_edge_weight * self.list_outgoing_edges[3].edge_weight

                #m_00 = self.list_outgoing_edges[0].target_node.get_matrix(upstream_ew_0)
                #m_01 = self.list_outgoing_edges[1].target_node.get_matrix(upstream_ew_1)
                #m_10 = self.list_outgoing_edges[2].target_node.get_matrix(upstream_ew_2)
                #m_11 = self.list_outgoing_edges[3].target_node.get_matrix(upstream_ew_3)

                #if m_00 == [[0]]:
                #    n = self.list_outgoing_edges[0].n_possible_paths
                #    m_00 = np.zeros((n, n))

                m_0x = np.append(list_of_submatrizes[0], list_of_submatrizes[1], 0)
                m_1x = np.append(list_of_submatrizes[2], list_of_submatrizes[3], 0)

                matrix_out = np.append(m_0x, m_1x, 1)

                return matrix_out

            else:
                print('Fehler beim Umwandeln des Entscheidungsdiagramms in einen Vektor oder Matrix.'
                      '\nKnoten müssen entweder 2 oder 4 ausgehende Kanten haben.')

        else:
            return np.array([[self.saved_value_on_node * upstream_edge_weight]])

