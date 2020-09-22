#   Projektarbeit Literaturrecherche zu Simulationsalgorithmen für Quantencomputing
#   Author: Lukas Lepper, 14.09.2020
#   Betreuer: Martin Hardieck
#   Dateiname: DDEdge.py
#   Version: 0.4


from Base import Base


class DDEdge(Base):

    def __init__(self, source_node, target_node):
        self.edge_weight = 1
        self.edge_probability = None
        self.source_node = source_node
        self.target_node = target_node
        self.is_calculated = False
        self.count_calc = 0
        super().__init__()

    def __str__(self):
        print(self.target_node.saved_value_on_node)

        str_out = ''

        if any(self.target_node.list_outgoing_edges):
            for element in self.target_node.list_outgoing_edges:
                str_out += (element.__str__())
            return str_out
        else:
            return str_out

    def calc_edge_weight(self):
        if self.is_calculated:
            return
        else:
            if self.source_node:
                if self.source_node.saved_value_on_node == 0:
                    self.edge_weight = 0
                else:
                    self.edge_weight = self.target_node.saved_value_on_node / self.source_node.saved_value_on_node
            else:
                self.edge_weight = self.target_node.saved_value_on_node
            self.is_calculated = True

            for edge in self.target_node.list_outgoing_edges:
                edge.calc_edge_weight()

    def calc_product_of_weights(self, upstream_value):
        if self.is_calculated:
            return
        else:
            self.edge_probability = pow(abs(self.edge_weight), 2) * upstream_value
            self.is_calculated = True

            for edge in self.target_node.list_outgoing_edges:
                edge.calc_product_of_weights(self.edge_probability)

    def calc_edge_propability(self):
        self.count_calc += 1
        for edge in self.target_node.list_outgoing_edges:
            edge.calc_edge_propability()

        if self.is_calculated:
            return
        else:
            self.edge_probability *= self.target_node.saved_value_on_node
            self.is_calculated = True
