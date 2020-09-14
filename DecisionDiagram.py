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
        self.list_of_all_nodes = np.array([])
        self.list_of_nodes_per_level = np.array([])
        #   Wird später in Funktion benötigt, um pro Ebene den ersten Knoten zu erstellen
        self.first_time = True
        #   In dieser Liste werden alle Knoten einer Ebene zwischengespeichert, und auf Redundanz überprüft.
        self.shared_memory_for_equivalence_check = None

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
        for level_index in range(Base.getnqubits()):
        #for level_index in range(0, 3):
            determine_nodes_on_level(self, level_index, matrix_in)
            #   Der Liste aller Knoten wird die Liste der Knoten pro Ebene angehängt ToDO: 2 Dimensionale Liste mit Ebenen
            self.list_of_all_nodes = np.append(self.list_of_all_nodes, self.list_of_nodes_per_level, 0)


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
        #   Beide Listen sind neu, besitzen nur ein Element
        dd_obj.list_of_all_nodes = np.array([dd_obj.node_root])
        dd_obj.list_of_all_edges = np.array([dd_obj.edge_root])

        #   Speichere Matrix in Knoten, die dann geteilt wird und wieder in zusammengefassten Knoten gespeichert wird
        dd_obj.node_root.saved_value_on_node = matrix_in
        #   Ebene 0 hat immer nur den Wurzelknoten
        dd_obj.list_of_nodes_per_level = [dd_obj.node_root]

    if n >= 0:
        #   Für jeden Knoten einer Ebene wird die nächste Teilmatrix bestimmt und somit die zusammengefassten Knoten
        #   der nächsten Ebene
        for source_node in dd_obj.list_of_nodes_per_level:

            # Speichere den aktuellen Quellknoten um später Kanten zu erstellen
            DDNode.remember_node = source_node
            matrix_in = source_node.saved_value_on_node

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
                matrix_out_1 = matrix_in[0:m_out, n_out:n_in]
                matrix_out_2 = matrix_in[m_out:m_in, 0:n_out]
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
        #   Die Knoten der nachsten Ebene werden nun in list_of_nodes_per_level gespeichert
        dd_obj.list_of_nodes_per_level = dd_obj.shared_memory_for_equivalence_check
        #   shared_memory_for_equivalence_check, wo jede Teilmatrix genau einmal gespeichert ist, wird geleert
        dd_obj.shared_memory_for_equivalence_check = []


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

    if dd_obj.first_time:
        #   Ablauf zum erstellen eines neuen Knotens mit Kante (Erster Knoten ohne append)
        #---   New_node_obj gehört noch mit dazu!

        #   Erstelle Kante mit gesoeicherten Knoten und neuem Knoten als Zielknoten (enthält die erste Teilmatrix)
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
