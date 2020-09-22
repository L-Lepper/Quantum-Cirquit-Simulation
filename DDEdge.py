#   Projektarbeit Literaturrecherche zu Simulationsalgorithmen für Quantencomputing
#   Author: Lukas Lepper, 14.09.2020
#   Betreuer: Martin Hardieck
#   Dateiname: DDEdge.py
#   Version: 0.4


from Base import Base


class DDEdge(Base):
    """
    Klasse für die Kantenobjekte. Jede Kante kennt ihren Ziel- und Quellknoten und hat ein Kantengewicht und eine
    Wahrscheinlichkeit. In count_calc ist die Anzahl gespeichert, wie oft die Kante in allen möglichen Ästen des
    Entscheidungsdiagramms vorkommt (bei mehreren eingehenden Kanten, wenn Knoten zusammengefasst wurden). Sie enthält
    die Memberfunktionen, die zb. das Kantengewicht für alle Kanten rekursiv berechnen.
    """

    def __init__(self, source_node, target_node):
        self.edge_weight = 1
        self.edge_probability = None
        self.source_node = source_node
        self.target_node = target_node
        #   is_calculated wird benötigt, damit durch die rekursiven Funktionsaufrufe jedes Objekt nur einmal berechnet
        #   wird
        self.is_calculated = False
        #   count_calc wird in der Funktion calc_edge_propability hochgezählt. Entspricht der Anzahl, wie oft die Kante
        #   in allen möglichen Ästen des Diagramms vorkommt.
        self.count_calc = 0
        super().__init__()

    def __str__(self):
        """
        Ausgabe des Entscheidungsdiagramms, wenn die Wurzelkante aufgerufen wird.
        :return:
        """

        print(self.target_node.saved_value_on_node)

        #   Ausgabestring, der für return benötigt wird
        str_out = ''

        if any(self.target_node.list_outgoing_edges):
            for element in self.target_node.list_outgoing_edges:
                str_out += (element.__str__())
            return str_out
        else:
            return str_out

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
            return
        else:
            #   In edge_probability wird das Produkt aus dem übergebenen Wert der vorherigen Kante und dem quadrierten
            #   Betrag des Kantengewichts der aktuellen Kante, gespeichert.
            self.edge_probability = pow(abs(self.edge_weight), 2) * upstream_value
            self.is_calculated = True

            #   Für jede ausgehende Kante des Zielknotens wird wieder dieses Produkt berechnet
            for edge in self.target_node.list_outgoing_edges:
                edge.calc_product_of_weights(self.edge_probability)

    def calc_edge_propability(self):
        """
        Die Funktion berechnet die Wahrscheinlichkeit der Kanten. Zuvor muss Schritt 7 in "instructions_for_decision_
        diagram.doocx" ausgeführt worden sein, damit in den Kanten und Knoten die benötigten Werte stehen.
        Die Funktion zählt in count_calc, wie oft die Kante in allen möglichen Ästen des Entscheidungsdiagramms
        vorkommt.
        ToDo: Dateiname überprüfen
        :return:
        """

        #   Der counter zählt wie oft die Funktion durch die zusammengefassten Knoten (mehrere eingehende Kanten)
        #   aufgerufen wird.
        self.count_calc += 1

        #   Zuerst wird für jede ausgehende Kante des Zielknotens die Funktion rekursiv aufgerufen, damit die
        #   Berechnung von count_calc funktioniert
        for edge in self.target_node.list_outgoing_edges:
            edge.calc_edge_propability()

        #   Falls Funktion schon durch einen anderen Ast aufgerufen wurde, muss Berechnung nicht nochmal durchgeführt
        #   werden
        if self.is_calculated:
            return
        else:
            #   Für die Wahrscheinlichkeit wird anschließend das Produkt aus dem Wert des Zielknotens mit dem
            #   Zwischenergebniss in der Kante berechnet.
            self.edge_probability *= self.target_node.saved_value_on_node
            self.is_calculated = True
