#   Projektarbeit Literaturrecherche zu Simulationsalgorithmen für Quantencomputing
#   Author: Lukas Lepper, 14.09.2020
#   Betreuer: Martin Hardieck
#   Dateiname: DDEdge.py
#   Version: 0.4


from Base import Base


class DDNode(Base):
    remember_node = None
    def __init__(self, list_incoming_edges, list_outgoing_edges):
        self.saved_value_on_node = 0
        self.level = None
        self.list_incoming_edges = list_incoming_edges
        self.list_outgoing_edges = list_outgoing_edges
        super().__init__()
