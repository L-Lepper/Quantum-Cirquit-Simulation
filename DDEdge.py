#   Projektarbeit Literaturrecherche zu Simulationsalgorithmen für Quantencomputing
#   Author: Lukas Lepper, 19.10.2020
#   Betreuer: Martin Hardieck
#   Dateiname: DDEdge.py
#   Version: 0.5


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
        """
        Es wird ein Objekt für die Kante erstellt.
        :param source_node: Quellknoten der Kante
        :param target_node: Zielknoten der Kante
        :param dd_obj_in: Objekt des Entscheidungsdiagramms, zudem diese Kante gehört.
        """

        #   Objekt des Entscheidungsdiagramms wird benötigt um auf Liste der Knoten und Kanten zuzugreifen.
        self.dd_obj = dd_obj_in
        self.edge_weight = 1
        self.edge_probability = 0
        self.old_edge_probability = 0
        self.conditional_probability = 0
        self.source_node = source_node
        self.target_node = target_node

        #   Speichert die Anzahl, wie viele Kanten auf den 0-Knoten durch diese Kante dargestellt werden.
        self.n_possible_paths_to_zero = 0
        #   Speichert die Anzahl, wie häufig diese Kante in allen möglichen Ästen vorkommt.
        self.count_of_paths = 0
        #   is_calculated wird benötigt, damit durch die rekursiven Funktionsaufrufe jedes Objekt nur einmal berechnet
        #   wird
        self.is_calculated = False

        super().__init__()


    def delete_edge(self, dd_obj):
        """
        Funktion löscht nachfolgende Kanten und Knoten, welche nicht mehr benötigt werden.
        :param dd_obj:
        :return:
        """

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
        """
        Die Funktion berechnet die bedingte Wahrscheinlichkeit, dass an einem Knoten die Entscheidung 0 oder 1, linke
        oder rechte Kante getroffen wird.
        :return:
        """

        #   Falls die Wahrscheinlichkeit bereits berechnet wurde, kann Funktion abgebrochen werden.
        if self.is_calculated:
            return

        #   Berechnung der bedingten Wahrscheinlichkeit, falls noch nicht getan
        else:
            #   Falls die Kante einen Quellknoten hat, wird Kantenwahrscheinlichkeit der aktuellen Kante durch die
            #   Summe der Kantenwahrscheinlichkeiten der eingehenden Kanten des Quellknotens geteilt.
            if self.source_node:
                sum_incoming_ep = 0

                #   Summe der Wahrscheinlichkeiten der eingehenden Kanten
                for edge in self.source_node.list_incoming_edges:
                    sum_incoming_ep += edge.edge_probability

                #   Berechnung der bedingten Wahrscheinlichkeit durch division der Kantenwahrscheinlichkeit durch die
                #   Summe der eingehenden Kanten
                self.conditional_probability = self.edge_probability / sum_incoming_ep

            #   Falls die Kante keinen Quellknoten hat, entspricht die bedigte Wahrscheinlichkeit der
            #   Kantenwahrscheinlichkeit (Wurzelknoten mit P=1)
            else:
                self.conditional_probability = self.edge_probability / 1

            #   Falls der Zielknoten ausgehende Kanten hat, wird die Funktion für diese Kanten rekursiv aufgerufen
            if any(self.target_node.list_outgoing_edges):
                for edge in self.target_node.list_outgoing_edges:
                    edge.calc_conditional_probabilities()

            #   Merke, dass diese Kante berechnet wurde
            self.is_calculated = True

    def calc_count_of_paths(self):
        """
        Diese Funktion berechnet die Anzahl, wie oft eine Kante in allen Möglichen Ästen vorkommt.
        :return:
        """

        #   Falls die Anzahl noch nicht berechnet wurde, entspricht sie der Anzahl der Kanten auf den 0-Knoten, die
        #   durch die betrachtete Kante dargestellt werden. (Ist bei Kanten die nicht auf den 0-Knoten zeigen 0)
        if not self.is_calculated:
            self.count_of_paths = self.n_possible_paths_to_zero
            self.is_calculated = True

        else:
            #   Zähle Anzahl für jeden Funktionsaufruf hoch
            self.count_of_paths += 1

        #   Falls der Zielknoten ausgehende Kanten hat, wird die Funktion rekursiv für diese Kanten aufgerufen
        if any(self.target_node.list_outgoing_edges):
            for edge in self.target_node.list_outgoing_edges:
                edge.calc_count_of_paths()
