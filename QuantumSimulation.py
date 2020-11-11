#   Projektarbeit Literaturrecherche zu Simulationsalgorithmen für Quantencomputing
#   Author: Lukas Lepper, 21.10.2020
#   Betreuer: Martin Hardieck
#   Dateiname: QuantumSimulation.py
#   Version: 0.5


#   Importiere wie in der main oben beschrieben, alle Klassen auf der untersten Ebene. Durch Objekte in diesen Klassen
#   kann auf alle Funktionen zugegriffen werden, die benötigt werden.
from Base import Base
from Operation import Operation
from QState import QState
from PauliX import PauliX
from PauliZ import PauliZ
from HadarmardH import HadamardH
from Measurement import Measurement
from PauliY import PauliY
from GateRphi import GateRphi
from pathlib import Path

#   wird nur für den custm Zustandsvektor benötigt
import numpy as np


class QuantumSimulation(Base):
    """
    In dieser Klasse sind die Hauptfunktionen des Programms definiert. Die hier definierten Funktionen erstellen
    Objekte der anderen Klassen. Diese Klassen erben von übergeordneeten Klassen, sodass Objekte nur aus den
    Kind-Klassen benötigt werden.

    Funktionen sind das Einlesen der Eingabe, das Initialisieren des Zustandsvektors und das Durchführen der Berechnung.
    Die Operationen werden in einer Liste gespeichert (Gatter, Messungen, Print Ausgaben) und nacheinander ausgeführt.
    """

    def __init__(self):
        super().__init__()

        #   Erstellen von Objekten, die in dieser Klasse benötigt werden
        self.qstate_obj = QState()
        self.operation_obj = Operation()
        self.qgate_obj = None
        self.phi_in = []
        self.clear_memory = False

    def calculate(self):
        """
        Funktion führt Operationen aus der Operation_List aus. Elemente dieser Liste werden abgearbeitet:
        Erstellt Objekt für Operation, und führt Multiplikation aus, wenn es ein Gatter ist. Wenn Messung oder der
        Befehl printdurchgeführt werden soll, wird die Multipligation Gate*State nicht ausgeführt, sondern der
        jeweilige Code.
        :return qstate_obj: Mit Ergebnis als Zustandsvektor.
        """

        #   Index in der operation_list
        i = 0

        #   Führe nacheinander die Operationen aus operation_obj.list_tuple_operation_qubit_i
        for operation in self.operation_obj.list_tuple_operation_qubit_i:

            #   Falls ein Element der Liste mehr als 2 Elemente hat, handelt es sich um ein Gatter, ansonsten um einen
            #   Befehl, wie print state (in der Form 'state')
            if len(operation) >= 2:
                #   In der 2-Dimensionalen Liste list_tuple_operation_qubit_i wird aus dem Element mit dem aktuellen Index
                #   i, die Liste mit den Indizes der Qubits, auf welche das Gatter angewendet wird, ausgelesen.
                #   [['h', 1], ['cx', 0, 3, 6]]
                list_affected_qubits = operation[1:]

                #   Erzeugen des benötigten Objekt für das Gatter (Gatter werden durch Konstruktor automatisch auf richtige
                #   Größe erweitert.
                if operation[0] == 'x':
                    self.qgate_obj = PauliX(list_affected_qubits)
                elif operation[0] == 'z':
                    self.qgate_obj = PauliZ(list_affected_qubits)
                elif operation[0] == 'h':
                    self.qgate_obj = HadamardH(list_affected_qubits)
            #    elif operation[0] == 'y':
             #       self.qgate_obj = PauliY(list_affected_qubits)
              #  elif operation[0] == 'r_phi':
               #     self.qgate_obj = GateRphi(list_affected_qubits)
                elif operation[0] == 'm':

                    #   Erstelle Objekt für die Messung, dabei wird auch ein Objekt für das Entscheidungsdiagramm
                    #   erstellt --> Im Debug Modus: Ausgabe der einzelnen Schritte zum erstellen eines
                    #   Entscheidungsdiagramms
                    measure_obj = Measurement(self.qstate_obj.general_matrix, list_affected_qubits)

                    #   gebe Zustände des Zustandsvektors vor der Messung aus
                    if Base.get_verbose() > 0:
                        print('\n---------------\t Test of measurement \t---------------\n\n'
                              'States of the state vector before the measurement:')
                        print(self.qstate_obj, '\n')

                    #   Bei der Messung wird anstatt der Multiplikation unten, die Funktion measure() aufgerufen.
                    self.qstate_obj.general_matrix = measure_obj.measure()

                    #   gebe Zustände des Zustandsvektors nach der Messung aus
                    if Base.get_verbose() > 0:
                        print('\nStates of the state vector after the measurement:')
                        print(self.qstate_obj, '\n')

                    # Index welches Tupel abgearbeitet wird, wird hochgezählt
                    i += 1

                    continue

                #   Das 'Gatter' custm überschreibt den bisherigen Zustand mit einem beliebigen Zustandsvektor, der hier
                #   gespeichert wurde, oder mit einem Initialzustand 000..000 für die richtige Anzahl an Qubits
                elif operation[0] == 'custm':

                    #   Falls die Anzahl an Qubits, der Anzahl aus dem gespeicherten Vektor entspricht, wird dieser
                    #   verwendet
                    if Base.getnqubits() == 5:
                        #qsim_obj.qstate_obj.general_matrix = np.array([0.080396894, 0.037517934, 0j, 0j, 0j, 0j, 0j, 0j, 0j, 0j, 0j, 0j, 0j, 0j, 0j, 0j, 0.143565882, 0.066997412, 0j, 0j, 0j, 0j, 0j, 0j, 0.777808047, 0j, 0.601700565, 0j, 0j, 0j, 0j, 0j])
                        #qsim_obj.qstate_obj.general_matrix = np.array([1, 1, 0j, 0j, 0j, 0j, 0j, 0j, 0j, 0j, 0j, 0j, 0j, 0j, 0j, 0j, 1, 1, 0j, 0j, 0j, 0j, 0j, 0j, 1, 0j, 1, 0j, 0j, 0j, 0j, 0j])
                        self.qstate_obj.general_matrix = np.array([0, 0, 0.00752268163518088, 0, 0, 0, 0, 0, 0, 0, 0.306489370178815, 0.353641580975556, 0, 0, 0, 0, 0, 0, 0.286171213985822, 0.330197554599025, 0, 0, 0, 0, 0, 0.523233828563029, 0, 0.391028839851374, 0.283219972790003, 0.288323035362795, 0, 0])
                    else:
                        self.qstate_obj.general_matrix = np.zeros(Base.getnqubits())
                        self.qstate_obj.general_matrix[0] = 1


                    # Index welches Tupel abgearbeitet wird, wird hochgezählt
                    i += 1

                    continue

                #   Fehler: Operation wird als gültige Eingabe erkannt, ist oben aber nicht aufgeführt
                else:
                    raise Exception('Error: The following operation was not recognized as Error in '
                                    'QuantumSimulation.py: cmd_input_for_qsim(),\n'
                                    'but is not implemented in QuantumSimulation.py: calculate():', operation)

                #   Multiplikation führt Simulation aus: Neuer Zustandsvektor nachdem Gatter angewendet wurde
                #   (Messung wird ebenfalls durch den Operator __mul__() aufgerufen)
                self.qstate_obj = self.qgate_obj * self.qstate_obj

                # Index welches Tupel abgearbeitet wird, wird hochgezählt
                i += 1

            else:
                #   Gebe die aktuellen Zustände mit Wahrscheinlichkeit aus
                if operation[0] == 'print_states':
                    self.print_actual_states(False)

                #   Gebe den aktuellen Zustandsvektor als Vektor aus
                elif operation[0] == 'print_state_vec':
                    self.print_actual_states(True)

                #   Gebe die Liste der Operationen aus
                elif operation[0] == 'print_gates':
                    self.print_list_of_operations()

                # Index welches Tupel abgearbeitet wird, wird hochgezählt
                i += 1

        return self.qstate_obj

    #   Bitmuster kann als binäre Zahl in int umgewandelt werden, und wieder zurück. Vorgehen ist effizienter als
    #   String. Integer Zahl entspricht dann dem Index im Zustandsvektor, beginnend bei 0. Dadurch erfolgt leichtere
    #   Vektorzuordnung.
    #   Funktion erzeugt aus initialem Bitmuster im qstate_obj den zugehörigen Zustandsvektor
    def init_qbit_sequence_to_statevec(self, bit_seq_as_str):
        """
        Funktion erzeugt aus dem eingelesenen Initalzustand den zugehörigen Zustandsvektor im QState-Objekt, welches
        in dieser Klasse enthalten ist. Der Initalzustand wird als String aus 0en und 1en übergeben.

        :param bit_seq_as_str: Der String des Initialzustandes kann als binäre Zahl in eine Dezimalzahl umgewandelt
        werden. Diese entspricht genau dem Index des Zustandes im Zustandsvektor. Dieses Vorgehen ist effizienter als
        die Verwendung des Strings.
        :return: void.
        """

        bit_seq_as_int = int(bit_seq_as_str, 2)
        self.qstate_obj = self.qstate_obj.init_vec_with_bitsequence(bit_seq_as_int)

    #   1
    def process_n_qubits(self, n_qubits):
        """
        Setzt die Anzahl der QUbits und initialisiert sie mit 0.
        :param n_qubits:
        :return:
        """

        #   Falls der neue Wert größer ist als der bisherige Wert für die Qubits, wird die neue Anzahl
        #   gespeichert. Wird der Befehl interaktiv hintereinander aufgerufen, kann die Anzahl für jede Simulation
        #   geändert werden.
        if n_qubits >= Base.getnqubits():

            #   Anzahl an Qubits wird gespeichert
            self.set_n_qubits(n_qubits)

            #   In der Liste phi_in wird für jedes neue Qubit eine 0 hinzugefügt.
            self.phi_in += (Base.getnqubits() - len(self.phi_in)) * [0]

        #   Falls es bereits mehr Qubits gibt, als in dem Befehl vorgegeben (und n_qubits in args existiert), wird eine
        #   Warnung ausgegeben und alle darüberliegenden Qubits gelöscht
        elif n_qubits:

            #raise ValueError('Number of qubits have to be greater than 0:', Base.getnqubits())
            print('\nWarning!\n\tThe number of qubits was', Base.getnqubits(),
                  'but should be set to', n_qubits, '\n\tThe number of qubits was set to', n_qubits,
                  'and all qubits above were deleted! Output vector is now the initial state,\n\t'
                  'because the previous state vector does not match the number of qubits anymore.')

            #   Speichere die Anzahl der Qubits
            self.set_n_qubits(n_qubits)

            #   Der aktuelle Zustandsvektor wird gelöscht, da sich die Anzahl der Qubits verändert hat
            self.qstate_obj.general_matrix = np.array([])

            #   Prüfen, dass Index wirklich weiter geht, als die neue Anzahl der Qubits
            if len(self.phi_in) > n_qubits:
                del self.phi_in[n_qubits:]

    #   2
    def initialize_qubits(self, index, value):
        """
        Initialisiert ein Qubit mit dem Zustand 0 oder 1.
        :param index: Index des Qubits
        :param value: Zustand 0 oder 1
        :return:
        """

        #   Falls der Index des zu initialisierenden Qubits aus dem Bereich der Anzahl an Qubits hinaus geht,
        #   wird eine Warnung ausgegeben und die Anzahl angepasst.
        #        if index >= Base.getnqubits():
        #           print('\nWarnung!\n\tAnzahl der Qubits war', Base.getnqubits(), ', aber das Qubit mit Index',
        #                index, 'liegt darüber.\n\tDie Anzahl an Qubits wurde auf', index + 1,
        #               'geändert!\n')
        #        Base.set_n_qubits(index + 1)

        #   Die Anzahl der Qubits soll nicht automatisch festgelegt werden
        if index >= Base.getnqubits():
            raise IndexError('The Index of a Qubit is aut of range. It does\'t fit to the number of Qubits.')

        #   Der Liste der initialen Zustände der Qubits wird mit 0en für die neuen Qubits erweitert
        self.phi_in += (Base.getnqubits() - len(self.phi_in)) * [0]

        #   Der Zustand wird in der Liste phi_in gespeichert
        self.phi_in[index] = value

    #   3
    def process_operation(self, operation_in, list_affected_qubits):
        """
        Fügt die Gatter der Liste an Operationen hinzu.
        :param operation_in: Gatter, Befehl, welches der Liste an Operationen hinzugefügt wird
        :param list_affected_qubits: Indizes der Qubits, die das Gatter beeinflussen.
        :return:
        """

        #   Falls Operation ein Gatter ist, gibt es in der Liste mindestens 1 Index.
        if list_affected_qubits:

            #   Falls die Anzahl der Qubits kleiner ist, als der Index des Qubits welches initialisiert wird, wird
            #   eine Warnung ausgegeben und die Anzahl angepasst. Die restlichen neuen Qubits haben den Zustand 0.
            #        if max(list_affected_qubits) >= Base.getnqubits():
            #           print('\nWarnung!\n\tAnzahl der Qubits war', Base.getnqubits(), ', aber das Qubit mit Index',
            #                max(list_affected_qubits), 'liegt darüber.\n\tDie Anzahl an Qubits wurde auf',
            #               max(list_affected_qubits) + 1,
            #              'geändert!\n')
            #       Base.set_n_qubits(max(list_affected_qubits) + 1)
            #      qsim_obj.phi_in += (Base.getnqubits() - len(qsim_obj.phi_in)) * [0]


            #   Wird ein Gatter auf ein Index über der Anzahl an Qubits angewendet, soll es einen Fehler geben
            if max(list_affected_qubits) >= Base.getnqubits():
                raise IndexError('The Index of a gate is aut of range. It does\'t fit to the number of Qubits.')

            #   Der Operationen-Liste wird über die Funktion aus dem Operation-Objekt ein Tupel aus Gatter und
            #   betreffendem Qubit hinzugefügt.
            temp = [operation_in] + list_affected_qubits  # ToDo: Funktion add_tuple... überarbeiten
            self.operation_obj.add_tuple_to_operation_list([temp])

        #   Ist die Liste leer, hatte das Element in der Liste aller Operationen nur 1 Element, als war es ein Befehl:
        #   Print-Befehl, welcher der Liste hinzugefügt werden soll. Kann auch ein anderer Befehl sein, es sind aber
        #   sonst keine Befehle als Operation implementiert.
        else:
            self.operation_obj.add_tuple_to_operation_list([[operation_in]])

    def start_simulation(self):
        """
        Funktion prüft ob die Anzahl der Qubits größer 0 ist und ob in der Liste der Operationen Elemente vorhanden sind,
        und startet anschließend die Simulation.
        :return:
        """
        if Base.getnqubits() > 0 and self.operation_obj.list_tuple_operation_qubit_i:

            #   Falls im QState Objekt noch kein Vektor qsim_obj.general_matrix existiert, wird der neue Initialzustand
            #   verwendet
            if not any(self.qstate_obj.general_matrix):

                #   Das Bitmuster für den initialen Zustand, wird aus der Liste in einem String gespeichert
                phi_str = ""
                for value in self.phi_in:
                    phi_str += str(value)

                #   Diese Funktion wandelt das Bitmuster 0011 in eine 3 um, und ruft dann die Funktion
                #   init_vec_with_bitsequence(qsim_obj, int_in) in QState auf, die den zugehörigen Vektor im
                #   jeweiligen Objekt erzeugt
                self.init_qbit_sequence_to_statevec(phi_str)

            #   Falls im QState Objekt bereits ein Vektor qsim_obj.general_matrix existiert, wird dieser als aktueller
            #   Zustandsvektor verwendet, auf den alle Operationen angewendet werden
            else:
                if Base.get_verbose() >= 0:
                    print('Using previous state vector instead of a new base state / initial state...\n'
                          '(use -c to start a completely new simulation)')

            #   Führe Berechnung der eingelesenen Eingabe durch
            self.qstate_obj = self.calculate()

        else:
            if Base.get_verbose() >= 0:
                print('\nSimulation was not started, the number of qubits is 0 or the list of operations is empty.\n')

    #   7
    def print_list_of_operations(self):
        """
        Funktion gibt die Liste der Operationen aus.
        :return:
        """

        if Base.get_verbose() >= 0:
            print('List of operations:')

            #   Falls in der Liste der Operationen Elemente vorhanden sind:
            if self.operation_obj.list_tuple_operation_qubit_i:
                print('\tGates\t| Index of qubits to which the gate is applied')

                for operation in self.operation_obj.list_tuple_operation_qubit_i:
                    str_out = ''
                    if len(operation) >= 2:
                        str_out += '\t\t' + operation[0] + '\t|\t' + str(operation[1]) + '\n'
                    else:
                        str_out += '\t\t' + operation[0] + '\n'

                    print(str_out.rstrip())
                print('')
            else:
                print('The list is empty.\n')

        else:
            print(self.operation_obj.list_tuple_operation_qubit_i)

    #   7 ToDo: Möglichkeit als Vektor auszugeben
    def print_actual_states(self, as_vector):
        if Base.get_verbose() > 0:
            print('Output actual state:')

        if as_vector:
            print(self.qstate_obj.general_matrix)
        else:
            print(self.qstate_obj)

    #   7
    def print_init_state(self):
        """
        Die Funktion gibt den Initialzustand aus. ToDO: Diese Funktion wird im neuen CLI nicht mehr benötigt.
        :return:
        """

        #   Ausgabestring erstellen
        #   For-Schleife notwendig, da Liste in String gespeichert werden soll. Mit Strings konnte vorher
        #   nicht gearbeitet werden, da z.B. bsp_str[2]='g' nicht funktioniert.
        phi_str = "|"
        for value in self.phi_in:
            phi_str += str(value)
        phi_str += ")"

        print('The initial state in dirac notation is', phi_str, '.')

    #   8
    def clear_mem(self):
        """
        Diese Funktion löscht die Liste der Operationen, die Anzahl der Qubits und den Initialzustand.
        Sie löscht aber keine Objekte. Das ist bisher nicht nötig wegen der GarbageCollection.
        """

        #   Entferne alle Gatter in der Liste aller Operationen, die ausgeführt werden sollen
        self.operation_obj.list_tuple_operation_qubit_i = []

        #   Setze die Anzahl der Qubits auf 0
        self.set_n_qubits(0)

        #   Lösche die Initialisierung aller Qubits
        del self.phi_in[:]

        #   Lösche den aktuellen Zustandsvektor
        self.qstate_obj.general_matrix = np.array([])
