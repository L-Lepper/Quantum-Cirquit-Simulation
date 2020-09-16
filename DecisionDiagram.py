#   Projektarbeit Literaturrecherche zu Simulationsalgorithmen für Quantencomputing
#   Author: Lukas Lepper, 14.09.2020
#   Betreuer: Martin Hardieck
#   Dateiname: DDEdge.py
#   Version: 0.4


import numpy as np
from Base import Base
from DDNode import DDNode
from DDEdge import DDEdge


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
        #self.graph = []
        self.list_of_all_edges = np.array([])
        self.list_of_all_nodes = [[] for i in range(Base.getnqubits() + 1)]
        self.list_of_nodes_per_level = np.array([])
        self.node_root = None
        self.node_zero = None
        #   Wird später in Funktion benötigt, um pro Ebene den ersten Knoten zu erstellen
        self.first_time = True
        #   In dieser Liste werden alle Knoten einer Ebene zwischengespeichert, und auf Redundanz überprüft.
        self.shared_memory_for_equivalence_check = np.array([])

        self.create_dd(matrix_in)

        super().__init__()

    def create_dd(self, matrix_in):
        """
        Funktion baut Entscheidungsdiagramm aus Vektor oder Matrix auf. Knoten speichern Teilmatrizen in
        saved_value_on_node
        :param matrix_in: Matrix oder Vektor aus dem das Entscheidungsdiagramm erstellt wird
        :return:
        """

        #   Für jede Ebene werden die Knoten bestimmt, gleiche Knoten werden zusammengefasst und ihre Kanten in einer
        #   Liste zusammengeführt
        for level_index in range(Base.getnqubits() + 1):
            determine_nodes_on_level(self, level_index, matrix_in)

            #   Der 2-Dimensionalen Liste aller Knoten wird pro Zeile die Liste der Knoten pro Ebene angehängt
            self.list_of_all_nodes[level_index] += self.list_of_nodes_per_level.tolist()

            # ----------
            #   Ausgabe der Matrizen im vollständigen Diagramm, die momentan in den Knoten gespeichert sind, falls
            #   debug True. Ansprechen der Knoten über jede einzelne Kante
        if Base.get_debug():
            print(
                '\n\nTest des Aufbaus des Entscheidungsdiagramms. Die jeder Knoten hat 4 Nachfolgekanten, \n'
                'die Knoten werden durch die jeweiligen Matrizen dargestellt:\n')
            #   print root node
            print(self.list_of_all_edges[0])

            #   Ausgabe aller elementaren Knoten, durch die Matrix die dort gespeichert ist
            print('\n\n\nTest der Anzahl an verschiedenen Knoten. Redundante Knoten sind zusammengefasst:\n')
            #   print alle Knoten in der 2D Liste
            for zeile in self.list_of_all_nodes:
                for element in zeile:
                    print(element.saved_value_on_node)
            # ----------

        #   Von den Nachfolgeknoten wird der größte Wert auf den Elternknoten übertragen
        self.list_of_all_nodes[0][0].get_max_value_of_target_nodes()

            # ----------
            #   Ausgabe der übertragenen Werte
        if Base.get_debug():
            print('\n\n\nTest mit auf Elternknoten übertragenen Werten (Max aus Nachfolgeknoten):\n')
            #   print alle Knoten in der 2D Liste
            for zeile in self.list_of_all_nodes:
                for element in zeile:
                    print(element.saved_value_on_node)
            # ---------
            

        #   Kantengewicht
        #   ...


        #   In der letzten Ebene der Knoten wurden die Einträge der Matrix/Vektor gespeichert, die für die Funktion
        #   zuvor benötigt wurde. Damit das Diagramm später normiert ist, muss Endknoten entweder 0 oder 1 sein
        remember_edges = np.array([])
        for node in self.list_of_all_nodes[Base.getnqubits()][:]:
            if node.saved_value_on_node != 0:
                remember_edges = np.append(remember_edges, node.list_incoming_edges)
                self.list_of_all_nodes[Base.getnqubits()].remove(node)
        node_one = DDNode(remember_edges, np.array([]))
        node_one.saved_value_on_node = 1
        node_one.level = Base.getnqubits()
        self.list_of_all_nodes[Base.getnqubits()] += [node_one]

        # ----------
        #   Ausgabe der übertragenen Werte
        if Base.get_debug():
            print('\n\n\nTest mit auf Elternknoten übertragenen Werten (Max aus Nachfolgeknoten):\n')
            #   print alle Knoten in der 2D Liste
            for zeile in self.list_of_all_nodes:
                for element in zeile:
                    print(element.saved_value_on_node)
            # ---------



def determine_nodes_on_level(dd_obj, n, matrix_in):
    """
    In jedem Knoten in der Liste list_of_nodes_per_level sind in saved_value_on_node die Matrizen gespeichert. Diese
    werden geteilt und die Teilmatrizen bilden die neue Ebene. Die Teilmatrizen werden auf Redundanzen überprüft und
    zusammengefasste Knoten erstellt, die in dd_obj unter list_of_nodes_per_level gespeichert sind.
    :param dd_obj: Objekt, indem auf den selben Adressen gearbeitet wird und neue Ergebnisse gespeichert werden (wie Pointer)
    :param n: Index der Ebene, auf dem der Knoten erstellt wird (zur Programm-Funktionsweise nicht benötigt)
    :param matrix_in: Matrix, die in Teilmatrizen geteilt werden soll
    :return:
    """
    if n == 0:
        #   Erstelle die Wurzelkante mit einem Wurzelnkoten, indem die ausgangsmatrix gespeichert ist
        #   Leerer Knoten, der für die Kante benötigt wird
        dd_obj.node_root = DDNode([], [])
        #   Die Kante hat nur einen Zielknoten
        dd_obj.edge_root = DDEdge(None, dd_obj.node_root)
        dd_obj.node_root.list_incoming_edges = [dd_obj.edge_root]
        #   Index der Ebene auf dem sich der Knoten befindet. Wird für die Funktion des Programmes zurzeit nicht benötigt
        dd_obj.node_root.level = 0
        #   Liste der Kanten ist neu, sie besitzt nur ein Element. Der Knoten weiter unten in list_of_nodes_per_level
        #   gespeichert und wird erst auserhalb der Funktion mit der gesamten Ebene der Liste aller Knoten hinzugefügt
        dd_obj.list_of_all_edges = np.array([dd_obj.edge_root])

        #   Speichere Matrix in Knoten, die dann geteilt wird und wieder in zusammengefassten Knoten gespeichert wird
        dd_obj.node_root.saved_value_on_node = matrix_in
        #   Ebene 0 hat immer nur den Wurzelknoten
        dd_obj.list_of_nodes_per_level = np.array([dd_obj.node_root])

        #   Erstelle 0-Endknoten, auf den alle Kanten verweisen, die irgendwo im Entscheidungsdiagramm auf eine
        #   0 Matrix/Vektor/Element führen
        dd_obj.node_zero = DDNode(np.array([]), np.array([]))

        # Falls Vektor gespeichert ist [0], falls Matrix: [[0]]
        if np.ndim(matrix_in) == 1:
            dd_obj.node_zero.saved_value_on_node = [0]
        else:
            dd_obj.node_zero.saved_value_on_node = [[0]]

        dd_obj.node_zero.level = Base.getnqubits()
        dd_obj.list_of_all_nodes[Base.getnqubits()] = [dd_obj.node_zero]


    if n > 0:
        #   Für jeden Knoten einer Ebene wird die nächste Teilmatrix bestimmt und somit die zusammengefassten Knoten
        #   der nächsten Ebene
        for source_node in dd_obj.list_of_nodes_per_level:

            # Speichere den aktuellen Quellknoten um später Kanten zu erstellen
            DDNode.remember_node = source_node
            matrix_in = source_node.saved_value_on_node

            #   Falls matrix_in schon eine 0-Matrix / ein 0-Vektor ist, gehen direkt alle Kanten auf 0
            if np.array_equal(matrix_in, np.zeros_like(matrix_in)):
                #   Anzahl der Möglichkeiten x ab matrix_in im Entscheidungsdiagramm = Anzahl der Kanten auf den 0-Knoten
                #   x Berechnet sich mit der geometrischen Summenformel für i=1 bis i=n
                q = 2 * np.ndim(matrix_in)
                i = Base.getnqubits()
                # x = int((1 - pow(q, i)) / (1 - q))
                x = pow(2, Base.getnqubits() + 1 - n)
                for i in range(x):
                    new_edge = DDEdge(source_node, dd_obj.node_zero)
                    #   Füge neue Kante der Liste aller Kanten hinzu
                    dd_obj.list_of_all_edges = np.append(dd_obj.list_of_all_edges, [new_edge])
                    #   Füge neue Kante der Liste des Elternknoten als ausgehende Kante hinzu
                    source_node.list_outgoing_edges = np.append(source_node.list_outgoing_edges, [new_edge])
                    dd_obj.node_zero.list_incoming_edges = np.append(dd_obj.node_zero.list_incoming_edges, [new_edge])

                #   Überspringe die Teilung der Matrix, da Baum an der Stelle endet
                continue

            #   Anzahl der Zeilen der Matrix/ des Vektors
            m_in = np.shape(matrix_in)[0]
            #   Anzahl der Zeilen nach der Teilung
            m_out = int(m_in / 2)

            #   Falls Matrix:
            if np.ndim(matrix_in) == 2:
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
            elif np.ndim(matrix_in) == 1:
                #   Speichern der 2 Teilvektoren
                matrix_out_0 = matrix_in[0:m_out]
                matrix_out_1 = matrix_in[m_out:m_in]

                #   Funktion prüft ob Teilmatrix identisch mit einer Teilmatrix von einem Knoten der selben Ebene ist,
                #   und erstellt einen Knoten mit Kante, oder nur eine neue Kante
                create_node_if_new(dd_obj, matrix_out_0, n)
                create_node_if_new(dd_obj, matrix_out_1, n)

            else:
                print('Ungültige Matrix: Entweder Vektor oder Quadratische Matrix!')
                return -1

        #   Alle Knoten einer Ebene wurden durchlaufen, für die nächste Ebene wird first_time wieder auf True gesetzt.
        #   Wird benötigt um beim ersten Knoten das numpyArray zu erstellen, bevor append genutzt werden kann
        dd_obj.first_time = True

        #   Lösche node_zero, der bereits ganz zu Beginn der Liste aller Knoten hinzugefügt wurde, und daher nicht in
        #   list_of_nodes_per_level vorkommen darf, um Duplikat zu vermeiden, wenn list_of_nodes_per_level der Liste
        #   aller Knoten hinzugefügt wird
        if n == Base.getnqubits():
            dd_obj.list_of_all_nodes[n] = []

        #   Die Knoten der nachsten Ebene werden nun in list_of_nodes_per_level gespeichert, falls vorhanden
        dd_obj.list_of_nodes_per_level = dd_obj.shared_memory_for_equivalence_check
        #   shared_memory_for_equivalence_check, wo jede Teilmatrix genau einmal gespeichert ist, wird geleert
        dd_obj.shared_memory_for_equivalence_check = np.array([])

        #   Die Endknoten der letzten Ebene sollen anstatt der einelementigen Matrix / Vektor den Wert dieses
        #   Eintrags in saved_value_on_node speichern
        #   Wird nur für die letzte Ebene ausgeführt
        if n == Base.getnqubits():
            for index, node in enumerate(dd_obj.list_of_nodes_per_level):
                node.list_outgoing_edges = np.array([])

                # Falls Vektor gespeichert ist, wird anstatt [x] x gespeichert
                if np.shape(node.saved_value_on_node) == (1,):
                    dd_obj.list_of_nodes_per_level[index].saved_value_on_node = node.saved_value_on_node[0]

                #   Falls Matrix gespeichert ist, wird anstatt [[x]] x gespeichert
                elif np.shape(node.saved_value_on_node) == (1, 1):
                    dd_obj.list_of_nodes_per_level[index].saved_value_on_node = node.saved_value_on_node[0][0]
                else:
                    print(
                        'Fehler: In der Letzten Ebene des Entscheidungsdiagramms, sollten die Einträge der Matrix/Vektor'
                        ' mit [[x]], [x] in saved_value_on_node gespeichert sein')

        #   Die in den Knoten gespeicherten Matrizen werden in der vorherigen Ebene gelöscht
        if n >= 1 and not Base.get_debug():
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
    :param n: Index der Ebene, ist bisher nicht relevant, wird aber mit gespeichert
    :return:
    """

    #   Erstelle neuen und leeren Knoten, der an verschiedenen Stellen vervollständigt wird.
    new_node_obj = DDNode([], [])
    new_node_obj.level = n

    if n == Base.getnqubits() and dd_obj.first_time == True:
        #   Erstelle Kante mit gespeicherten Knoten und neuem Knoten als Zielknoten (enthält die erste Teilmatrix)
        #new_edge_obj = DDEdge(DDNode.remember_node, dd_obj.node_zero)
        #   Die erstellte Kante wird in dem neuen Knoten gespeichert
        #dd_obj.node_zero.list_incoming_edges = np.append(dd_obj.node_zero.list_incoming_edges, [new_edge_obj])
        dd_obj.shared_memory_for_equivalence_check = np.array([dd_obj.node_zero])
        dd_obj.first_time = False


    if dd_obj.first_time:
        #   Ablauf zum erstellen eines neuen Knotens mit Kante (Erster Knoten ohne append)
        #---   New_node_obj gehört noch mit dazu!

        #   Erstelle Kante mit gespeicherten Knoten und neuem Knoten als Zielknoten (enthält die erste Teilmatrix)
        new_edge_obj = DDEdge(DDNode.remember_node, new_node_obj)
        #   Die erstellte Kante wird in dem neuen Knoten gespeichert
        new_node_obj.list_incoming_edges = [new_edge_obj]

        #   Speichern der Teilmatrix
        new_node_obj.saved_value_on_node = matrix_to_find

        #   Die neue Kante wird dem gespeicherten Quellknoten hinzugefügt
        DDNode.remember_node.list_outgoing_edges = np.append(DDNode.remember_node.list_outgoing_edges, [new_edge_obj], 0)

        #   Die neue Kante wird der Liste mit allen Kanten hinzugefügt
        dd_obj.list_of_all_edges = np.append(dd_obj.list_of_all_edges, [new_edge_obj], 0)

        #   Der neu erstellte Knoten wird in shared_memory_for_equivalence_check gespeichert, wo erneute
        #   Funktionsaufrufe der nächsten Teilmatrizen, aber auch die Teilmatrizen von anderen Quellvektoren der selben
        #   Ebene darauf zugreifen
        dd_obj.shared_memory_for_equivalence_check = np.array([new_node_obj])
        #---

        dd_obj.first_time = False

    else:
        #   Prüfe für jedes Element in shared_memory_for_equivalence_check, ob gespeicherte Matrix identisch mit der zu
        #   suchenden ist
        matrix_exists = False
        for node_obj in dd_obj.shared_memory_for_equivalence_check:
            if np.array_equal(node_obj.saved_value_on_node, matrix_to_find):
                #   Falls Matrizen identisch sind wird ähnlich dem oberen ablauf, diesmal nur eine neue Kante zwischen
                #   gespeichertem Quellknoten und vorhandenen Zielknoten erstellt.
                #---
                new_edge_obj = DDEdge(DDNode.remember_node, node_obj)
                node_obj.list_incoming_edges = np.append(node_obj.list_incoming_edges, [new_edge_obj], 0)

                #

                DDNode.remember_node.list_outgoing_edges = np.append(DDNode.remember_node.list_outgoing_edges, [new_edge_obj], 0)

                dd_obj.list_of_all_edges = np.append(dd_obj.list_of_all_edges, [new_edge_obj], 0)

                #

                #---

                matrix_exists = True
                break

        if not matrix_exists:
            #   Falls die Matrix nicht existiert, wird ähnlich wie zu Beginn, ein neuer Knoten mit Kante erzeugt.
            #   Jetzt wird append() verwendet, um die Liste zu erweitern
            #---
            new_edge_obj = DDEdge(DDNode.remember_node, new_node_obj)
            new_node_obj.list_incoming_edges = [new_edge_obj]

            new_node_obj.saved_value_on_node = matrix_to_find

            DDNode.remember_node.list_outgoing_edges = np.append(DDNode.remember_node.list_outgoing_edges, [new_edge_obj], 0)

            dd_obj.list_of_all_edges = np.append(dd_obj.list_of_all_edges, [new_edge_obj], 0)

            dd_obj.shared_memory_for_equivalence_check = np.append(dd_obj.shared_memory_for_equivalence_check,
                                                                   [new_node_obj], 0)
            #---

    return 0
