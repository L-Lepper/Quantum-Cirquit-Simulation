#   Projektarbeit Literaturrecherche zu Simulationsalgorithmen für Quantencomputing
#   Author: Lukas Lepper, 24.11.2020
#   Betreuer: Martin Hardieck
#   Dateiname: DDEdge.py
#   Version: 0.6


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

        self.edge_weight = 1
        self.edge_probability = 0
        self.old_edge_probability = 1
        self.conditional_probability = 0

        #   Wird benötigt, um identische Äste bei den Knoten zusammenzufassen.
        self.unique_value = [0, 0]
        self.source_node = source_node
        self.target_node = target_node

        #   Objekt des Entscheidungsdiagramms wird benötigt um auf Liste der Knoten und Kanten zuzugreifen.
        #   Wird auch zum löschen benötigt (in dd-obj sind die Listen gespeichert)
        self.dd_obj = dd_obj_in

        #   Speichert die Anzahl, wie viele Kanten auf den 0-Knoten durch diese Kante dargestellt werden.
        self.n_possible_paths_to_zero = 0
        #   Speichert die Anzahl, wie häufig diese Kante in allen möglichen Ästen vorkommt.
        self.count_of_paths = 1
        #   is_calculated wird benötigt, damit durch die rekursiven Funktionsaufrufe jedes Objekt nur einmal berechnet
        #   wird
        self.is_calculated = False

        super().__init__()

    def __str__(self):
        return self.print_recursive('')

    def print_upstream(self, str_in):
        """
        Die Funktion wird anstatt __str__ verwendet, damit sie besser rekursiv aufgerufen werden kann. Zusammen mit der
        print-Funktion in DDNOde, wird für jede neue Ebene, die ausgabe weiter eingerückt, sodass die Baumstrucktur
        besser erkennbar wird. Das ist bei einer höheren Anzahl nicht mehr so übersichtlich!
        :param str_in: Diesem Parameter wird durch den Nachfolgeknoten für jede Ebene ein Tabulator hinzugefügt.
            Dadurch kann die Ausgabe-Zeile einer Kante richtig eingerückt werden.
        :return:
        """

        str_out = ''
        if self.source_node:
            str_out = str_in + \
                      str(self.edge_weight) + ' ' + \
                      str(self.source_node.saved_value_on_node) + '\n' + \
                      self.source_node.print_recursive(str_in)
        else:
            str_out = str_in + \
                      str(self.edge_weight) + ' ' + '\n'
        return str_out

    def print_recursive(self, str_in):
        """
        Die Funktion wird anstatt __str__ verwendet, damit sie besser rekursiv aufgerufen werden kann. Zusammen mit der
        print-Funktion in DDNOde, wird für jede neue Ebene, die ausgabe weiter eingerückt, sodass die Baumstrucktur
        besser erkennbar wird. Das ist bei einer höheren Anzahl nicht mehr so übersichtlich!
        :param str_in: Diesem Parameter wird durch den Nachfolgeknoten für jede Ebene ein Tabulator hinzugefügt.
            Dadurch kann die Ausgabe-Zeile einer Kante richtig eingerückt werden.
        :return:
        """

        str_out = str_in + \
                  str(self.edge_weight) + ' ' + \
                  str(self.target_node.saved_value_on_node) + '\n' + \
                  self.target_node.print_recursive(str_in)
        return str_out

    def delete_edge(self):
        """
        Funktion löscht nachfolgende Kanten und Knoten, welche nicht mehr benötigt werden.
        :return:
        """

        #   Falls die Liste des Zielknotens nur eine eingehende Kante hat und er nicht der 0-Knoten ist, wird der
        #   Knoten gelöscht.
        if np.size(self.target_node.list_incoming_edges) == 1 and self.target_node.saved_value_on_node != 0:
            self.target_node.list_incoming_edges = np.array([])
            self.target_node.delete_node()

        #   Andernfalls wird nur diese Kante, die gelöscht werden soll, aus der Liste der eingehenden Kanten entfernt
        #   und gelöscht
        else:

            #   Lösche diese Kante in der Liste der eingehenden Kanten des Zielknotens
            self.target_node.delete_edge_in_incoming_list(self)

        #   Suche nun die zu löschende Kante in der Liste aller Kanten, um sie auch dort zu löschen.
        self.dd_obj.delete_edge_list_of_all_edges(self)

    def calc_edge_weight(self):
        """
        Funktion berechnet das Kantengewicht der einzelnen Kanten. Zuvor muss Schritt 3 in
        "Anleitung - Entscheidungsdiagramm und Messung - v4.pdf" ausgeführt worden sein, damit in den Knoten in
        saved_value_on_node die benötigten Werte stehen.
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
        zur Wurzelkante. Zuvor muss Schritt 6 in "Anleitung - Entscheidungsdiagramm und Messung - v4.pdf" ausgeführt
        worden sein, damit in den Knoten in saved_value_on_node die benötigten Werte stehen.
        Außerdem muss die Anzahl count_of_paths bereits berechnet worden sein.
        ToDo: Dateiname überprüfen
        :param upstream_value: Bei Funktionsaufruf der Wurzelkante muss diesem Parameter 1 übergeben werden. Jede Kante
        ruft diese Funktion rekursiv für Nachfolgekanten auf, diese Verwenden den berechneten Wert aus der Elternkante.
        :return:
        """

        #   Falls Funktion noch nicht berechnet wurde, wird die Wahrscheinlichkeit auf 0 zurückgesetzt
        #   (Falls das Diagramm später neu berechnet wird und der Ausgangswert nicht 0 ist):
        if not self.is_calculated:
            self.edge_probability = 0
            self.is_calculated = True

        #   In old_edge_probability wird das Produkt aus dem übergebenen Wert der vorherigen Kante und dem quadrierten
        #   Betrag des Kantengewichts der aktuellen Kante gespeichert. Dieser Wert wird an die nachfolgenden Kanten
        #   übergeben. Somit wird im Falle mehrerer eingehenden Kanten bei jedem Aufruf die Wahrscheinlichkeit durch den
        #   neuen Ast, der nachfolgenden Kantenwahrscheinlichkeiten hinzuaddiert.
        self.old_edge_probability = pow(abs(self.edge_weight), 2) * upstream_value

        #   Die neue Kantenwahrscheinlichkeit des aktuellen Funktionsaufrufs wird dem bisherigen Wert hinzuaddiert
        self.edge_probability += self.old_edge_probability

        #   Für jede ausgehende Kante des Zielknotens wird wieder dieses Produkt berechnet
        for edge in self.target_node.list_outgoing_edges:
            edge.calc_product_of_weights(self.old_edge_probability)

    def calc_edge_propability(self):
        """
        Die Funktion berechnet die Wahrscheinlichkeit der Kanten. Zuvor muss Schritt 7 in
        "Anleitung - Entscheidungsdiagramm und Messung - v4.pdf" ausgeführt worden sein, damit in den Kanten und Knoten die benötigten Werte stehen.
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

        #   Falls die Anzahl noch nicht berechnet wurde, wird sie auf 1 gesetzt. So kann die Anzahl auch noch mal neu
        #   berechnet werden.
        if not self.is_calculated:
            self.count_of_paths = 1
            self.is_calculated = True

        else:
            #   Zähle Anzahl für jeden Funktionsaufruf hoch
            self.count_of_paths += 1

        #   Falls der Zielknoten ausgehende Kanten hat, wird die Funktion rekursiv für diese Kanten aufgerufen
        if any(self.target_node.list_outgoing_edges):

            for edge in self.target_node.list_outgoing_edges:
                edge.calc_count_of_paths()

    def calc_unique_value(self):
        """
        Diese Funktion berechnet für eine Kante eine Liste mit einem bestimmten Wert für jede ausgehende Kante des Ziel-
        Knotens. Dadurch sollen beim Zusammenfassen von Knoten identische Äste erkannt werden. Die getrennte Information
        über den Linken oder rechten Ast ist notwendig, um Äste zu unterscheiden bei denen das Kantengewicht rechts und
        links einfach nur vertauscht ist, und der Wert saved_value im Knoten dadurch auch identisch ist. Dieser Wert
        kann alleine nicht verwendet werden, um gleiche Äste/Knoten zu erkennen.
        Da Äste nur zusammengefasst werden können, die in der untersten Ebene schon gleich sind, sollten mit diesem Wert
        gleiche Äste richtig erkannt werden können. unique_value enthält nur Infomationen zu der nächst unteren Ebene
        und nicht immer über den gesammten Ast (Beispiel: Wenn in 2 Ebenen weiter unten Kantengewichte vertauscht
        werden, ist oben dieser Wert trotzdem gleich)
        ToDo: falls notwendig, muss dieser Wert noch anders berechnet werden
        :return: unique_value der aktuellen Kante
        """

        #   Der Wert wird nur einmal berechnet, wenn Funktion für ein Objekt mehrmals aufgerufen wird
        if not self.is_calculated:
            self.unique_value = [1, 1]

            #   Falls es ausgehende Kanten am Zielknoten gibt, wird der unique_value einer ausgehenden Kante zusammen
            #   addiert und mit dem Wert der jeweiligen Seite i multipliziert (eine Seite der Liste für jede ausgehende
            #   Kante des Zielknotens der aktuellen Kante)
            if any(self.target_node.list_outgoing_edges):
                for i, edge in enumerate(self.target_node.list_outgoing_edges):

                    #   Speichern der zwei Werte in der Liste unique_value der aktuellen ausgehenden Kante
                    value_l, value_r = edge.calc_unique_value()

                    #   Multiplikation der Addition beider Werte mit dem aktuellen Kantengewicht
                    self.unique_value[i] *= (value_l + value_r) * self.edge_weight

            #   Falls der Zielknoten keine ausgehenden Kanten hat, wird in der Liste einfach das aktuelle Kantengewicht
            #   gespeichert
            else:
                self.unique_value = [self.edge_weight, self.edge_weight]

            #   Es wird sich gemerkt, dass diese Kante schon berechnet wurde
            self.is_calculated = True

        #   Die Funktion gibt die berechnete Liste zurück
        return self.unique_value
