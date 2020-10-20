#   Projektarbeit Literaturrecherche zu Simulationsalgorithmen für Quantencomputing
#   Author: Lukas Lepper, 19.10.2020
#   Betreuer: Martin Hardieck
#   Dateiname: DDNode.py
#   Version: 0.5


import numpy as np
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
        """
        Funktion bestimmt rekursiv aus den Nachfolgeknoten die Matrix oder den Vektor, der durch das
        Entscheidungsdiagramm dargestellt wird.
        :param upstream_edge_weight: Das Produkt aus dem quadrierten Betrag aller Kantengewichte, auf dem über dem
        betrachteten Knoten liegendem Ast.
        :return: Matrix aus dem nachfolgenden Teildiagramm
        """

        #   Falls der Knoten ausgehende Kanten hat, wird die Funktion für die Nachfolgeknoten mit dem neuen Upstream-
        #   Kantengewicht aufgerufen
        if any(self.list_outgoing_edges):

            #   Für Vektoren
            if self.dd_obj.is_vector:

                #   Liste merkt sich die Teilvektoren, die aus den Nachfolgeknoten zurückgegeben werden
                list_of_subvectors = np.array([])

                #   Für jeden Ast wird das neue Upstream-Kantengewicht berechnet und die Funktion rekursiv aufgerufen
                #   und die Teilmatrix in der Liste gespeichert
                for i in range(2):
                    upstream_ew = upstream_edge_weight * self.list_outgoing_edges[i].edge_weight
                    subvector = self.list_outgoing_edges[i].target_node.get_matrix(upstream_ew)

                    #   Falls die Teilmatrix nur das Element 0 enthält, wird aus dem in der entsprechenden Kante
                    #   gespeicherten Wert (Anzahl der verschiedenen Pfade auf den 0-Knoten, die durch diese Kante
                    #   repräsentiert werden), die Matrix/der Vektor auf die entsprechende Größe erweitert. Selbe Größe,
                    #   wie die anderen Teilmatrizen.
                    if np.array_equal(subvector, [0]):
                        n = self.list_outgoing_edges[i].n_possible_paths_to_zero
                        subvector = np.zeros(n)

                    list_of_subvectors = np.append(list_of_subvectors, subvector)

                vec_out = list_of_subvectors

                return vec_out

            #   Falls Matrix
            elif not self.dd_obj.is_vector:

                #   Liste merkt sich die Teilmatrizen, die aus den Nachfolgeknoten zurückgegeben werden
                list_of_submatrizes = np.array([[]])

                #   Für jeden Ast wird das neue Upstream-Kantengewicht berechnet und die Funktion rekursiv aufgerufen
                #   und die Teilmatrix in der Liste gespeichert
                for i in range(4):
                    upstream_ew = upstream_edge_weight * self.list_outgoing_edges[i].edge_weight
                    submatrix = self.list_outgoing_edges[i].target_node.get_matrix(upstream_ew)

                    #   Falls die Teilmatrix nur das Element 0 enthält, wird aus dem in der entsprechenden Kante
                    #   gespeicherten Wert (Anzahl der verschiedenen Pfade auf den 0-Knoten, die durch diese Kante
                    #   repräsentiert werden), die Matrix/der Vektor auf die entsprechende Größe erweitert. Selbe Größe,
                    #   wie die anderen Teilmatrizen.
                    if np.array_equal(submatrix, [[0]]):
                        n = self.list_outgoing_edges[i].n_possible_paths_to_zero
                        submatrix = np.zeros((n, n))

                    list_of_submatrizes = np.append(list_of_submatrizes, submatrix)

                #   Teilmatrizen werden so zusammengefasst, dass alle Teilmatrizen immer die selbe Größe haben
                m_0x = np.append(list_of_submatrizes[0], list_of_submatrizes[1], 0)
                m_1x = np.append(list_of_submatrizes[2], list_of_submatrizes[3], 0)

                matrix_out = np.append(m_0x, m_1x, 1)

                return matrix_out

            else:
                print('Fehler beim Umwandeln des Entscheidungsdiagramms in einen Vektor oder Matrix.'
                      '\nKnoten müssen entweder 2 oder 4 ausgehende Kanten haben, Vektor oder Matrix.')

        #   Falls Knoten keine ausgehenden Kanten hat, ist er ein Endknoten
        else:

            #   Es wird das Produkt aus dem im Knoten gespeicherten Wert und dem Upstream-Kantengewicht als Vektor oder
            #   Matrix zurückgegeben
            if self.dd_obj.is_vector:
                return np.array([self.saved_value_on_node * upstream_edge_weight])
            else:
                return np.array([[self.saved_value_on_node * upstream_edge_weight]])

