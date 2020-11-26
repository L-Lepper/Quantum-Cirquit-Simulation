#   Projektarbeit Literaturrecherche zu Simulationsalgorithmen für Quantencomputing
#   Author: Lukas Lepper, 24.11.2020
#   Betreuer: Martin Hardieck
#   Dateiname: QuantumSimulation.py
#   Version: 0.6


#   Importiere wie in der main oben beschrieben, alle Klassen auf der untersten Ebene. Durch Objekte in diesen Klassen
#   kann auf alle Funktionen zugegriffen werden, die benötigt werden.
from Base import Base
from Operation import Operation
from QState import QState
from G_PauliX import PauliX
from G_PauliZ import PauliZ
from G_Hadarmard import HadamardH
from Measurement import Measurement
from G_PauliY import PauliY
from G_Rphi import GateRphi
from G_Identity import GIdentity
from G_U3ThetaPhiLamda import GU3ThetaPhiLamda
from CNOT import CNOT
from G_Toffoli import Toffoli
from G_Fredkin import Fredkin
from G_Deutsch import Deutsch
import cmath

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

        #   Initialzustand = Basiszustand ist standardmäßig 000.. --> Index 0 im Vektor
        self.index_of_basis_state = 0

        self.clear_memory = False
        self.interactive_input = False

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

        #   Führe nacheinander die Operationen aus operation_obj.list_of_operations
        for operation in self.operation_obj.list_of_operations:

            #   Falls ein Element der Liste Indizes in der Liste operation[1] gespeichert hat, handelt es sich um ein
            #   Gatter, ansonsten um einen Befehl, wie print state (in der Form 'state')
            if operation[1]:
                #   In der mehr-Dimensionalen Liste list_of_operations wird aus dem Element mit dem aktuellen Index
                #   i, die Liste mit den Indizes der Qubits, auf welche das Gatter angewendet wird, ausgelesen.
                #   [ ['h', [1], []], ['cx', [0, 3, 6], [], [print_gates, [], []] ]
                list_affected_qubits = operation[1]
                list_of_parameters = operation[2]

                #   Erzeugen des benötigten Objekt für das Gatter (Gatter werden durch Konstruktor automatisch auf richtige
                #   Größe erweitert.
                if operation[0] == 'x':
                    self.qgate_obj = PauliX(list_affected_qubits)
                elif operation[0] == 'z':
                    self.qgate_obj = PauliZ(list_affected_qubits)
                elif operation[0] == 'h':
                    self.qgate_obj = HadamardH(list_affected_qubits)
                elif operation[0] == 'y':
                    self.qgate_obj = PauliY(list_affected_qubits)
                elif operation[0] == 'r_phi':
                    self.qgate_obj = GateRphi(list_affected_qubits, list_of_parameters)
                elif operation[0] == 's':
                    self.qgate_obj = GateRphi(list_affected_qubits, [cmath.pi/2])
                elif operation[0] == 's*':
                    self.qgate_obj = GateRphi(list_affected_qubits, [-cmath.pi/2])
                elif operation[0] == 't':
                    self.qgate_obj = GateRphi(list_affected_qubits, [cmath.pi/4])
                elif operation[0] == 't*':
                    self.qgate_obj = GateRphi(list_affected_qubits, [cmath.pi/4])
                elif operation[0] == 'i':
                    self.qgate_obj = GIdentity(list_affected_qubits)
                elif operation[0] == 'u3':
                    self.qgate_obj = GU3ThetaPhiLamda(list_affected_qubits, list_of_parameters)
                elif operation[0] == 'cnot':
                    self.qgate_obj = CNOT(list_affected_qubits)
                elif operation[0] == 'toffoli':
                    self.qgate_obj = Toffoli(list_affected_qubits)
                elif operation[0] == 'fredkin' or operation[0] == 'cswap':
                    self.qgate_obj = Fredkin(list_affected_qubits)
                elif operation[0] == 'deutsch':
                    self.qgate_obj = Deutsch(list_affected_qubits, list_of_parameters)
                elif operation[0] == 'm':

                    #   Erstelle Objekt für die Messung, dabei wird auch ein Objekt für das Entscheidungsdiagramm
                    #   erstellt --> Im Debug Modus: Ausgabe der einzelnen Schritte zum erstellen eines
                    #   Entscheidungsdiagramms
                    measure_obj = Measurement(self.qstate_obj.general_matrix, list_affected_qubits)

                    #   gebe Zustände des Zustandsvektors vor der Messung aus
                    if Base.get_verbose() >= 0:
                        print('\n---------------\t Measurement \t---------------\n')
                    if Base.get_verbose() >= 1:
                        print('States of the state vector before the measurement:')
                        print(self.qstate_obj, '\n')

                    #   Bei der Messung wird anstatt der Multiplikation unten, die Funktion measure() aufgerufen.
                    self.qstate_obj.general_matrix = measure_obj.measure()

                    #   gebe Zustände des Zustandsvektors nach der Messung aus
                    if Base.get_verbose() >= 1:
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
                        #self.qstate_obj.general_matrix = np.array([0.080396894, 0.037517934, 0j, 0j, 0j, 0j, 0j, 0j, 0j, 0j, 0j, 0j, 0j, 0j, 0j, 0j, 0.143565882, 0.066997412, 0j, 0j, 0j, 0j, 0j, 0j, 0.777808047, 0j, 0.601700565, 0j, 0j, 0j, 0j, 0j])
                        #qsim_obj.qstate_obj.general_matrix = np.array([1, 1, 0j, 0j, 0j, 0j, 0j, 0j, 0j, 0j, 0j, 0j, 0j, 0j, 0j, 0j, 1, 1, 0j, 0j, 0j, 0j, 0j, 0j, 1, 0j, 1, 0j, 0j, 0j, 0j, 0j])
                        self.qstate_obj.general_matrix = np.array([0, 0, 0.00752268163518088, 0, 0, 0, 0, 0, 0, 0, 0.306489370178815, 0.353641580975556, 0, 0, 0, 0, 0, 0, 0.286171213985822, 0.330197554599025, 0, 0, 0, 0, 0, 0.523233828563029, 0, 0.391028839851374, 0.283219972790003, 0.288323035362795, 0, 0])
                    elif self.getnqubits() == 4:
                        self.qstate_obj.general_matrix = np.array([0, 0.350723877, 0, 0.350723877, 0, 0.344408624, 0.344408624, 0, 0, 0.363103585, 0, 0.356154234, 0, 0.358337265, 0.360076766, 0])
                    elif self.getnqubits() == 6:
                        #   1
                        #self.qstate_obj.general_matrix = np.array([0.0812610073560534, 0.162522014712107, 0.237532175348464, 0.118766087674232, 0.162522014712107, 0.0812610073560534, 0.118766087674232, 0.237532175348464, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.12640601144275, 0.2528120228855, 0.369494494986499, 0.18474724749325, 0.2528120228855, 0.12640601144275, 0.18474724749325, 0.369494494986499, 0, 0, 0, 0, 0.540196630097221, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])

                        #   2
                        self.qstate_obj.general_matrix = np.array([0.0967127694558382, 0.193425538911676, 0.28269886456322, 0.14134943228161, 0.193425538911676, 0.0967127694558382, 0.14134943228161, 0.28269886456322, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.0967127694558382, 0.193425538911676, 0.28269886456322, 0.14134943228161, 0.193425538911676, 0.0967127694558382, 0.14134943228161, 0.28269886456322, 0, 0, 0, 0, 0.642914896667491, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])

                        #   3
                        #self.qstate_obj.general_matrix = np.array([0.20135869720078, 0.256274705528265, 0.321047433299145, 0.42806324439886, 0.31119071385575, 0.237969369419103, 0.401309291623931, 0.107015811099715, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.0366106722183236, 0.0549160083274853, 0.240785574974359, 0.0267539527749288, 0.109832016654971, 0.0915266805458089, 0.21403162219943, 0.267539527749287, 0, 0, 0, 0, 0.283938420180097, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
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

                #   Gebe den aktuell gespeicherten Initialzustand aus
                elif operation[0] == 'print_init_state':
                    self.print_init_state()

                # Index welches Tupel abgearbeitet wird, wird hochgezählt
                i += 1

        return self.qstate_obj

    #   1
    def process_n_qubits(self, n_qubits):
        """
        Setzt die Anzahl der QUbits und initialisiert sie mit 0, sofern vorher der default Wert 0 war. In der
        interactiven Eingabe wird die Anzahl an Qubits durch den ersten Befhel festgelegt.
        :param n_qubits:
        :return:
        """

        #   Falls die bisherige Anzahl an Qubits noch 0 ist, wird die neue Anzahl gespeichert. Wird der Befehl
        #   interaktiv hintereinander aufgerufen, kann die Anzahl des ersten Befehls für alle nachfolgenden Befehle
        #   verwendet.
        if Base.getnqubits() == 0:

            #   Anzahl an Qubits wird gespeichert
            self.set_n_qubits(n_qubits)

        elif n_qubits != Base.getnqubits():
            print('Due to the previous setting the number of qubits is', Base.getnqubits(),
                  '. The new input of', n_qubits, 'qubits is ignored. Use --clear to delete memory.')

    #   3
    def process_operation(self, operation_in):
        """
        Fügt die Gatter der Liste an Operationen hinzu.
        :param operation_in: Liste mit 0: Bezeichnung des Gatters/Befehl, 1: Liste der Indizes der Qubits, die das
         Gatter beeinflussen, 2: Liste der Parameter, die für das Gatter notwendig sind. Liste, die der Liste aller
         Operationen hinzugefügt wird
        :return:
        """

        #   Falls Operation ein Gatter ist, gibt es in der Liste mindestens 1 Index.
        if operation_in[1]:

            #   Wird ein Gatter auf ein Index über der Anzahl an Qubits angewendet, soll es einen Fehler geben
            if max(operation_in[1]) >= Base.getnqubits():
                raise IndexError('The Index of a gate is aut of range. It does\'t fit to the number of Qubits.')

        #   Der Operationen-Liste wird über die Funktion aus dem Operation-Objekt ein Tupel aus Gatter, Liste der
        #   betreffendem Qubits und Liste der Parameter hinzugefügt.
        self.operation_obj.add_operation_to_list([operation_in])

    def start_simulation(self):
        """
        Funktion prüft ob die Anzahl der Qubits größer 0 ist und ob in der Liste der Operationen Elemente vorhanden sind,
        und startet anschließend die Simulation.
        :return:
        """
        if Base.getnqubits() > 0 and self.operation_obj.list_of_operations:

            #   Falls im QState Objekt noch kein Vektor qsim_obj.general_matrix existiert, wird der neue Initialzustand
            #   verwendet
            if not any(self.qstate_obj.general_matrix):

                self.qstate_obj.init_vec_from_index(self.index_of_basis_state)

            #   Falls im QState Objekt bereits ein Vektor qsim_obj.general_matrix existiert, wird dieser als aktueller
            #   Zustandsvektor verwendet, auf den alle Operationen angewendet werden
            else:
                if Base.get_verbose() >= 0:
                    print('Using previous state vector instead of a new base state / initial state...\n'
                          '(use -c to start a completely new simulation)')

            #   Führe Berechnung der eingelesenen Eingabe durch
            self.qstate_obj = self.calculate()

            #   Ausgabe der Zustände nach der Simulation, falls vebose level 0 (nicht quiet)
            if Base.get_verbose() >= 0:
                print('\n---------------\t Simulation completed: \t---------------\n')
            print(self.qstate_obj, '\n\n\n')

        else:
            if Base.get_verbose() >= 0:
                print('\nSimulation was not started, the number of qubits is 0 or the list of operations is empty. '
                      'Type clii -h for help.\n')

    #   7
    def print_list_of_operations(self):
        """
        Funktion gibt die Liste der Operationen aus.
        :return:
        """

        if Base.get_verbose() >= 0:
            print('\n---------------\t List of operations: \t---------------\n')

            #   Falls in der Liste der Operationen Elemente vorhanden sind:
            if self.operation_obj.list_of_operations:
                print('\tGate/Command\t| Indices\t| Parameters')

                for operation in self.operation_obj.list_of_operations:
                    str_out = ''
                    if operation[1]:
                        str_out += '\t  ' + operation[0] + '\t\t|  ' + str(operation[1]) + '\t\t|  ' + str(operation[2]) + '\n'
                    else:
                        str_out += '\t ' + operation[0] + '\n'

                    print(str_out.rstrip())
                print('')
            else:
                print('The list is empty.\n')

        else:
            print(self.operation_obj.list_of_operations)

    #   7
    def print_actual_states(self, as_vector):
        if Base.get_verbose() >= 0:
            print('\n---------------\t Output actual state: \t---------------\n')

        if as_vector:
            print(self.qstate_obj.general_matrix)
        else:
            print(self.qstate_obj)

    #   7
    def print_init_state(self):
        """
        Die Funktion gibt den Initialzustand aus.
        :return:
        """

        #   Ausgabestring erstellen
        #   For-Schleife notwendig, da Liste in String gespeichert werden soll. Mit Strings konnte vorher
        #   nicht gearbeitet werden, da z.B. bsp_str[2]='g' nicht funktioniert.
        phi_str = "|"
        phi_str += str(bin(self.index_of_basis_state)[2:])
        phi_str += ")"

        print('\n---------------\t Output initial state: \t---------------\n'
              'The initial state in dirac notation is', phi_str, '.')

    #   8
    def clear_mem(self):
        """
        Diese Funktion löscht die Liste der Operationen, die Anzahl der Qubits und den Initialzustand.
        Sie löscht aber keine Objekte. Das ist bisher nicht nötig wegen der GarbageCollection.
        """

        #   Entferne alle Gatter in der Liste aller Operationen, die ausgeführt werden sollen
        self.operation_obj.list_of_operations = []

        #   Setze die Anzahl der Qubits auf 0
        self.set_n_qubits(0)

        #   Lösche die Initialisierung aller Qubits (Default-Basiszustand 0000..0)
        self.index_of_basis_state = 0

        #   Lösche den aktuellen Zustandsvektor
        self.qstate_obj.general_matrix = np.array([])
