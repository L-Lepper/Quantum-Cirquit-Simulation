#   Projektarbeit Literaturrecherche zu Simulationsalgorithmen für Quantencomputing
#   Author: Lukas Lepper, 25.08.2020
#   Betreuer: Martin Hardieck
#   Dateiname: QState.py
#   Version: 0.3


import numpy as np
from QMatrix import QMatrix


class QState(QMatrix):
    """
    Klasse für Quantenzustandsvektoren: enthält verschedene Darstellungen und überladenen Operator für
    Matrix-Vektor-Produkt
    """

    #   Default-Konstruktor
    def __init__(self):  # phi_in
        super().__init__()

    #   Über print(qstate_object) werden alle möglichen Zustände und Wahrscheinlichkeiten ausgegeben
    def __str__(self):
        """
        Ausgabe alle möglichen Zustände und zugehörigen Wahrscheinlichkeiten im Ausgabestring.
        ( print(QState-Obj) möglich)

        :return return_str: Ausgabestring
        """

        return_str = ''
        index = 0

        #   Ausgabe für jeden einzelnen Wert ungleich 0, im Zustandsvektor
        for value in self.general_matrix:

            if value != 0. + 0.j:
                #   Umwandlung des Indexes in ein Bitmuster (3 --> 0011)
                diracnotation = self.getdiracnotation(index, self.getnqubits())
                #   Berechnung der Wahrscheinlichkeit in %
                probability = round(pow(abs(value), 2) * 100, 13)

                return_str += 'Der Zustand {} hat die Wahrscheinlichkeit von {}%.\n'.format(diracnotation, probability)

            index += 1

        return return_str

    @staticmethod
    def getdiracnotation(index, n_qubits):
        """
        Funktion wandelt einen Zustand in Diracnotation um ( |001) ). Benötigt die Anzahl der Qubits für führende
        Nullen.

        :param index: Index des Zustandes im Vektor
        :param n_qubits: Anzahl der Qubits
        :return diracnotation: In Diracnotation |100)
        """

        #   Umwandlung von int in binärcode, Abschneiden der Information des Vorzeichenbits ( 0b / 1b )
        str_var = bin(index)[2:]

        diracnotation = '|' + (n_qubits - len(str_var)) * '0' + str_var + ')'

        return diracnotation

    def init_vec_with_bitsequence(self, int_in):
        """
        Initialisiert den Zustandsvektor aus dieser Klasse mit einem Basiszustand. general_matrix ist hier ein Vektor.
        Das Bitmuster des Basiszustandes kann als binäre Zahl in int umgewandelt werden, und wieder zurück. Vorgehen
        ist effizienter als die Verwendung einse String. Integer Zahl entspricht dann dem Index im Zustandsvektor,
        beginnend bei 0. Dadurch leichtere Vektorzuordnung.

        :param int_in: Index des Basiszustandes im Zustandsvektor
        :return: Verändert general_matrix im eigenen Objekt
        """

        #   Leeren Zustandsvektor erstellen
        self.general_matrix = np.zeros(pow(2, self.getnqubits()), dtype=complex)

        #   Bitmuster beschreibt einen Basiszustand: Nur der Eintrag des Index ist 1 (entspricht dem Zustand der
        #   durch das Bimuster dargestellt ist). Die restlichen Komponenten sind 0.
        self.general_matrix[int_in] = 1 + 0j

        return self
