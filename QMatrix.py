#   Projektarbeit "Recherche und Tool zur Simulation von Quantenschaltungen im Bereich Quantencomputing"
#   Author: Lukas Lepper, 25.08.2020
#   Betreuer: Dipl.-Ing. Martin Hardieck
#   Dateiname: QMatrix.py
#   Version: 0.3


import numpy as np
from Base import Base


class QMatrix(Base):
    """
    Elternklasse für Zustandsvektor und Gatter. Sie stellt eine allgemeine Matrix zur Verfügung, die als Zustandsvektor
    oder Matrix für ein Gatter verwendet werden kann.
    """

    def __init__(self):
        """
        Variable für die allgemeine Matrix wird angelegt. Ihr Datentyp wird hier noch nicht festgelegt,
        könnte aber gemacht werden. Hier wird dann ein Numpy Array verwendet.
        """

        self.general_matrix = np.array([])
        super().__init__()

    def __mul__(self, qstate_obj):
        """
        Operator * führt Matrix-Vektor-Multiplikation zwischen QGate und QState durch."
        Für die Messung wird dieser Operator in der Klasse Measurement überladen.

        :param qstate_obj: Zustandsvektor, mit dem Multipliziert wird
        :return qstate_obj: Gibt veränderten Zustandsvektor zurück
        """

        #   Matrix-Vektor-Produkt ergibt neuen Zustandsvektor
        qstate_obj.general_matrix = np.matmul(self.general_matrix, np.transpose(qstate_obj.general_matrix))

        return qstate_obj
