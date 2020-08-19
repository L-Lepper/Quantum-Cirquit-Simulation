#   Projektarbeit Literaturrecherge zu Simulationsalgorithmen für Quantencomputing
#   Author: Lukas Lepper, 19.08.2020
#   Betreuer: Martin Hardieck
#   Dateiname: QuantumSimulation.py
#   Version: 0.2

class QuantumSim:

    #   Private Attribute: Zugriff über Funktion / Klassenmethode.
    __nqubits = 0
    __qubitToChange = 0

    def __init__(self):
        self.__nqubits = 0
        self.__qubitToChange = 0

        # if isinstance(object_in, QGate):
        #    self.u_matrix = object_in.u_matrix
        # elif isinstance(object_in, QState):
        #    self.phi_vec = object_in.phi_vec

        # self.np_array_for_sim = np.array

    #   get Anzahl der Qubits
    @staticmethod
    def getnqubits():
        return QuantumSim.__nqubits

    #   set Anzahl der Qubits
    @staticmethod
    def setnqubits(n_qubits):
        QuantumSim.__nqubits = n_qubits

    #   get Index des Qubits, auf welches das Gatter angewendet wird
    @staticmethod
    def getqubittochange():
        return QuantumSim.__qubitToChange

    #   set Index des Qubits, auf welches das Gatter angewendet wird
    @staticmethod
    def setqubittochange(qubittochange):
        QuantumSim.__qubitToChange = qubittochange
