#   Projektarbeit Literaturrecherche zu Simulationsalgorithmen für Quantencomputing
#   Author: Lukas Lepper, 24.11.2020
#   Betreuer: Martin Hardieck
#   Dateiname: QState.py
#   Version: 0.6


import numpy as np
from Base import Base
from QMatrix import QMatrix


class QState(QMatrix):
    """
    Klasse für Quantenzustandsvektoren: enthält verschedene Darstellungen und überladenen Operator für
    Matrix-Vektor-Produkt
    """

    #   Default-Konstruktor
    def __init__(self):
        super().__init__()

    #   Über print(qstate_object) werden alle möglichen Zustände und Wahrscheinlichkeiten ausgegeben
    def __str__(self):
        """
        Ausgabe alle möglichen Zustände und zugehörigen Wahrscheinlichkeiten im Ausgabestring.
        ( print(QState-Obj) möglich)

        :return return_str: Ausgabestring
        """

        return_str = ''
        return_list = []
        index = 0
        sum_entries = 0

        #   Ausgabe für jeden einzelnen Wert ungleich 0, im Zustandsvektor
        for value in self.general_matrix:

            if round(abs(value), 13) != 0.:  #ToDo Genauigkeit?

                #   Summiere den Betrag der Einträge zum quadrat, für die Geamtwahrscheinlichkeit (muss 100% sein)
                sum_entries += pow(abs(value), 2)

                #   Umwandlung des Indexes in ein Bitmuster (3 --> 0011)
                diracnotation = self.getdiracnotation(index, self.getnqubits())

                #   Berechnung der Wahrscheinlichkeit in % ToDo: Genauigkeit?
                probability = round(pow(abs(value), 2) * 100, self.get_accuracy())

                #   Für die Ausgabe wird dem Ausgabestring für jeden Zustand eine neue Zeile Text hinzugefügt
                if Base.get_verbose() >= 0:
                    return_str += 'The state {} has a probability of {}%.\n'.format(diracnotation, probability)

                #   Für das Verbose-Level -1 (quiet) wird nur eine Liste ausgegeben.
                else:
                    return_list += [diracnotation, probability]

            index += 1

        #   Ist das Vebose-Level größer gleich 0, wird ein Text mit den Zuständen ausgegeben.
        if Base.get_verbose() >= 0:

            #   Ausgabe der Summe aus den gadrierten Beträgen der Elemente aus dem Zustandsvektor
            #   Damit wird die Normiertheit gepfüft, diese Summe muss 1 ergeben
            if Base.get_verbose() >= 1:
                return_str += '\nCheck normalization: {a}% == 100%'.format(a=round(sum_entries*100, self.get_accuracy()))
                # ToDo: Genauigkeit

            #   rstrip() entfernt den letzten Zeilenumbruch, der durch for-Schleife zu viel ist
            return return_str.rstrip()

        #   Bei --quite wird nur ein Vektor ausgegeben.
        else:
            return str(return_list)

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

        if Base.get_verbose() >= 0:
            diracnotation = '|' + (n_qubits - len(str_var)) * '0' + str_var + ')'
        else:
            diracnotation = (n_qubits - len(str_var)) * '0' + str_var

        return diracnotation

    def init_vec_from_index(self, int_in):
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
