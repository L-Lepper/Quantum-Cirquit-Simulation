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
