
class QuantumSim:

    __nqubits = 0

    def __init__(self):
        self.__nqubits = 0

        # if isinstance(object_in, QGate):
        #    self.u_matrix = object_in.u_matrix
        # elif isinstance(object_in, QState):
        #    self.phi_vec = object_in.phi_vec

        # self.np_array_for_sim = np.array

    @staticmethod
    def getnqubits():
        return QuantumSim.__nqubits

    @staticmethod
    def setnqubits(n_qubits):
        QuantumSim.__nqubits = n_qubits
