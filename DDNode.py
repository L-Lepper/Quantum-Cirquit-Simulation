#   Projektarbeit "Recherche und Tool zur Simulation von Quantenschaltungen im Bereich Quantencomputing"
#   Author: Lukas Lepper, 24.11.2020
#   Betreuer: Dipl.-Ing. Martin Hardieck
#   Dateiname: DDNode.py
#   Version: 0.6


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

        #   wird zum löschen benötigt (in dd-obj sind die Listen aller Kanten und Knoten gespeichert)
        self.dd_obj = dd_obj_in
        super().__init__()

    def call_upstream(self, str_in):
        """
        ToDo: Funktion überarbeiten, diese Variante ist immer noch nicht so übersichtlich
        Die Funktion wird anstatt __str__ verwendet, damit sie besser rekursiv aufgerufen werden kann. Zusammen mit der
        print-Funktion in DDEdge, wird für jede neue Ebene, die ausgabe weiter eingerückt, sodass die Baumstrucktur
        besser erkennbar wird. Das ist bei einer höheren Anzahl nicht mehr so übersichtlich!
        :param str_in: Diesem Parameter wird durch jeden Aufruf ein Tabulator hinzugefügt. (Jeder Aufruf bedeutet eine
            neue Ebene, die auch weiter eingerükt werden soll.
        :return:
        """

        str_in += '\t'
        str_out = ''

        #   Falls der Knoten ausgehende Kanten hat, wird für jede Kante eine Ausgabezeile erzeugt, zusammen mit dem
        #   neuen Abstand str_in
        if any(self.list_incoming_edges):

            for edge in self.list_incoming_edges:
                str_out += str_in + edge.print_upstream(str_in)

        return str_out


    def print_recursive(self, str_in):
        """
        Die Funktion wird anstatt __str__ verwendet, damit sie besser rekursiv aufgerufen werden kann. Zusammen mit der
        print-Funktion in DDEdge, wird für jede neue Ebene, die ausgabe weiter eingerückt, sodass die Baumstrucktur
        besser erkennbar wird. Das ist bei einer höheren Anzahl nicht mehr so übersichtlich!
        :param str_in: Diesem Parameter wird durch jeden Aufruf ein Tabulator hinzugefügt. (Jeder Aufruf bedeutet eine
            neue Ebene, die auch weiter eingerükt werden soll.
        :return:
        """

        str_in += '\t'
        str_out = ''

        #   Falls der Knoten ausgehende Kanten hat, wird für jede Kante eine Ausgabezeile erzeugt, zusammen mit dem
        #   neuen Abstand str_in
        if any(self.list_outgoing_edges):

            for edge in self.list_outgoing_edges:
                str_out += str_in + edge.print_recursive(str_in)

        return str_out

    def delete_node(self):
        """
        Löscht den betreffenden Knoten und den gesamten nachfolgenden Baum, wenn dieser nicht durch andere Äste
        erreicht wird.
        Knoten wird aus der Liste aller Knoten entfernt.
        Falls dieser Knoten eingehende Kanten hat, müssen sie erst entfernt werden, um sicher zu gehen, dass sie nicht
        vergessen wurden. Funktion gibt sonst Fehler aus und bricht das Programm ab.
        :return:
        """

        #   Prüfe Liste der eingehenden Kanten
        #   Falls der Knoten noch eingehende Kanten gespeichert hat, besteht die Gefahr, das die Kanten nicht gelöscht
        #   werden und noch auf diesen Knoten zeigen. Dadurch wird dieser nicht durch die Garbage Collection entfernt
        #   und das DD nicht abgeschnitten, der Teilbaum ist über diese Kanten weiter erreichbar, auch wenn er nicht
        #   mehr in der Liste aller Knoten und Kanten vorkommt.
        if any(self.list_incoming_edges):
            raise Exception('Error by deleting node of decision diagram: List of incoming edges have to be empty\n'
                            'or edge have to point on an other node to avoid edges without target node.')

        #   Jede ausgehende Kante des Knotens wird gelöscht, damit alle Nachfolger aus den jeweiligen Listen
        #   herausgenommen werden (rekursives Aufrufen von delete_node() )
        for edge in self.list_outgoing_edges:

            #   suche diesen Knoten in der Liste aller Knoten, und aktualisiere dort die Liste der eingehenden Kanten
            for index_layer, layer in enumerate(self.dd_obj.list_of_all_nodes):
                try:
                    index_node = layer.index(edge.target_node)

                    #   Suche den Index der Kante in der Liste der eingehenden Kanten
                    #   list_incoming_edges hat nur eine Dimension, np.where gibt das Tuple (array([INDEX], dtype=int64),)
                    #   zurück. Dabei ist [INDEX] eine Liste mit Indizes, an denen das gesuchte Element gefunden wurde.
                    #   In einem 2D Array sähe das Tupel mit Listen für die x- und y-Komponente so aus:
                    #   (array([x1, x2, x3], dtype=int64), array([y1, y2, y3], dtype=int64))
                    #   Hier sollte index_list_x so aussehen: [1]
                    #   np.where funktioniert nicht, edge wird nicht gefunden
                    #index_incoming_list = np.where(edge.target_node.list_incoming_edges == edge)[0]
                    new_list = []
                    for element in edge.target_node.list_incoming_edges:
                        new_list += [element]
                    index_incoming_list = [new_list.index(edge)]

                    #   Es sollte nur ein Index gefunden werden, die Kante kann aus der Liste entfernt werden.
                    if np.size(index_incoming_list) == 1:
                        self.dd_obj.list_of_all_nodes[index_layer][index_node].list_incoming_edges = np.delete(
                            self.dd_obj.list_of_all_nodes[index_layer][index_node].list_incoming_edges,
                            index_incoming_list[0])

                        #   Falls der Zielknoten jetzt keine eingehenden Kanten mehr hat und er nicht der 0 oder 1
                        #   Knoten in der letzten Ebene ist, wird er gelöscht
                        if not any(self.dd_obj.list_of_all_nodes[index_layer][index_node].list_incoming_edges) \
                                and index_layer != Base.getnqubits():
                            self.dd_obj.list_of_all_nodes[index_layer][index_node].delete_node()

                    #   Die Kante wurde in der Liste nicht gefunden, sie hätte aber drin sein müssen,
                    #   da sie auf diesen Knoten zeigt
                    elif np.size(index_incoming_list) == 0:
                        raise Exception('Error when deleting an edge in the decision diagram.\n'
                                        'The List of incoming edges doesn\'t contain the edge', edge,
                                        ',\nbut it was expected. Error in the Decision Diagram.')

                    #   Die Kante ist doppelt, wenn sie mehfach vorkommt. Sollte auch nicht passieren.
                    else:
                        for i in index_incoming_list:
                            self.dd_obj.list_of_all_nodes[index_layer][index_node].list_incoming_edges = np.delete(
                                self.dd_obj.list_of_all_nodes[index_layer][index_node].list_incoming_edges,
                                index_incoming_list[i])

                        if Base.get_verbose() >= 0:
                            print('Error when deleting an edge in the decision diagram.\n'
                                  'The edge to be deleted should occur only once in qsim_obj.target_node.list_incoming_edges.\n'
                                  'Error in the Decision Diagram.')

                    #   Lösche die Kante in der Liste aller Kanten
                    self.dd_obj.delete_edge_list_of_all_edges(edge)

                    break

                except ValueError:
                    continue

        #   Dieser Knoten wird aus der Liste aller Knoten gelöscht
        n = 0
        for layer in self.dd_obj.list_of_all_nodes:

            #   Prüfe Ebene für Ebene, ob Knoten enthalten ist (Kann in 2D Liste nicht einzeln gefunden werden)
            #   Zähle Anzahl, wie oft er gefunden wurde, sollte nur einmal vorkommen.
            try:
                layer.remove(self)
                n += 1
                break

            #   Gibt es einen ValueError, ist Knoten in dieser Ebene nicht vorhanden
            except ValueError:
                continue

        #   Knoten wird wegen break oben nur einmal gefunden. Er kommt eigentlich auch nicht öfter vor, so ist das
        #   Programm ein bisschen schneller
        if n != 1:
            raise Exception('Error by deleting node in list of all nodes:', self,
                            '\nNode have to exists exactly once, but fund', n, ' times.')

    def delete_edge_in_incoming_list(self, edge_in):
        """
        Die Funktion entfernt eine Kante aus der Liste der eingehenden Kanten von diesem Knoten. Dazu wird der aktuelle
        Knoten in der Liste aller Knoten gesucht, um den Knoten dort zu verändern. Das soll Probleme vermeiden, wenn
        Objekt-Weitergabe doch keine Reeferenz ist. Programm bricht mit Fehler ab, wenn Kante nicht gefunden wurde.

        :param edge_in: Kante, die aus der Liste der eingehenden Kanten entfernt werden soll.
        :return:
        """

        #   suche diesen Knoten in der Liste aller Knoten, und aktualisiere dort die Liste der eingehenden Kanten
        for index_layer, layer in enumerate(self.dd_obj.list_of_all_nodes):
            try:
                index_node = layer.index(self)

                #   list_incoming_edges hat nur eine Dimension, np.where gibt das Tuple (array([INDEX], dtype=int64),)
                #   zurück. Dabei ist [INDEX] eine Liste mit Indizes, an denen das gesuchte Element gefunden wurde.
                #   In einem 2D Array sähe das Tupel mit Listen für die x- und y-Komponente so aus:
                #   (array([x1, x2, x3], dtype=int64), array([y1, y2, y3], dtype=int64))
                #   Hier sollte index_list_x so aussehen: [1]
                index_list_x = np.where(self.list_incoming_edges == edge_in)[0]

                #   Es sollte nur ein Index gefunden werden, die Kante kann aus der Liste entfernt werden.
                if np.size(index_list_x) == 1:
                    self.dd_obj.list_of_all_nodes[index_layer][index_node].list_incoming_edges = np.delete(self.list_incoming_edges, index_list_x[0])

                #   Die Kante wurde in der Liste nicht gefunden, sie hätte aber drin sein müssen,
                #   da sie auf diesen Knoten zeigt
                elif np.size(index_list_x) == 0:
                    raise Exception('Error when deleting an edge in the decision diagram.\n'
                                    'The List of incoming edges doesn\'t contain the edge', self,
                                    ',\nbut it was expected. Error in the Decision Diagram.')

                #   Die Kante ist doppelt, wenn sie mehfach vorkommt. Sollte auch nicht passieren.
                else:
                    for i in index_list_x:
                        self.list_incoming_edges = np.delete(self.list_incoming_edges, index_list_x[i])

                    if Base.get_verbose() >= 0:
                        print('Error when deleting an edge in the decision diagram.\n'
                              'The edge to be deleted should occur only once in qsim_obj.target_node.list_incoming_edges.\n'
                              'Error in the Decision Diagram.')
                break

            except ValueError:
                continue

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
                    #   gespeicherten Wert für die Anzahl der verschiedenen Pfade auf den 0-Knoten, die durch diese
                    #   Kante repräsentiert werden, die Matrix/der Vektor auf die entsprechende Größe erweitert.
                    #   Selbe Größe, wie die anderen Teilmatrizen.
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
                raise Exception('Error when converting the decision diagram into a vector or matrix.\n'
                                'Nodes must have either 2 or 4 outgoing edges, vector or matrix.')

        #   Falls Knoten keine ausgehenden Kanten hat, ist er ein Endknoten
        else:

            #   Es wird das Produkt aus dem im Knoten gespeicherten Wert und dem Upstream-Kantengewicht als Vektor oder
            #   Matrix zurückgegeben
            if self.dd_obj.is_vector:
                #   Als Vektor
                return np.array([self.saved_value_on_node * upstream_edge_weight])
            else:
                #   Als Matrix
                return np.array([[self.saved_value_on_node * upstream_edge_weight]])
