#   Projektarbeit Literaturrecherche zu Simulationsalgorithmen für Quantencomputing
#   Author: Lukas Lepper, 14.09.2020
#   Betreuer: Martin Hardieck
#   Dateiname: DDEdge.py
#   Version: 0.4


from Base import Base


class DDNode(Base):
    """
    Klasse für die Knoten-Objekte. Jeder Knoten hat eine Liste mit allen eingehenden und allen ausgehenden Kanten.
    In saved_value_on_node können auf dem Knoten Zwischenergebnisse gespeichert werden.
    """

    #   remember_node wird bei der Überprüfung der Teilmatrizen beim Zusammenfassen der Knoten benötigt
    remember_node = None

    def __init__(self, list_incoming_edges, list_outgoing_edges):
        """
        :param list_incoming_edges: numpy liste mit Objekten der eingehenden Kanten
        :param list_outgoing_edges: numpy liste mit Objekten der ausgehenden Kanten
        """

        self.saved_value_on_node = 0
        self.list_incoming_edges = list_incoming_edges
        self.list_outgoing_edges = list_outgoing_edges
        self.is_calculated = False
        super().__init__()

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
            #   aus den Zielknoten hinzugefügt.
            if any(self.list_outgoing_edges):
                for edge in self.list_outgoing_edges:
                    temp += [edge.target_node.get_max_value_of_target_nodes()]

                #   Speichere den größten Wert aus der Liste temp im aktuellen Knoten
                self.saved_value_on_node = max(temp)
                #   Falls der kleinste Wert in temp betragsmäßig größer ist als der Maximalwert, wird der kleinste Wert
                #   gespeichert.
                if abs(min(temp)) > self.saved_value_on_node:
                    self.saved_value_on_node = min(temp)

                #   Gebe den gespeicherten Wert zurück
                return self.saved_value_on_node

            #   Falls der aktuelle Knoten ein Endknoten ist, wird der in ihm gespeicherte Wert zurückgegeben
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
