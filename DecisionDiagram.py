#   Projektarbeit Literaturrecherche zu Simulationsalgorithmen für Quantencomputing
#   Author: Lukas Lepper, 24.11.2020
#   Betreuer: Martin Hardieck
#   Dateiname: DecisionDiagram.py
#   Version: 0.6


import numpy as np
from Base import Base
from DDNode import DDNode
from DDEdge import DDEdge

from copy import deepcopy


class DecisionDiagram(Base):
    """
    Klasse für Entscheidungsdiagramme. Durch Erzeugen von Objekten mit einer Matrix oder einem Vektor, wird das
    entsprechende Entscheidungsdiagramm aus Knoten- und Kantenobjekten gebaut, die in Form von Listen gespeichert
    werden.
    """

    def __init__(self, matrix_in):
        """
        Konstruktor ruft Memberfunktion create_dd auf und erzeugt Entscheidungsdiagramm
        :param matrix_in: Matrix oder Vektor, ausdem Entscheidungsdiagramm erstellt wird
        """
        #   Wird ein Vektor dargestellt oder eine Matrix?
        #   Falls Matrix:
        if np.ndim(matrix_in) == 2:
            self.is_vector = False
        #   Falls Vektor
        elif np.ndim(matrix_in) == 1:
            self.is_vector = True
        else:
            raise Exception('Invalid matrix: either vector or square matrix expected.')

        #   Liste aller Kanten
        self.list_of_all_edges = np.array([])

        #   Leere Liste für alle Knoten: alle Knoten einer Ebene werden in einer eigenen Zeile gespeichert
        self.list_of_all_nodes = [[] for i in range(Base.getnqubits() + 1)]

        #   Variable wird benötigt, um das Entscheidungsdiagramm aufzubauen:
        #   Liste aller Knoten in der betrachteten Ebene
        self.list_of_nodes_per_level = np.array([])

        #   Objekte mit den Adressen, wo der Start und die Endknoten gespeichert sind
        self.node_root = None
        self.node_zero = None
        self.node_one = None

        #   Wird später in Funktion benötigt, um pro Ebene den ersten Knoten zu erstellen
        self.first_time = True

        #   In dieser Liste werden alle Knoten einer Ebene zwischengespeichert, und auf Redundanz überprüft.
        self.shared_memory_for_equivalence_check = np.array([])

        #   Entscheidungsdiagramm aufbauen
        self.create_dd(matrix_in)

        super().__init__()

    def __str__(self):
        print('Print Decision Diagram:\n')

        #   Debug Verbose-Level 3
        if Base.get_verbose() >= 3:
            print('(\'count to zero\' means the number of edges to zero represented by this edge.)\n')

            #   Ebenen im Entscheidungsdiagramm
            for index, row in enumerate(self.list_of_all_nodes):
                print('layer ', index, ':')

                #   Knoten einer Ebene
                for j, node in enumerate(row):
                    print('\tnode', j, ':', node.saved_value_on_node,
                          ', number of incoming edges:', np.size(node.list_incoming_edges))

                    if index == 0:
                        #   print Eingehende Kante des Wurzelknotens
                        print('\t\tincoming edge of root node:')
                        print('\t\t\tedge weight\t', node.list_incoming_edges[0].edge_weight,
                              '\n\t\t\toccurrence\t', node.list_incoming_edges[0].count_of_paths,
                              '\n\t\t\tcount to zero\t', node.list_incoming_edges[0].n_possible_paths_to_zero,
                              '\n\t\t\tedge probability\t', node.list_incoming_edges[0].edge_probability,
                              '\n\t\t\tconditional probability\t', node.list_incoming_edges[0].conditional_probability)

                    #   print Ausgehende Kanten
                    for k, edge in enumerate(node.list_outgoing_edges):
                        print('\t\toutgoing edges', k, ':')
                        print('\t\t\tedge weight\t', edge.edge_weight,
                              '\n\t\t\toccurrence\t', edge.count_of_paths,
                              '\n\t\t\tcount to zero\t', edge.n_possible_paths_to_zero,
                              '\n\t\t\tedge probability\t', edge.edge_probability,
                              '\n\t\t\tconditional probability\t', edge.conditional_probability,
                              '\n\t\t\ttarget node', edge.target_node.saved_value_on_node)

            #   Berechne Anzahl aller Kanten und Knoten
            n = 0
            for level in self.list_of_all_nodes:
                n += len(level)

            e = np.size(self.list_of_all_edges)
            print('Number of all nodes:', n, ', number of all edges:', e, '\n')

        #   Debug Verbose-Level 2
        if Base.get_verbose() == 2:

            #   Ebenen im Entscheidungsdiagramm
            for index, row in enumerate(self.list_of_all_nodes):
                print('layer ', index, ':')

                #   Knoten einer Ebene
                for j, node in enumerate(row):
                    print('\tnode ', j, ': ', node.saved_value_on_node)

                    if index == 0:
                        #   print Eingehende Kante des Wurzelknotens
                        print('\t\tincoming edge of root node:')
                        print('\t\t\tedge weight\t', node.list_incoming_edges[0].edge_weight)

                    #   print Ausgehende Kanten
                    for k, edge in enumerate(node.list_outgoing_edges):
                        print('\t\toutgoing edges', k, ':')
                        print('\t\t\tedge weight\t', edge.edge_weight,
                              '\n\t\t\ttarget node', edge.target_node.saved_value_on_node)

            #   Berechne Anzahl aller Kanten und Knoten
            n = 0
            for level in self.list_of_all_nodes:
                n += len(level)

            e = np.size(self.list_of_all_edges)
            print('Number of all nodes:', n, ', number of all edges:', e, '\n')

        return '\n'

    def set_is_calculated_false(self):
        """
        Funktion setzt für alle Objekte der Klassen DDNode, DDEdge die Variable is_calculated auf False. Diese Variable
        wird benötigt, damit bei rekursivem Funktionsaufruf der Memberfunktionen einzelne Objekte nicht mehrfach
        berechnet werden. Das zurücksetzen kann nicht in diesen Objekten erfolgen, da sie keine Information darüber
        haben, wann die Berechnung abgeschlossen ist.
        :return:
        """

        #   is_calculated für alle Kanten auf False setzen
        for edge in self.list_of_all_edges:
            edge.is_calculated = False

        #   is_calculated für alle Knoten auf False setzen
        for row in self.list_of_all_nodes:
            for node in row:
                node.is_calculated = False

    def create_dd(self, matrix_in):
        """
        Die Funktion baut das Entscheidungsdiagramm aus einem Vektor oder einer Matrix auf. Die Knoten speichern
        Zwischenergebnisse in saved_value_on_node. Die einzelnen Schritte, wie das Diagramm aufgebaut wird, sind in der
        Datei "Anleitung - Entscheidungsdiagramm und Messung - v4.pdf" gespeichert. ToDo: Dateiname überprüfen
        :param matrix_in: Matrix oder Vektor aus dem das Entscheidungsdiagramm erstellt wird
        :return:
        """

        #   Debug Ausgabe für das erstellte Entscheidungsdiagramm
        if Base.get_verbose() >= 3:
            print('\n--------------------\t'
                  'Output all partial results of creating a decision diagram'
                  '\t--------------------\n')

        """ SCHRITT 1 + 2 """

        #   Für jede Ebene werden die Knoten bestimmt, gleiche Knoten werden zusammengefasst und ihre Kanten in einer
        #   Liste zusammengeführt
        for level_index in range(Base.getnqubits() + 1):
            determine_nodes_on_level(self, level_index, matrix_in)

            #   Der 2-Dimensionalen Liste aller Knoten wird pro Zeile die Liste der Knoten pro Ebene angehängt
            self.list_of_all_nodes[level_index] += self.list_of_nodes_per_level.tolist()

        #   Ausgabe der Matrizen im vollständigen Diagramm, die momentan in den Knoten gespeichert sind, falls
        #   debug True. Ansprechen der Knoten über jede einzelne Kante
        if Base.get_verbose() >= 3:
            print(
                '\nTest the structure of the decision diagram after steps 1 and 2 '
                '(See instructions in documentation folder).\n'
                'Starting with the root edge, the value stored in the target node is output for each edge.\n'
                'Currently this is the respective sub-matrix:')

            #   Ebenen im Entscheidungsdiagramm
            for index, row in enumerate(self.list_of_all_nodes):
                print('layer ', index, ':')

                #   Knoten einer Ebene
                for j, node in enumerate(row):
                    print('\tnode ', j, ':')

                    if index == 0:
                        #   print Eingehende Kante des Wurzelknotens
                        print('\t\tincoming edge of root node:')
                        print('\t\t\ttarget node', node.list_incoming_edges[0].target_node.saved_value_on_node)

                    #   print Ausgehende Kanten
                    for k, edge in enumerate(node.list_outgoing_edges):
                        print('\t\toutgoing edges', k, ':')
                        print('\t\t\ttarget node', edge.target_node.saved_value_on_node)

            #   Berechne Anzahl aller Kanten und Knoten
            n = 0
            for level in self.list_of_all_nodes:
                n += len(level)

            e = np.size(self.list_of_all_edges)
            print('Number of all nodes:', n, ', number of all edges:', e, '\n')

            #   Ausgabe aller elementaren Knoten, durch die Matrix die dort gespeichert ist
            print('Test the number of different nodes. Nodes from identical submatrices are combined:\n')
            #   print alle Knoten in der 2D Liste
            for index, row in enumerate(self.list_of_all_nodes):
                print('nodes of layer', index, ':')
                for j, node in enumerate(row):
                    print('\tnode ', j, ': ', str(node.saved_value_on_node))

        """ SCHRITT 3 """

        #   Von den Nachfolgeknoten wird der größte Wert auf den Elternknoten übertragen
        self.list_of_all_nodes[0][0].get_max_value_of_target_nodes()
        self.set_is_calculated_false()

        #   Ausgabe der übertragenen Werte
        if Base.get_verbose() >= 3:
            print('\n\nTest of step 3 with the values transferred to the parent nodes (max from successor nodes).\n'
                  'A zero ending node is always present here, even if no edge points to it:\n')
            #   print alle Knoten in der 2D Liste
            for index, row in enumerate(self.list_of_all_nodes):
                print('nodes of layer', index, ':')
                for j, node in enumerate(row):
                    print('\tnode ', j, ': ', str(node.saved_value_on_node))

        """ SCHRITT 4 """

        #   Berechne Kantengewichte aller Kanten
        self.list_of_all_edges[0].calc_edge_weight()
        self.set_is_calculated_false()

        """ SCHRITT 5 """

        #   In der letzten Ebene der Knoten wurden die Einträge der Matrix/Vektor gespeichert, die für die Funktion
        #   zuvor benötigt wurde. Damit das Diagramm später normiert ist, muss Endknoten entweder 0 oder 1 sein
        remember_edges = np.array([])

        #   Speichere für jeden Knoten in der letzten Ebene, dessen Wert ungleich 0 ist,
        #   die Liste der eingehenden Kanten
        for node in self.list_of_all_nodes[Base.getnqubits()][:]:
            if node.saved_value_on_node != 0:
                remember_edges = np.append(remember_edges, node.list_incoming_edges)

                #   Entferne den Knoten, dessen eingehenden Kanten gerade gespeichert wurden
                self.list_of_all_nodes[Base.getnqubits()].remove(node)

        #   Erstelle den 1-Endknoten mit den zuvor gespeicherten eingehenden Kanten
        self.node_one = DDNode(remember_edges, np.array([]), self)
        self.node_one.saved_value_on_node = 1

        #   Ändere den Zielknoten jeder gespeicherten Kante auf den erstellten 1-Endknoten
        for edge in remember_edges:
            edge.target_node = self.node_one

        #   Füge den 1-Endknoten der letzten Ebene der Liste aller Knoten hinzu (besteht jetzt nur noch aus dem 0- und
        #   1-Endknoten)
        self.list_of_all_nodes[Base.getnqubits()] += [self.node_one]

        #   Ausgabe der übertragenen Werte
        if Base.get_verbose() >= 3:
            print('\n\nTest for step 4 and 5 - Decision diagram with edge weights:\n')

            #   Ebenen im Entscheidungsdiagramm
            for index, row in enumerate(self.list_of_all_nodes):
                print('layer ', index, ':')

                #   Knoten einer Ebene
                for j, node in enumerate(row):
                    print('\tnode ', j, ':')

                    if index == 0:
                        #   print Eingehende Kante des Wurzelknotens
                        print('\t\tincoming edge of root node:')
                        print('\t\t\tedge weight\t', node.list_incoming_edges[0].edge_weight,
                              '\n\t\t\ttarget node', node.list_incoming_edges[0].target_node.saved_value_on_node)

                    #   print Ausgehende Kanten
                    for k, edge in enumerate(node.list_outgoing_edges):
                        print('\t\toutgoing edges', k, ':')
                        print('\t\t\tedge weight\t', edge.edge_weight,
                              '\n\t\t\ttarget node', edge.target_node.saved_value_on_node)

            #   Berechne Anzahl aller Kanten und Knoten
            n = 0
            for level in self.list_of_all_nodes:
                n += len(level)

            e = np.size(self.list_of_all_edges)
            print('Number of all nodes:', n, ', number of all edges:', e, '\n')

        """ SCHRITT 6 """

        #   Berechnen der gewichteten Wahrscheinlichkeit aller Knoten (p=p_left * w_left^2 + p_right * w_right^2)
        self.list_of_all_nodes[0][0].get_weighted_propability_of_node()
        self.set_is_calculated_false()

        #   Ausgabe der gewichteten Wahrscheinlichkeit aller Knoten
        if Base.get_verbose() >= 3:
            print('\n\nTest for step 6 - Weighted probability of all nodes:\n')

            #   Ebenen im Entscheidungsdiagramm
            for index, row in enumerate(self.list_of_all_nodes):
                print('layer ', index, ':')

                #   Knoten einer Ebene
                for j, node in enumerate(row):
                    print('\tnode ', j, ':')

                    if index == 0:
                        #   print Eingehende Kante des Wurzelknotens
                        print('\t\tincoming edge of root node:')
                        print('\t\t\ttarget node', node.list_incoming_edges[0].target_node.saved_value_on_node)

                    #   print Ausgehende Kanten
                    for k, edge in enumerate(node.list_outgoing_edges):
                        print('\t\toutgoing edges', k, ':')
                        print('\t\t\ttarget node', edge.target_node.saved_value_on_node)

            #   Berechne Anzahl aller Kanten und Knoten
            n = 0
            for level in self.list_of_all_nodes:
                n += len(level)

            e = np.size(self.list_of_all_edges)
            print('Number of all nodes:', n, ', number of all edges:', e, '\n')

        """ SCHRITT 7 """

        self.merge_dd_step7()

        #   Für jede Kante wird die Anzahl berechnet, wie häufig sie in den Ästen vorkommt
        self.list_of_all_edges[0].calc_count_of_paths()
        self.set_is_calculated_false()

        #   Ausgabe der Häufigkeit der Kanten und Test für zusammengefasste Knoten
        if Base.get_verbose() >= 3:
            print('\n\nTest for step 7 - Merged nodes:\n')

            #   Ebenen im Entscheidungsdiagramm
            for index, row in enumerate(self.list_of_all_nodes):
                print('layer ', index, ':')

                #   Knoten einer Ebene
                for j, node in enumerate(row):
                    print('\tnode ', j, ':')

                    if index == 0:
                        #   print Eingehende Kante des Wurzelknotens
                        print('\t\tincoming edge of root node:')
                        print('\t\t\tedge weight\t', node.list_incoming_edges[0].edge_weight,
                              '\n\t\t\toccurrence\t', node.list_incoming_edges[0].count_of_paths,
                              '\n\t\t\ttarget node', node.list_incoming_edges[0].target_node.saved_value_on_node)

                    #   print Ausgehende Kanten
                    for k, edge in enumerate(node.list_outgoing_edges):
                        print('\t\toutgoing edges', k, ':')
                        print('\t\t\tedge weight\t', edge.edge_weight,
                              '\n\t\t\toccurrence\t', edge.count_of_paths,
                              '\n\t\t\ttarget node', edge.target_node.saved_value_on_node)

            #   Berechne Anzahl aller Kanten und Knoten
            n = 0
            for level in self.list_of_all_nodes:
                n += len(level)

            e = np.size(self.list_of_all_edges)
            print('Number of all nodes:', n, ', number of all edges:', e, '\n')

    def calc_probabilities_if_vector(self):
        """
        In dieser Funktion sind die Schritte beim Aufbauen des Entscheidungsdiagramms entahlten, wenn ein
        Zustandsvektror dargestellt wird und die Wahrscheinlichkeiten berechnet werden sollen. Die Berechnung der
        gewichteten Wahrscheinlichkeiten in Schritt 6 könnt auch noch hier stehen, aber die Ergebnisse werden in den
        Knoten unter saved_value noch benötigt, um Knoten in Schritt 7 zusammenzufassen.
        :return:
        """

        """ SCHRITT 8 """

        #   Berechnen des Produktes aller Kantengewichte auf dem Ast von der jeweiligen Kante bis zur Wurzelkante
        self.list_of_all_edges[0].calc_product_of_weights(1)
        self.set_is_calculated_false()

        #   Ausgabe des Produktes aller Kantengewichte hoch zur Wurzelkante
        if Base.get_verbose() >= 3:
            print('\n\nTest of step 8 - Calculated products of the edge weights:\n')

            #   Ebenen im Entscheidungsdiagramm
            for index, row in enumerate(self.list_of_all_nodes):
                print('layer ', index, ':')

                #   Knoten einer Ebene
                for j, node in enumerate(row):
                    print('\tnode ', j, ':')

                    if index == 0:
                        #   print Eingehende Kante des Wurzelknotens
                        print('\t\tincoming edge of root node:')
                        print('\t\t\tproduct of edge weights\t', node.list_incoming_edges[0].edge_probability,
                              '\n\t\t\ttarget node', node.list_incoming_edges[0].target_node.saved_value_on_node)

                    #   print Ausgehende Kanten
                    for k, edge in enumerate(node.list_outgoing_edges):
                        print('\t\toutgoing edges', k, ':')
                        print('\t\t\tproduct of edge weights\t', edge.edge_probability,
                              '\n\t\t\ttarget node', edge.target_node.saved_value_on_node)

            #   Leerzeile nach der Ausgabe
            print('\n')

        """ SCHRITT 9 """

        #   Berechnen der Wahrscheinlichkeit an jeder Kante (Wert im Zielknoten multipliziert mit oben berechneten
        #   Produkt der Kantengewichte, welches in edge_probability gespeichert ist)
        self.list_of_all_edges[0].calc_edge_propability()
        self.set_is_calculated_false()

        #   Ausgabe der Wahrscheinlichkeit aller Kanten
        if Base.get_verbose() >= 3:
            print('\n\nTest of the calculated probabilities in step 9:\n')

            #   Ebenen im Entscheidungsdiagramm
            for index, row in enumerate(self.list_of_all_nodes):
                print('layer ', index, ':')
                sum_probability_per_level = 0

                #   Knoten einer Ebene
                for j, node in enumerate(row):
                    print('\tnode ', j, ':')

                    if index == 0:
                        #   print Eingehende Kante des Wurzelknotens
                        print('\t\tincoming edge of root node:')
                        print('\t\t\tedge probability\t', node.list_incoming_edges[0].edge_probability,
                              '\n\t\t\ttarget node', node.list_incoming_edges[0].target_node.saved_value_on_node)

                    #   print Ausgehende Kanten
                    for k, edge in enumerate(node.list_outgoing_edges):
                        print('\t\toutgoing edges', k, ':')
                        print('\t\t\tedge probability\t', edge.edge_probability,
                              '\n\t\t\ttarget node', edge.target_node.saved_value_on_node)
                        sum_probability_per_level += edge.edge_probability

                print('Sum of the probabilities on this layer:', sum_probability_per_level, '\n')

        """ SCHRITT 10 """

        #   Berechne dei bedingte Wahrscheinlichkeit der Kanten: Entscheidung nach jedem Knoten entweder linker
        #   oder rechter Ast. Summe der ausgehenden Äste = 1.
        self.list_of_all_edges[0].calc_conditional_probabilities()
        self.set_is_calculated_false()

        #   Ausgabe der berechneten bedingten Wahrscheinlichkeit für jede Kante
        if Base.get_verbose() >= 3:
            print('\n\nTest the conditional probabilities in step 10:\n')

            #   Ebenen im Entscheidungsdiagramm
            for index, row in enumerate(self.list_of_all_nodes):
                print('layer ', index, ':')

                #   Knoten einer Ebene
                for j, node in enumerate(row):
                    print('\tnode ', j, ':')
                    sum_probability_per_node = 0

                    if index == 0:
                        #   print Eingehende Kante des Wurzelknotens
                        print('\t\tincoming edge of root node:')
                        print('\t\t\tconditional probability\t', node.list_incoming_edges[0].conditional_probability,
                              '\n\t\t\ttarget node', node.list_incoming_edges[0].target_node.saved_value_on_node)

                    #   print Ausgehende Kanten
                    for k, edge in enumerate(node.list_outgoing_edges):
                        print('\t\toutgoing edges', k, ':')
                        print('\t\t\tconditional probability\t', edge.conditional_probability,
                              '\n\t\t\ttarget node', edge.target_node.saved_value_on_node)
                        sum_probability_per_node += edge.conditional_probability

                    print('Sum of the conditional probabilities:', sum_probability_per_node, '\n')

            print('Recursive call of edges and nodes of the decision diagram:\n'
                  '(edge weight | saved value on node)\n', self.list_of_all_edges[0])
        a = 2

    def create_matrix(self):
        """
        Funktion ruft die Funktion get_matrix() für den ersten Knoten auf. Dadurch wird rekursiv die Matrix/ der Vektor
         bestimmt.
        :return: Vektor/Matrix, der mit dem Entscheidungsdiagramm dargestellt wird.
        """

        return self.list_of_all_nodes[0][0].get_matrix(self.list_of_all_edges[0].edge_weight)

    def merge_nodes_from_list(self, list_indices_of_nodes, list_nodes_to_del):
        """
        Um Knoten in Schritt 7 zusammenzufassen, werden mit dieser Funktion eine Auswahl an Knoten auf gleiche Äste
        überprüft. Die "gewichteten Wahrscheinlichkeiten", die noch in den Knoten in saved_value gespeichert sind, und
        die Kantengewichte reichen nicht aus, um Äste sicher zusammenzufassen. (1. Knoten: Kantengewicht links = 0.5,
        KG. rechts = 1; 2. Knoten: KG links = 1 und Kantengewicht rechts = 0.5; Zielknoten sind der 1-Endknoten. Dann
        ergibt sich der selbe Wert für saved_value des Quellknotens, und eine Ebene darüber soll dann evt. dieser Knoten
        zusammenfassengefasst werden. Die Ebene sieht aber nicht, dass am unteren Ende die Kantengewichte vertauscht
        sind und desswegen der gleiche Wert herausgekommen ist.

        Desswegen werden zuerst nur die Knoten in der untersten Ebene betrachtet. Können Knoten zusammengefassst werden,
        werden die Quellknoten an den eingehenden Kanten in einer Liste gespeichert und diese Funktion für diese direkt
        rekursiv aufgerufen, sodass dem Ast entlang nach oben geprüft wird, welche Knoten zusammengefasst werden können.
        Sind auf der untersten Ebene die Knoten nicht identisch, können auch weiter oben keine Knoten zusammengefasst
        werden.
        Außerdem werden anstatt den Kantengewichte extra Werte in unique_value berechnet, eine Liste mit Werten die aus
        jeder ausgehenden Kante berechnet wurden, damit mehr Informationen verfügbar sind, ob der nachfolgende Ast
        identisch ist.

        :param list_indices_of_nodes: Liste mit Indizes der Knoten in der Liste aller Knoten, die auf gleiche Äste
            überprüft werden sollen.
        :param list_nodes_to_del: In dieser Liste werden Knoten gespeichert, die nach der Zusammenfassung wegfallen,
            und später gelöscht werden sollen. (Indizes veschieben sich sonst)
        :return:
        """

        #   Für jeden Knoten in der übergebenen Liste, werden nacheinander die Index-Paare ausgelesen
        #for i, j in list_indices_of_nodes:

            #   Der Erste Knoten ist der Referenz-Knoten, mit dem die anderen Knoten der Liste
         #   for k in range(j + 1, len(self.list_of_all_nodes[i])):
          #      reference_node = self.list_of_all_nodes[i][j]
           #     compared_node = self.list_of_all_nodes[i][k]

        #   Falls die Funktion für die nächste Ebene mit den Quellknoten der zuvor Zusammengefassten Knoten
        #   aufgerufen wird, kann passieren dass die Quellknoten identisch sind. Der Knoten soll übersprungen werden,
        #   da sonst zwei Elemente in list_indices_of_nodes auf den selben Knoten zeigen und somit dieser Knoten
        #   gelöscht wird, obwohl er nur einmal existiert. Dazu werden sich die Bearbeiteten Knoten gemerkt:
        #   In dieser Liste werden die Indizes k gespeichert, an denen die Knoten bereits verglichen wurden.
        #   Nach dem Zusammenfassen und dem rekursiven Aufruf mit den Quellknoten, können die selben Knoten in der
        #   Liste noch mal vorkommen. ( [[4, 0], [4, 1], [4, 0], [4, 1]] wenn die zusammengefassten Knoten den selben
        #   Quellknoten haben, da er schon beim Erstellen des DD zusammengefasst wurden, weil Teilvektoren identisch
        #   waren.)
        remember_j = []

        #   Für jeden Knoten in der übergebenen Liste, werden nacheinander die Index-Paare ausgelesen. Der aktuelle
        #   Knoten stellt den Referenz-Knoten dar.
        #   index_element wird benötigt, um in der zweiten Schleife in der selben Liste ab dem nächsten Element zu
        #   starten
        for index_element, list_i_j in enumerate(list_indices_of_nodes):
            i, j = list_i_j

            #   Suche den Indek j des Knotens in der Liste, ob der Knoten bereits verglichen wurde. Wird er gefunden,
            #   wird mit dem nächsten weiter gemacht, ansonsten wird der Code unten ausgeführt. k und j bezeichnen
            #   Knoten in der selben Liste
            try:
                temp = remember_j.index(j)
                continue
            except ValueError:
                remember_j += [j]

            #   Es wird eine neue Liste erstellt, in welcher die Knoten j gespeichert sind. Dort werden in der nächsten
            #   Schleife die bereits Verglichenen Knoten gespeichert. Da die Liste list_indices_of_nodes unsortiert ist
            #   und die selben Knoten mehrmals vorkommen können, werden die Knoten j, die in der 1. SChleife schon
            #   bearbeitet wurden in dieser Liste mit aufgenommen, dass sie in der 2. Schleife übersprungen werden
            #   können
            remember_k = deepcopy(remember_j)

            #   In dieser Schleife werden die Knoten in der Liste ab dem Referenzknoten durchgegangen. Diese stellen
            #   den zu vergleichenden Knoten dar
            #   Es werden nur Knoten nach dem Element der oberen Schleife bei index_element verglichen.
            for unused, k in list_indices_of_nodes[index_element + 1:]:

                #   Suche k in der Liste, ob der Knoten bereits verglichen wurde. Wird er gefunden, wird mit dem
                #   nächsten weiter gemacht, ansonsten wird der Code unten ausgeführt.
                try:
                    temp = remember_k.index(k)
                    continue
                except ValueError:
                    remember_k += [k]

                #   Speichere den Referenzknoten j und den zu Vergleichenden k
                reference_node = self.list_of_all_nodes[i][j]
                compared_node = self.list_of_all_nodes[i][k]

                #   Runde den in den Knoten gespeicherten Wert, die miteinander verglichen werden sollen
                #   ToDo Genauigkeit
                round_sv_1 = round(reference_node.saved_value_on_node, 6)
                round_sv_2 = round(compared_node.saved_value_on_node, 6)

                #   Runde den Real- und Imaginärteil der linken ausgehenden Kante beider Knoten (0-Kante)
                #   und bilde wieder eine komplexe Zahl
                #round_ew_1 = (round(reference_node.list_outgoing_edges[0].edge_weight.real, 6)
                 #             + round(reference_node.list_outgoing_edges[0].edge_weight.imag, 6) * 1j)
                #round_ew_2 = (round(compared_node.list_outgoing_edges[0].edge_weight.real, 6)
                 #             + round(compared_node.list_outgoing_edges[0].edge_weight.imag, 6) * 1j)

                #   Runde den Real- und Imaginärteil der rechten ausgehenden Kante beider Knoten (1-Kante)
                #   und bilde wieder eine komplexe Zahl
                #round_ew_3 = (round(reference_node.list_outgoing_edges[1].edge_weight.real, 6)
                 #             + round(reference_node.list_outgoing_edges[1].edge_weight.imag, 6) * 1j)
                #round_ew_4 = (round(compared_node.list_outgoing_edges[1].edge_weight.real, 6)
                 #             + round(compared_node.list_outgoing_edges[1].edge_weight.imag, 6) * 1j)

                #   In der Liste unique_value sind aus jeder ausgehenden Kante Werte aus den Kantengewichten berechnet.
                #   Um zu prüfen ob zwei Kanten identisch sind, müssen also die zwei Werte aus der Liste verglichen
                #   werden. Der Knoten, der zusammengefasst werden soll, hat zwei ausgehende Kanten, also müssen 4 Werte
                #   verglichen werden. Außserdem können die Werte komplex sein, da eventuell kleine ungenauigkeiten
                #   vorhanden sein können, muss als jeweils der Real und Imaginärteil gerundet werden. Anschlißend wird
                #   wieder eine komplexe Zahl erzeugt, die weiter unten verglichen wird.
                #   ToDo: Genauigkeit prüfen
                #   Linker Ast:
                round_uv_1 = (round(reference_node.list_outgoing_edges[0].unique_value[0].real, 6)
                              + round(reference_node.list_outgoing_edges[0].unique_value[0].imag, 6) * 1j)
                round_uv_2 = (round(reference_node.list_outgoing_edges[0].unique_value[1].real, 6)
                              + round(reference_node.list_outgoing_edges[0].unique_value[0].imag, 6) * 1j)
                round_uv_3 = (round(reference_node.list_outgoing_edges[1].unique_value[0].real, 6)
                              + round(reference_node.list_outgoing_edges[1].unique_value[0].imag, 6) * 1j)
                round_uv_4 = (round(reference_node.list_outgoing_edges[1].unique_value[1].real, 6)
                              + round(reference_node.list_outgoing_edges[1].unique_value[0].imag, 6) * 1j)

                #   Rechter Ast
                round_uv_a = (round(compared_node.list_outgoing_edges[0].unique_value[0].real, 6)
                              + round(compared_node.list_outgoing_edges[0].edge_weight.imag, 6) * 1j)
                round_uv_b = (round(compared_node.list_outgoing_edges[0].unique_value[1].real, 6)
                              + round(compared_node.list_outgoing_edges[0].edge_weight.imag, 6) * 1j)
                round_uv_c = (round(compared_node.list_outgoing_edges[1].unique_value[0].real, 6)
                              + round(compared_node.list_outgoing_edges[1].edge_weight.imag, 6) * 1j)
                round_uv_d = (round(compared_node.list_outgoing_edges[1].unique_value[1].real, 6)
                              + round(compared_node.list_outgoing_edges[1].edge_weight.imag, 6) * 1j)

                #   Sind die 4 Werte der Kanten und Wert in den Knoten identisch, können die beiden Knoten zusammen-
                #   gefasst werden.
                #   Der Test, ob der Wert in saved_value gleich ist, ist zwingend notwendig!
                #   ToDo: Möglicherweise ist die Berechnung unique_value auch nicht ganz so eindeutig?
                if round_sv_1 == round_sv_2 and round_uv_1 == round_uv_a and round_uv_2 == round_uv_b \
                        and round_uv_3 == round_uv_c and round_uv_4 == round_uv_d:

                    #   Der compared_node soll gelöscht werden, ändere den Zielknoten aller eingehenden Kanten
                    #   des compared_node auf den reference_node.
                    for edge in compared_node.list_incoming_edges:
                        edge.target_node = reference_node

                    #   Die eingehenden Kanten des compared_node werden dem reference_node hinzugefügt
                    #   (Vorgehen des Zusammenfassens)
                    reference_node.list_incoming_edges = np.append(reference_node.list_incoming_edges,
                                                                  compared_node.list_incoming_edges)

                    #   Der Liste mit den Indizes, werden die Indizes der Ebene und des Knotens hinzugefügt, um
                    #   diesen Knoten später zu löschen. Wird nicht sofort gelöscht, damit die Indizes gültig
                    #   bleiben.
                    compared_node.list_incoming_edges = np.array([])
                    list_nodes_to_del += [[i, k]]

                    #   Da diese beiden Knoten zusammengefasst wurden, wird für die Quellknoten rekursiv getestet, ob
                    #   sie ebenfalls zusammengefasst werden können. Es können mehr als 2 Quellknoten sein. Davon
                    #   könnten zwei identisch sein und die Rekursion geht dort weiter. Beim 3. Knoten endet sie aber,
                    #   wenn er sich von dem zusammengefassten Knoten unterscheidet. Ist dieser auch identisch, kann er
                    #   genauso zusammengefasst werden.
                    new_list_of_indices = []
                    for edge in self.list_of_all_nodes[i][j].list_incoming_edges:

                        #   Index der nächsten Ebene (i ist die aktuelle Ebene)
                        new_i = i - 1
                        #   Index des Quellknotens in der Liste aller Knoten
                        new_j = self.list_of_all_nodes[new_i].index(edge.source_node)

                        #   Das Index-Paar wird der Liste hinzugefügt
                        new_list_of_indices += [[new_i, new_j]]

                    #   Rekursiver Funktionsaufruf mit der neuen Liste der Knoten: Es wird geprüft, ob den Pfad entlang
                    #   nach oben weitere Knoten zusammengefasst werden können.
                    self.merge_nodes_from_list(new_list_of_indices, list_nodes_to_del)

    """
    def leer(self):
        list_nodes_to_del = []

        for j, l in list_indices_of_nodes:
            operating_node = self.list_of_all_nodes[j][l]

            for k in range(j + 1, len(list_indices_of_nodes)):

                #   Runde den in den Knoten gespeicherten Wert des Knotens j und des Knotens k,
                #   die miteinander verglichen werden sollen
                round_sv_1 = round(operating_node.saved_value_on_node, 6)
                round_sv_2 = round(self.list_of_all_nodes[i][k].saved_value_on_node, 6)

                #   Runde den Real- und Imaginärteil der linken ausgehenden Kante beider Knoten (0-Kante)
                #   und bilde wieder eine komplexe Zahl
                round_ew_1 = (round(operating_node.list_outgoing_edges[0].edge_weight.real, 6)
                              + round(operating_node.list_outgoing_edges[0].edge_weight.imag, 6) * 1j)
                round_ew_2 = (round(self.list_of_all_nodes[i][k].list_outgoing_edges[0].edge_weight.real, 6)
                              + round(self.list_of_all_nodes[i][k].list_outgoing_edges[0].edge_weight.imag, 6) * 1j)

                #   Runde den Real- und Imaginärteil der rechten ausgehenden Kante beider Knoten (1-Kante)
                #   und bilde wieder eine komplexe Zahl
                round_ew_3 = (round(operating_node.list_outgoing_edges[1].edge_weight.real, 6)
                              + round(operating_node.list_outgoing_edges[1].edge_weight.imag, 6) * 1j)
                round_ew_4 = (round(self.list_of_all_nodes[i][k].list_outgoing_edges[1].edge_weight.real, 6)
                              + round(self.list_of_all_nodes[i][k].list_outgoing_edges[1].edge_weight.imag, 6) * 1j)

                #   Sind ausgehende Kanten und Wert in den Knoten identisch, kann der Knoten zusammengefasst werden
                if round_sv_1 == round_sv_2 and round_ew_1 == round_ew_2 and round_ew_3 == round_ew_4:

                    new_list_of_indices = []

                    #   Der Knoten j soll gelöscht werden, ändere den Zielknoten aller eingehenden Kanten
                    #   des Knoten j auf den Knoten k.
                    for edge in operating_node.list_incoming_edges:
                        edge.target_node = self.list_of_all_nodes[i][k]

                    for edge in self.list_of_all_nodes[i][k].list_incoming_edges:
                        index_l_new = self.list_of_all_nodes[i - 1].index(edge.source_node)
                        new_list_of_indices += [[i - 1, index_l_new]]

                    #   Die eingehenden Kanten des Knotens j werden dem Knoten k hinzugefügt
                    #   (Vorgehen des Zusammenfassens)
                    self.list_of_all_nodes[i][k].list_incoming_edges \
                        = np.append(self.list_of_all_nodes[i][k].list_incoming_edges,
                                    operating_node.list_incoming_edges)

                    #   Der Liste mit den Indizes werden die Indizes der Ebene und des Knotens gespeichert, um
                    #   diesen Knoten später zu löschen. Wird nicht sofort gelöscht, damit die Indizes gültig
                    #   bleiben.
                    operating_node.list_incoming_edges = np.array([])
                    list_nodes_to_del += [operating_node]

        #   Die Knoten an den in der Liste gespeicherten Indizes werden gelöscht
        for node in list_nodes_to_del:

            #   delete_node() verlangt, dass die eingehenden Kanten bereits umgeleitet wurden, dh. sie zeigen nicht
            #   mehr auf den Knoten, der gelöscht wird, oder die Liste muss leer sein.
            #   Da in der Schleife oben in der untersten Ebene angefangen wurde Knoten zusammenzufassen, sind alle
            #   Knoten die in der Liste der zu löschenden Knoten stehen, ohne eingehende Kanten, die auf den
            #   jeweiligen Knoten zeigen.
            node.delete_node()
            if Base.get_verbose() >= 3:
                print('Deleting node in step 7 - Merging nodes')"""

    def merge_dd_step7(self):
        """
        Funktion fasst Knoten im Entscheidungsdiagramm zusammen. Zuerst werden die Knoten der letzten Ebene in der Liste
        aller Knoten in einer Liste gespeichert, die dann der Funktion merge_nodes_from_list übergeben wird.
        Diese Funktion prüft die Knoten in der Liste mit ihren Pfaden auf gleichheit und wird rekursiv aufgerufen, um
        Knoten weiter oben auf dem selben Pfad zusammenzufassen. Hier wird deswegen nur die unterste Ebene verwendet.
        Danach werden hier die restlichen Knoten gelöscht.
        Zuvor müsssen die gewichteten Warhscheinlichkeiten an den Knoten berechnet worden sein (Schritt 6).
        :return:
        """

        #   Liste, in der die Indizes der Knoten gespeichert werden
        list_of_nodes = []
        #   Liste in der die Indizes der restlichen Knoten gespeichert werden, die nach dem Zusammenfassen gelöscht
        #   werden sollen
        list_nodes_to_del = []

        #   Berechne die Liste der Kante neu, die für jede Kante unterschiedliche Werte gepseichert hat, wenn sie nicht
        #   zusammengefasst werden können. Identische Äste haben die selben Werte in den Listen und können
        #   zusammengefasst werden
        self.list_of_all_edges[0].calc_unique_value()
        self.set_is_calculated_false()

        #   Speichere die Indizes der Knoten in der letzten Ebene in der Liste, die für die Funktion
        #   merge_nodes_from_list benötigt wird
        i = self.getnqubits() - 1
        for j in range(len(self.list_of_all_nodes[i])):
            list_of_nodes += [[i, j]]

        #   Führe die Zusammenfassung aus
        self.merge_nodes_from_list(list_of_nodes, list_nodes_to_del)

        #   Die Knoten, an den in der Liste gespeicherten Indizes, werden gelöscht. Dazu werden in einer neuen Liste
        #   anstatt der Indizes, die Knotenobjekte hinzugefügt.
        list_node_objects = []
        count = 0
        for i, j in list_nodes_to_del:
            list_node_objects += [self.list_of_all_nodes[i][j]]

        #   Die Knoten werden in der Liste aller Knoten gesucht und gelöscht, dadurch werden die zuver verwendetetn
        #   Indizes ungültig
        for node in list_node_objects:

            #   delete_node() verlangt, dass die eingehenden Kanten bereits umgeleitet wurden, dh. sie zeigen nicht
            #   mehr auf den Knoten, der gelöscht wird, oder die Liste muss leer sein.
            #   Da in der Schleife oben in der untersten Ebene angefangen wurde Knoten zusammenzufassen, sind alle
            #   Knoten die in der Liste der zu löschenden Knoten stehen, ohne eingehende Kanten, die auf den
            #   jeweiligen Knoten zeigen.
            for m, layer in enumerate(self.list_of_all_nodes):
                try:
                    n = layer.index(node)
                    self.list_of_all_nodes[m][n].delete_node()
                    count += 1
                    break

                #   Wurde der Knoten in dieser Ebene nicht gefunden, wird in der nächsten Ebene gesucht
                except ValueError:
                    continue

        #   Gebe die Anzahl der gelöschten Knoten aus
        if Base.get_verbose() >= 3:
            print('Deleting {a} node(s) in step 7 - Merging nodes'.format(a=count))

        #   Wird nicht mehr benötigt, da es mit einer neuen Funktion jetzt anders Funktioniert
        """
        #   Liste, in der die Indizes aller Knoten gespeichert werden, die anschließend gelöscht werden sollen
        list_nodes_to_del = []

        #   Fasse Knoten mit den selben gespeicherten Werten zusammen, wenn die ausgehenden Kanten die selben
        #   Kantengewichte haben. Dazu muss in der untersten Ebene begonnen werden.
        for i in range(Base.getnqubits() - 1, 0, -1):
            for j, operating_node in enumerate(self.list_of_all_nodes[i]):
                for k in range(j + 1, len(self.list_of_all_nodes[i])):

                    #   Runde den in den Knoten gespeicherten Wert des Knotens j und des Knotens k,
                    #   die miteinander verglichen werden sollen
                    round_sv_1 = round(operating_node.saved_value_on_node, 6)
                    round_sv_2 = round(self.list_of_all_nodes[i][k].saved_value_on_node, 6)

                    #   Runde den Real- und Imaginärteil der linken ausgehenden Kante beider Knoten (0-Kante)
                    #   und bilde wieder eine komplexe Zahl
                    round_ew_1 = (round(operating_node.list_outgoing_edges[0].unique_value.real, 6)
                                  + round(operating_node.list_outgoing_edges[0].unique_value.imag, 6) * 1j)
                    round_ew_2 = (round(self.list_of_all_nodes[i][k].list_outgoing_edges[0].unique_value.real, 6)
                                  + round(self.list_of_all_nodes[i][k].list_outgoing_edges[0].unique_value.imag, 6) * 1j)

                    #   Runde den Real- und Imaginärteil der rechten ausgehenden Kante beider Knoten (1-Kante)
                    #   und bilde wieder eine komplexe Zahl
                    round_ew_3 = (round(operating_node.list_outgoing_edges[1].unique_value.real, 6)
                                  + round(operating_node.list_outgoing_edges[1].unique_value.imag, 6) * 1j)
                    round_ew_4 = (round(self.list_of_all_nodes[i][k].list_outgoing_edges[1].unique_value.real, 6)
                                  + round(self.list_of_all_nodes[i][k].list_outgoing_edges[1].unique_value.imag, 6) * 1j)

                    #   Sind ausgehende Kanten und Wert in den Knoten identisch, kann der Knoten zusammengefasst werden
                    if round_sv_1 == round_sv_2 and round_ew_1 == round_ew_2 and round_ew_3 == round_ew_4:

                        #   Der Knoten k soll gelöscht werden, ändere den Zielknoten aller eingehenden Kanten
                        #   des Knoten k auf den Knoten j.
                        for edge in self.list_of_all_nodes[i][k].list_incoming_edges:
                            edge.target_node = operating_node

                        #   Die eingehenden Kanten des Knotens k werden dem Knoten j hinzugefügt
                        #   (Vorgehen des Zusammenfassens)
                        operating_node.list_incoming_edges \
                            = np.append(operating_node.list_incoming_edges,
                                        self.list_of_all_nodes[i][k].list_incoming_edges)

                        #   Der Liste mit den Indizes werden die Indizes der Ebene und des Knotens gespeichert, um
                        #   diesen Knoten später zu löschen. Wird nicht sofort gelöscht, damit die Indizes gültig
                        #   bleiben.
                        self.list_of_all_nodes[i][k].list_incoming_edges = np.array([])
                        list_nodes_to_del += [self.list_of_all_nodes[i][k]]

            #   Die Knoten an den in der Liste gespeicherten Indizes werden gelöscht
            for node in list_nodes_to_del:

                #   delete_node() verlangt, dass die eingehenden Kanten bereits umgeleitet wurden, dh. sie zeigen nicht
                #   mehr auf den Knoten, der gelöscht wird, oder die Liste muss leer sein.
                #   Da in der Schleife oben in der untersten Ebene angefangen wurde Knoten zusammenzufassen, sind alle
                #   Knoten die in der Liste der zu löschenden Knoten stehen, ohne eingehende Kanten, die auf den
                #   jeweiligen Knoten zeigen.
                node.delete_node()
                if Base.get_verbose() >= 3:
                    print('Deleting node in step 7 - Merging nodes')
            list_nodes_to_del = [] """

    def delete_edge_list_of_all_edges(self, edge_in):
        """
        Diese Funktion sucht eine Kante in der Liste aller Kanten und löscht sie daraus. Wird sie nicht gefunden,
        bricht das Programm mit einer Fehlermeldung ab.
        :param edge_in: Die Kante, die aus der Liste entfernt werden soll.
        :return:
        """

        #   Suche den Index, andem die Kante in der Liste aller Kanten gespeichert ist.
        #   numpy.where() funktioniert nicht, die Kante wird dann nicht gefunden
        #index_list_x = np.where(self.list_of_all_edges == edge_in)[0]
        #   Stattdessen wird die Liste aller Kanten (numpy) in einer normalen Liste gespeichert
        new_list = []
        for element in self.list_of_all_edges:
            new_list += [element]

        #   Finde den Index
        index_list_x = [new_list.index(edge_in)]

        #   Lösche diese Kante aus der Liste aller Kanten
        if np.size(index_list_x) == 1:
            self.list_of_all_edges = np.delete(self.list_of_all_edges, index_list_x[0])

        #   Die Kante wurde in der Liste nicht gefunden, sie hätte aber drin sein müssen.
        elif np.size(index_list_x) == 0:
            raise Exception('Error when deleting an edge in the decision diagram.\n'
                            'The List of all edges doesn\'t contain the edge', self,
                            ',\nbut it was expected. Error in the list_of_all_edges.')

        #   Die Kante ist doppelt, wenn sie mehfach vorkommt. Sollte auch nicht passieren.
        else:
            for i in index_list_x:
                self.list_of_all_edges = np.delete(self.list_of_all_edges, index_list_x[i])

            if Base.get_verbose():
                print('Error when deleting an edge in the decision diagram.\n'
                      'The edge to be deleted should occur only once in list_of_all_edges.\n')


def determine_nodes_on_level(dd_obj, n, matrix_in):
    """
    In jedem Knoten in der Liste list_of_nodes_per_level sind in saved_value_on_node die Matrizen gespeichert. Diese
    werden geteilt und die Teilmatrizen bilden die neue Ebene. Die Teilmatrizen werden auf Redundanzen überprüft und
    zusammengefasste Knoten erstellt, die in dd_obj unter list_of_nodes_per_level gespeichert sind.
    :param dd_obj: Objekt, indem auf den selben Adressen gearbeitet wird und neue Ergebnisse gespeichert werden
    (wie Pointer)
    :param n: Index der Ebene, auf dem der Knoten erstellt wird (zur Programm-Funktionsweise nicht benötigt)
    :param matrix_in: Matrix, die in Teilmatrizen geteilt werden soll
    :return:
    """

    #   Erstellen des Wurzelknotens mit Kante, Start des Entscheidunsdiagramms
    if n == 0:
        #   Erstelle die Wurzelkante mit einem Wurzelnkoten, indem die zu Beginn vorgegebene Matrix gespeichert ist.
        #   Leerer Knoten, der für die Kante benötigt wird:
        dd_obj.node_root = DDNode([], [], dd_obj)

        #   Die Kante hat nur einen Zielknoten, Quellknoten ist leer
        dd_obj.edge_root = DDEdge([], dd_obj.node_root, dd_obj)

        #   Die Kante wird dem neuen Knoten bei den eingehenden Kanten zugefügt
        dd_obj.node_root.list_incoming_edges = [dd_obj.edge_root]

        #   Liste der Kanten ist neu, sie besitzt nur ein Element.
        #   Der Knoten wird weiter unten in list_of_nodes_per_level
        #   gespeichert und dann außerhalb der Funktion, mit der gesamten Ebene, der Liste aller Knoten hinzugefügt.
        dd_obj.list_of_all_edges = np.array([dd_obj.edge_root])

        #   Speichere Matrix im Wurzelknoten, die im neuen Funktionsaufruf für n=1 geteilt wird und in
        #   zusammengefassten Knoten gespeichert wird
        dd_obj.node_root.saved_value_on_node = matrix_in

        #   Ebene 0 hat immer nur den Wurzelknoten gespeichert
        dd_obj.list_of_nodes_per_level = np.array([dd_obj.node_root])

        #   Erstelle 0-Endknoten, auf den alle Kanten verweisen, die irgendwo im Entscheidungsdiagramm auf eine
        #   0 Matrix/Vektor/Element führen
        dd_obj.node_zero = DDNode(np.array([]), np.array([]), dd_obj)

        #   0-Endknoten hat den Wert 0 gespeichert
        dd_obj.node_zero.saved_value_on_node = 0

        #   Füge den 0-Endknoten der Liste aller Knoten in der letzten Ebene hinzu
        dd_obj.list_of_all_nodes[Base.getnqubits()] = [dd_obj.node_zero]

    #   Regelablauf für Ebenen ab dem Wurzelknoten
    if n > 0:
        #   Für jeden Knoten einer Ebene wird die nächste Teilmatrix bestimmt und für jede einzigartige Teilmatrix auf
        #   der gesamten Ebene wird ein Knoten erstellt. Das sind zusammengefasste Knoten auf der nächsten Ebene.
        for source_node in dd_obj.list_of_nodes_per_level:

            #   Speichere den aktuellen Quellknoten um damit später Kanten zu erstellen
            DDNode.remember_node = source_node
            #   matrix_in speichert die Matrix die im Quellknoten gespeichert ist. Diese Matrix soll nun geteilt werden
            #   und auf redundanz geprüft werden (in shared_memory_for_equivalence_check soll es jede Teilmatrix genau
            #   einmal geben).
            matrix_in = source_node.saved_value_on_node

            #   Anzahl der Zeilen der Matrix/ des Vektors vor der Teilung
            m_in = np.shape(matrix_in)[0]
            #   Anzahl der Zeilen nach der Teilung
            m_out = int(m_in / 2)

            #   Falls Matrix:
            if not dd_obj.is_vector:
                #   Anzahl der Spalten vor und nach der Teilung
                n_in = np.shape(matrix_in)[1]
                n_out = int(n_in / 2)

                #   Speichern der 4 Teilmatrizen
                matrix_out_0 = matrix_in[0:m_out, 0:n_out]
                matrix_out_1 = matrix_in[m_out:m_in, 0:n_out]
                matrix_out_2 = matrix_in[0:m_out, n_out:n_in]
                matrix_out_3 = matrix_in[m_out:m_in, n_out:n_in]

                #   Funktion prüft ob Teilmatrix identisch mit einer Teilmatrix von einem Knoten der selben Ebene ist,
                #   und erstellt einen Knoten mit Kante, oder nur eine neue Kante
                create_node_if_new(dd_obj, matrix_out_0, n)
                create_node_if_new(dd_obj, matrix_out_1, n)
                create_node_if_new(dd_obj, matrix_out_2, n)
                create_node_if_new(dd_obj, matrix_out_3, n)

            #   Falls Vektor
            if dd_obj.is_vector:
                #   Speichern der 2 Teilvektoren
                matrix_out_0 = matrix_in[0:m_out]
                matrix_out_1 = matrix_in[m_out:m_in]

                #   Funktion prüft ob Teilmatrix identisch mit einer Teilmatrix von einem Knoten der selben Ebene ist,
                #   und erstellt einen Knoten mit Kante, oder nur eine neue Kante
                create_node_if_new(dd_obj, matrix_out_0, n)
                create_node_if_new(dd_obj, matrix_out_1, n)

        #   Alle Knoten einer Ebene wurden durchlaufen, für die nächste Ebene wird first_time wieder auf True gesetzt.
        #   Wird benötigt um beim ersten Knoten das numpyArray zu erstellen, bevor append genutzt werden kann
        dd_obj.first_time = True

        #   Die Knoten der nachsten Ebene werden nun in list_of_nodes_per_level gespeichert, falls vorhanden
        dd_obj.list_of_nodes_per_level = dd_obj.shared_memory_for_equivalence_check
        #   shared_memory_for_equivalence_check, wo jede Teilmatrix einer ganzen Ebene genau einmal gespeichert ist,
        #   wird geleert
        dd_obj.shared_memory_for_equivalence_check = np.array([])

        #   Die Endknoten der letzten Ebene sollen anstatt der ein-elementigen Matrix / Vektor den Wert dieses
        #   Eintrags in saved_value_on_node speichern
        #   Wird nur für die letzte Ebene ausgeführt
        if n == Base.getnqubits():
            for index, node in enumerate(dd_obj.list_of_nodes_per_level):

                # Falls Vektor gespeichert ist, wird anstatt [x] x gespeichert
                if np.shape(node.saved_value_on_node) == (1,):
                    dd_obj.list_of_nodes_per_level[index].saved_value_on_node = node.saved_value_on_node[0]

                #   Falls Matrix gespeichert ist, wird anstatt [[x]] x gespeichert
                elif np.shape(node.saved_value_on_node) == (1, 1):
                    dd_obj.list_of_nodes_per_level[index].saved_value_on_node = node.saved_value_on_node[0][0]
                else:
                    raise Exception('Error: In the last level of the decision diagram,\n'
                                    'the entries of the matrix/vector should be stored with [[x]] or [x]'
                                    ' in saved_value_on_node')

        #   Die in den Knoten gespeicherten Matrizen werden in der vorherigen Ebene gelöscht
        if n >= 1 and Base.get_verbose() == 0:
            for node in dd_obj.list_of_all_nodes[n - 1]:
                node.saved_value_on_node = None


def create_node_if_new(dd_obj, matrix_to_find, n):
    """
    Funktion um aus einer Matrix/Vektor jede einmalige Teilmatrizen zu suchen und daraus zusammengefasste Knoten zu
    erstellen. Ist die Teilmatrix neu, wird ein neuer Knoten erstellt, der die Teilmaatrix in saved_value_on_node
    gespeichert hat, und eine Kante zwischen diesem und dem gemerkten Quellknoten (DDNode.remember_node). Gibt es die
    Teilmatrix bereits, werden nur Kantenobjekte erstellt und der Liste des entsprechenden Knotens hinzugefügt.
    :param dd_obj: Objekt des Entscheidungsdiagramms, indem auf festen Adressen gearbeitet wird. Neue Werte werden
            direkt verändert (wie Pointer)
    :param matrix_to_find: Eingegebene Teilmatrix, die mit Teilmatrizen verglichen wird, die in schon gespeicherten
            Knoten sind
    :param n: Index der Ebene wird zur Berechnung der Anzahl der selben Kanten auf 0 benötigt.
    (geht von 0 bis n_qubits+1)
    :return:
    """

    #   Erstelle neuen und leeren Knoten, der an verschiedenen Stellen vervollständigt wird.
    new_node_obj = DDNode(np.array([]), np.array([]), dd_obj)

    #   Falls matrix_in eine 0-Matrix / ein 0-Vektor ist, gehen direkt alle Kanten auf 0
    if np.array_equal(matrix_to_find, np.zeros_like(matrix_to_find)):
        #   Neue Kante vom betrachteten Quellknoten bis zum 0-Endknoten
        new_edge = DDEdge(DDNode.remember_node, dd_obj.node_zero, dd_obj)

        #   Anzahl der möglichen Äste n im Entscheidungsdiagramm, ab Quellknoten mit matrix_in bis zum Endknoten, die
        #   durch matrix_in darstellen. Diese Anzahl wird nur für die Kanten auf den 0-Knoten benötigt: Sie gibt die
        #   Anzahl der Kanten auf 0 an, die durch diese eine Kante dargestellt werden.
        #   n_possible_paths_to_zero berechnet sich mit 2^(Anzahl der verbleibenden Ebenen) (Basis 2 oder 4, Vektor
        #   oder Matrix)
        #   n hat die Werte 0,1,2,3 bei 3 Qubits und bezeichnet die Ebene der Knoten. Es werden immer die eingehenden
        #   Kanten der Knoten betrachtet. Für die Wurzelkante (Ebene 0) ergenen sich dann 8 Möglichkeiten, bei 1: 4,
        #   bei 2: 2 und bei 3:1.
        new_edge.n_possible_paths_to_zero = int(pow(2 * np.ndim(matrix_to_find), Base.getnqubits() - n))

        #   Füge neue Kante der Liste aller Kanten hinzu
        dd_obj.list_of_all_edges = np.append(dd_obj.list_of_all_edges, [new_edge])

        #   Füge neue Kante der Liste des Elternknoten als ausgehende Kante hinzu
        DDNode.remember_node.list_outgoing_edges = np.append(DDNode.remember_node.list_outgoing_edges, [new_edge])

        #   Füge neue Kante der Liste des 0-Endknotens als eingehende Kante hinzu
        dd_obj.node_zero.list_incoming_edges = np.append(dd_obj.node_zero.list_incoming_edges, [new_edge])

        #   Überspringe die Teilung der Matrix, da Baum an der Stelle endet. In for-Schleife wird neuer Knoten
        #   der Ebene n betrachtet
        return 0

    #   Falls die Funktion create_node_if_new das erste Mal für die Ebene n aufgerufen wird: Erstelle für die aktuelle
    #   Teilmatrix (matrix_to_find) einen Knoten, eine neue Kante und speichere diese in den jeweiligen Listen.
    if dd_obj.first_time:

        #   Ablauf zum erstellen eines neuen Knotens mit Kante (Erster Knoten ohne append)
        # ---   New_node_obj gehört noch mit dazu! ( # ---: ähnliche Codeabschnitte)

        #   Erstelle Kante mit gespeicherten Knoten und neuem Knoten als Zielknoten (enthält die erste Teilmatrix)
        new_edge_obj = DDEdge(DDNode.remember_node, new_node_obj, dd_obj)

        #   Die erstellte Kante wird in dem neuen Knoten gespeichert
        new_node_obj.list_incoming_edges = [new_edge_obj]

        #   Speichern der Teilmatrix
        new_node_obj.saved_value_on_node = matrix_to_find

        #   Die neue Kante wird dem gespeicherten Quellknoten hinzugefügt
        DDNode.remember_node.list_outgoing_edges = np.append(DDNode.remember_node.list_outgoing_edges, [new_edge_obj],
                                                             0)

        #   Die neue Kante wird der Liste mit allen Kanten hinzugefügt
        dd_obj.list_of_all_edges = np.append(dd_obj.list_of_all_edges, [new_edge_obj], 0)

        #   Der neu erstellte Knoten wird in shared_memory_for_equivalence_check gespeichert, wo erneute
        #   Funktionsaufrufe der nächsten Teilmatrizen, aber auch die Teilmatrizen von anderen Quellvektoren der selben
        #   Ebene darauf zugreifen
        dd_obj.shared_memory_for_equivalence_check = np.array([new_node_obj])
        # ---

        dd_obj.first_time = False

    else:
        #   Prüfe für jedes Element in shared_memory_for_equivalence_check, ob gespeicherte Matrix identisch mit der zu
        #   suchenden ist
        matrix_exists = False
        for node_obj in dd_obj.shared_memory_for_equivalence_check:
            if np.array_equal(node_obj.saved_value_on_node, matrix_to_find):

                #   Falls Matrizen identisch sind wird ähnlich dem oberen ablauf, diesmal nur eine neue Kante zwischen
                #   gespeichertem Quellknoten und vorhandenen Zielknoten erstellt.
                # ---
                new_edge_obj = DDEdge(DDNode.remember_node, node_obj, dd_obj)
                node_obj.list_incoming_edges = np.append(node_obj.list_incoming_edges, [new_edge_obj], 0)

                #

                DDNode.remember_node.list_outgoing_edges = np.append(DDNode.remember_node.list_outgoing_edges,
                                                                     [new_edge_obj], 0)

                dd_obj.list_of_all_edges = np.append(dd_obj.list_of_all_edges, [new_edge_obj], 0)

                #

                # ---

                matrix_exists = True
                break

        if not matrix_exists:

            #   Falls die Matrix nicht existiert, wird ähnlich wie zu Beginn, ein neuer Knoten mit Kante erzeugt.
            #   Jetzt wird append() verwendet, um die Liste zu erweitern
            # ---
            new_edge_obj = DDEdge(DDNode.remember_node, new_node_obj, dd_obj)
            new_node_obj.list_incoming_edges = [new_edge_obj]

            new_node_obj.saved_value_on_node = matrix_to_find

            DDNode.remember_node.list_outgoing_edges = np.append(DDNode.remember_node.list_outgoing_edges,
                                                                 [new_edge_obj], 0)

            dd_obj.list_of_all_edges = np.append(dd_obj.list_of_all_edges, [new_edge_obj], 0)

            dd_obj.shared_memory_for_equivalence_check = np.append(dd_obj.shared_memory_for_equivalence_check,
                                                                   [new_node_obj], 0)
            # ---

    return 0
