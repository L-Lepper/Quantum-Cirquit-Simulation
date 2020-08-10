import numpy as np
import cmath
from QuantumSimulation import QuantumSim


class QGate(QuantumSim):
    """Klasse für Quantengatter: Objekt enthält Informationen zu Gatterart (Typ) und Matrix U"""

    #   Default-Konstruktor: Zuweisung der Matrizen für X und Z Gatter
    def __init__(self, gate_in):
        """Definition des Quantengatters durch Matrixzuweisung"""

        #   Pauli-X (Not)
        if gate_in == 'x':
            self.type = 'x'
            self.u_matrix = np.array([[0, 1], [1, 0]], dtype=complex)
        #   Pauli-Z
        elif gate_in == 'z':
            self.type = 'z'
            self.u_matrix = np.array([[1, 0], [0, -1]], dtype=complex)
        #   Hadarmard
        elif gate_in == 'h':
            self.type = 'h'
            self.u_matrix = np.array([[1/cmath.sqrt(2), 1/cmath.sqrt(2)], [1/cmath.sqrt(2), -1/cmath.sqrt(2)]], dtype=complex)

        super().__init__()


    def __mul__(self, qstate_obj):
        """Operator * führt Matrix-Vektor-Multiplikation durch"""

        #   Matrix-Vektor-Produkt ergibt neuen Zustandsvektor
        qstate_obj.phi_vec = np.matmul(self.u_matrix, np.transpose(qstate_obj.phi_vec), )

        return self
