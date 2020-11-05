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
from pathlib import Path
import argparse

#wird nur für custm Zustandsvektor benötigt
import numpy as np


"""
Die Klassen für den Parser müssen mit in die Datei QuantumSimulation.py, da in der benutzerdefinierten Aktion für das
Einlesen aus der Datei, eine Funktion von hier aufgerufen wird. Mann kann nicht gegenseitig zwei Dateien importieren.
"""
class ValidateInitialization(argparse.Action, Base):
    """
    Klasse mit einer benutzerdefinierten Argparse Akion, um zu Prüfen, ob die Eingabe für die Initialisierung der
    Qubits -i 2 1 gültig ist. Die eingegebenen Initialisierungen werden in einer Liste im namespace gespeichert.
    """

    def __call__(self, parser, namespace, values, option_string=None):
        #   Tupel mit den gültigen Werten, die für state in -i INDEX STATE erlaubt sind
        valid_states = (0, 1)

        #   Speichere die eingegebenen Parameter
        index, state = values

        #   Falls der Wert nicht in dem Tupel mit den gültigen Eingaben vorkommt, wird eine Fehlermeldung ausgegeben
        if state not in valid_states:
            raise argparse.ArgumentError(self, 'Invalid state for initializing the qubit '
                                               'with index {r!r}: {s!r}'.format(r=index, s=state))

        #   In Items wird die Liste gespeichert, die bisher in dem Parsor in namespace unter self.dest gespeichert war.
        items = getattr(namespace, self.dest, None)

        #   Falls vorher Elemente in der Liste gespeichert waren, werden die neuen Werte value=[Index, State]
        #   der Liste hinzugefügt
        if items:
            items.append(values)

        #   War die Liste leer, wird eine neue Liste mit dem neuen Element erstellt
        else:
            items = [values]

        #   In namespace von dem aktuellen Parsor wird die neue Liste Items an der Stelle der alten Liste gespeichert
        setattr(namespace, self.dest, items)


class ValidateGate(argparse.Action):
    """
    Klasse mit einer benutzerdefinierten Argparse Akion, um zu Prüfen, ob die Eingabe für das Gatter gültig ist.
    -g GATE INDEX Die beiden Parameter werden in der Liste der eingegebenen Gatter self.dest gespeichert.
    """

    def __call__(self, parser, namespace, values, option_string=None):

        #   Wurde nur ein Parameter -g m eingegeben, wird eine Fehlermeldung ausgegeben, da mindestens ein Index
        #   für alle Gatter erforderlich ist.
        if len(values) <= 1:
            raise argparse.ArgumentError(self, 'Missing values for --gate GATE INDEX ...INDEX')

        #   Speicher den ersten Parameter, der eingegeben wurde. Er bezeichnet das Gatter
        gate = values[0]

        #   Speichere die eingegebenen Indizes in einer Liste
        indices_of_qbits = values[1:]

        #   Tupel mit allen möglichen Parametern, die für Gatter stehen, welche auf ein einzelnes Qubit angewendet
        #   werden und daher nur einen Index-Parameter benötigen
        valid_gates = ('x', 'h', 'z', 'm', 'custm')

        #   Prüfe, ob das eingegebene Gatter in dem Tupel der möglichen Gatter vorkommt.
        #   Falls nein, wird eine Fehlermeldung ausgegeben und das Programm abgebrochen
        if gate not in valid_gates:
            raise argparse.ArgumentError(self, 'Invalid gate: {s!r}'.format(s=gate))

        #   Gehe die Liste der Indizes nacheinander durch. i ist der Index des aktuellen Elements in der Liste,
        #   x das Element selber
        for i, x in enumerate(indices_of_qbits):

            #   Versuche das aktuelle Element x in Integer zu konvertieren, sonst gebe eine Fehlermeldung aus
            #   Als Eingabe werden ganze Zahlen erwartet.
            try:
                indices_of_qbits[i] = int(x)
            except ValueError:
                raise argparse.ArgumentError(self, 'Value Error: {a!r} can\'t be converted to integer, '
                                                   'for index of the qubit an integer was expected.'.format(a=x))

            #   Falls die Zahl negativ ist, wird ebenfalls ein Fehler ausgegeben
            if indices_of_qbits[i] < 0:
                raise argparse.ArgumentError(self, 'Value Error: the index must be positive: {a!r}'
                                             .format(a=indices_of_qbits[i]))

        #   Gates that change 1 qubit:
        #   Tupel mit allen möglichen Parametern, die für Gatter stehen, welche auf ein einzelnes Qubit angewendet
        #   werden und daher nur einen Index-Parameter benötigen
        gates_1_qb = ('x', 'h', 'z', 'm', 'custm')

        #   Falls das aktuelle Gatter in dieser Liste vorkommt, sollte es nur einen Index haben:
        if gate in gates_1_qb:

            #   Fehlermelduung, wenn mehr Indizes eingegeben wurden
            if len(indices_of_qbits) != 1:
                raise argparse.ArgumentError(self, 'The number of indices ({r!r}) does not match the required '
                                                   'number of this gate ({s!r}: 1).'
                                             .format(r=len(indices_of_qbits), s=gate))

        #   Gates that change 2 qubits:
        #   Tupel mit allen möglichen Parametern, die für Gatter stehen, welche auf zwei Qubits angewendet
        #   werden und daher zwei Index-Parameter benötigen.
        # gates_2_qb = ('cx')

        #   Ein neues Element wird aus dem geprüften Gatter und der Liste der Indizes erstellt. Ist identisch mit value
        new_item = [gate] + indices_of_qbits

        #   Die alte Liste der bisherigen Gatter/Operationen wird gespeichert
        items = getattr(namespace, self.dest, None)

        #   Falls in dieser Liste bereits Gatter/Operationen enthalten sind, wird das neue Element ['m', 1]
        #   der Liste angehängt.
        if items:
            items.append(new_item)

        #   Ansonsten wird eine neue Liste mit dem aktuellen Element erstellt
        else:
            items = [new_item]

        #   Die bearbeitete Liste wird an der alten Position im Parsor gespeichert
        setattr(namespace, self.dest, items)


class CheckFilePath(argparse.Action):
    """
    Klasse mit einer benutzerdefinierten Argparse Akion, um zu Prüfen, ob die Eingabe für den Dateipfad gültig ist.
    Es wird geprüft, ob die Datei existiert. Dann werden die Befehle eingelesen und als Liste an der Stelle gespeichert,
    wo vorher der Dateipfad übergeben wurde.
    """

    def __call__(self, parser, namespace, values, option_string=None):

        #   Öffne die Datei, wenn möglich, und Schließe sie wieder am Ende der Umgebung. Ansonsten wird automatisch
        #   eine Fehlermeldung ausgegeben.
        with open(values) as file:

            #   Lese die gesammte Datei, Zeile für Zeile ein, und Speichere sie in einer Liste
            list_of_cmds = file.readlines()

        #   Erstelle eine neue Liste, in der gleich die eingelesenen Parameter gespeichert werden. Sie beginnt mit
        #   'cli', da diese Liste nach dem ArgParse aufruf in einen neuen Parser eingegeben wird. (Aktuell erfolgt die
        #   Eingabe des Schaltungsaufbaus entweder in der Datei, oder in dim Command Line Interface)
        args_list_from_file = ['cli']

        #   Zeile für Zeile werden die Parameter eingelesen und in der Liste oben angehängt
        for cmd in list_of_cmds:

            #   rstrip() entfernt Leerzeichen und Zeilenumbrüche am Ende eines Strings
            #   split() trennt String nach den Leerzeichen --> Aus Parameter mit Argumenten pro Zeile / Element in
            #   der Liste wird Liste mit neuen Elementen für jedes Argument
            args_list_from_file += cmd.rstrip().split()

        #   Speichere die neue Liste mit den eingelesenen Parametern am selben Ort, wo vorher der Dateipfad
        #   übergeben wurde
        setattr(namespace, self.dest, args_list_from_file)


class ValidatePrint(argparse.Action):
    """
    Klasse mit einer benutzerdefinierten Argparse Akion, um zu Prüfen, ob die Eingabe für print gültig ist.
    Außerdem wird der Print Befehl der Liste aller Operationen hinzugefügt.
    -g {STATE, GATES}
    """

    def __call__(self, parser, namespace, values, option_string=None):

        #   Die alte Liste der bisherigen Operationen wird gespeichert
        items = getattr(namespace, self.dest, None)

        str_out = 'print_' + values
        new_item = [str_out]

        #   Falls in dieser Liste bereits Operationen enthalten sind, wird das neue Element ['print', 'STATE|GATE']
        #   der Liste angehängt.
        if items:
            items.append(new_item)

        #   Ansonsten wird eine neue Liste mit dem aktuellen Element erstellt
        else:
            items = [new_item]

        #   Die bearbeitete Liste wird an der alten Position im Parsor gespeichert
        setattr(namespace, self.dest, items)


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
                    self.qstate_obj.general_matrix = measure_obj.measure

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
                        self.qstate_obj.general_matrix = np.array([0.080396894, 0.037517934, 0j, 0j, 0j, 0j, 0j, 0j, 0j, 0j, 0j, 0j, 0j, 0j, 0j, 0j, 0.143565882, 0.066997412, 0j, 0j, 0j, 0j, 0j, 0j, 0.777808047, 0j, 0.601700565, 0j, 0j, 0j, 0j, 0j])
                        #self.qstate_obj.general_matrix = np.array([1, 1, 0j, 0j, 0j, 0j, 0j, 0j, 0j, 0j, 0j, 0j, 0j, 0j, 0j, 0j, 1, 1, 0j, 0j, 0j, 0j, 0j, 0j, 1, 0j, 1, 0j, 0j, 0j, 0j, 0j])

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

    #   Funktion nimmt nacheinander Befehler aus dem Konsolenfenster entgegen und startet entsprechend die Simulation
    #   Einlesen von Befehlen aus Datei erfolgt über Befehl mit Dateipfad in der Konsole
    def cmd_input_for_qsim(self):
        """
        Diese Funktion wird in der main() aufgerufen, und fragt die Eingabe eines Befehls ab. Diese Funktion bildet das
        Commandline Interface. Die Eingabe wird an die Funktion cmd_line_parser() übergeben, welche die Parameter
        ausliest und weiter verarbeitet. Anschließend wird hier die Simulation gestartet und anschließend der Speicher
        gelöscht, falls in dem Eingabebefehl vorgesehen. Gab es keine Fehlermeldung, die das Programm immer abbrechen,
        wird an dieser Stelle nach einer neuen Eingabe gefragt.
        :return: True/ False. Je nachdem ob die Schleife zur Abfrage eines neuen Befehls abgebrochen werden soll oder
        nicht.
        """

        #   Speichere die erste Eingabe
        cmd_input = input().lower()

        #   Solange die Funktion execute_cmd() False zurück gibt, wird immer auf eine neue Konsoleneingabe gewartet.
        #   Das ist aktuell immer der Fall
        while True:

            #   Parse den eingegebenen Befehl, verarbeite die eingegebenen Parameter.
            #   Speichere den zurückgegebenen Wert. split() zerlegt den eingegebenen Befehl in die Einzelnen Argumente
            #   pro Zeile. Es wird nach Leerzeichen getrennt.
            bool_a = self.cmd_line_parser(cmd_input.split())

            #   Starte die Simulation
            self.start_simulation()

            #   Wurde True zurückgegeben, wird die Schleife und damit das Programm beendet.
            if bool_a:
                break

            #   Die Liste aller Gatter und der Initialzustand wird gelöscht, die Anzahl der Qubits wird auf 0 gesetzt
            #   (Falls -c --clear im eingegebenen Befehl)
            if self.clear_memory:
                QuantumSimulation.clear_mem(self)

            #   Es wird auf eine neue Eingabe gewartet
            cmd_input = input().lower()


    def cmd_line_parser(self, cmd_input):
        """
        Diese Funktion beinhaltet den Parser, der aus den Befehlen die Argumente ausliest und ruft weitere Funktionen
        auf, welche die eingegebenen Parameter verarbeiten. Der Befehl hat zwei Teilbefehle. Entweder kann der
        Schaltungsaufbau über das CLI eingelesen werden, oder aus einer Datei. --> -h, file -h, cli -h
        :param cmd_input: eingegebener Befehl
        :return:
        """

        #   Parser-Objekt erstellen
        parser = argparse.ArgumentParser(description='Simulation of Quantum Algorithm',
                                         epilog='by Lukas Lepper')

        #   Subparser-Objekt erstellen
        subparsers = parser.add_subparsers(title='sub-commands',
                                           description='read quantum circuit from file or from command '
                                                       'line interface input',
                                           dest='subparser_name',
                                           required=True)

        #   Gruppe aus nicht kompatiblen Parametern: Verbose-Level einstellen oder quite, um Ausgabe auf Ergebnisse zu
        #   beschränken
        verbose_groupe = parser.add_mutually_exclusive_group()

        #   Teilbefehl, der den Schaltungsaufbau aus der Eingabe ausliest
        parser_from_cli = subparsers.add_parser('cli', help='Input parameters from Commandline Interface')

        #   im Argumlent_Objekt des Parser wird an der Stelle function 'self.process_cli' gespeichert. Damit wird später
        #   der Funktionsaufruf args.function(args) zu self.process_cli(args), wenn der Teilbefehl cli aufgerufen wurde.
        parser_from_cli.set_defaults(function=self.process_cli)

    # Argumente für den Teilbefehl cli
        #   1: positional Argument für die Anzahl der Qubits
        parser_from_cli.add_argument('n_qubits',
                                     action='store',
                                     type=int,
                                     default=Base.getnqubits(),
                                     help='Set number of qubits. Initialize new qubits with 0.'
                                          'Index for inizializing or for the gates have to be in range of this number.')

        #   2: Argument um Qubits zu initialisieren
        parser_from_cli.add_argument('--init_qubit', '-i',
                                     dest='arg_phi_in',
                                     action=ValidateInitialization,
                                     type=int,
                                     nargs=2,
                                     metavar=('INDEX', 'STATE'),
                                     help='Initialize qubit INDEX with STATE = {0|1}.'
                                     )

        #   3: Argument um Gatter einzulesen
        parser_from_cli.add_argument('--gate', '-g',
                                     dest='list_of_operations',
                                     action=ValidateGate,
                                     nargs='+',
                                     metavar=('GATE', 'INDEX_1'),
                                     help='Gate and indices of the affected qubits.'
                                     )

        #   7: Argument um die Liste der Gatter oder den aktuellen Zustand auszugeben (Wird auch in der Liste der
        #   Operationen gespeichert)
        parser_from_cli.add_argument('--print', '-p',
                                     dest='list_of_operations',
                                     choices=['states', 'state_vec', 'gates'],
                                     action=ValidatePrint,
                                     help='Print the state vector or the list of gates')

        #   Teilbefehl, der den Schaltungsaufbau aus einer Datei ausliest
        parser_from_file = subparsers.add_parser('file', help='Input parameters from file')

        #   im Argumlent_Objekt des Parser wird an der Stelle function 'self.process_file' gespeichert. Damit wird
        #   später der Funktionsaufruf args.function(args) zu self.process_file(args), wenn der Teilbefehl file
        #   aufgerufen wurde.
        parser_from_file.set_defaults(function=self.process_file)

    # Argumente für den Teilbefehl file
        #   4: Argument um Datei einzulesen
        parser_from_file.add_argument('file',
                                      default=[],
                                      action=CheckFilePath,
                                      metavar='FILEPATH',
                                      help='Read command parameters from file.'
                                      )

    # Argumente, die im Elternbefehl vorkommen (In der Syntax vor den Teilbefhelen: -v 2 -c file c:/user...
        #   5: Argument um das Verbose-Level festzulegen
        verbose_groupe.add_argument('--verbose_level', '-v',
                                    dest='verbose_level',
                                    type=int,
                                    action='store',
                                    default=0,
                                    help='Increase output verbosity.'
                                    )

        #   6: Argument um die Ausgabe auf die Ergebnisse einzuschränken
        verbose_groupe.add_argument('--quiet', '-q',
                                    dest='quiet',
                                    action='store_true',
                                    help='Print only results.')

        #   8: Argument um nach der Simulation die alten Parameter zu löschen
        parser.add_argument('--clear', '-c',
                            dest='clear_mem',
                            action='store_true',
                            help='Delete the number of qubits, the list of gates, ... in memory.')

        #   9: Argument um meine erste Eingabe zu vewerwenden
        parser.add_argument('--interactive_input',
                            action='store_true',
                            help='Enter parameters one by one.')

        #   Parsor wird mit dem Eingegebenen Befehl aufgerufen (cmd_input ist bereits über split() in Argumente pro
        #   Zeile aufgeteilt)
        args = parser.parse_args(cmd_input)

        #   Je nach Teilbefehl wird in args.function ein bestimter Text gespeichert, der sich für die Teilbefehle
        #   unterscheidet. Für cli ist funcion = self.process_cli, für file, self.process_file. Somit werden je nach
        #   verwendetem Teilbefehl, verschiedene Funktionen aufgerufen.
        #   https://docs.python.org/3/library/argparse.html#sub-commands
        args.function(args)

        #   5   Das Verboselevel, bzw quiet wird verarbeitet (die betreffenden Variablen gesetzt)
        if args.quiet:

            #   Quiet bedeutet Debug-Modus auf -1
            Base.set_verbose_level(-1)
        else:
            Base.set_verbose_level(args.verbose_level)

# ToDo: kann eigentlich gelöscht werden
        #   9 Interaktive Abfrage wird hier zwischengeschaltet, falls in Eingabe gefragt. Kann mit cend beendet werden.
        if args.interactive_input:

            #   Führe den Befehl Help der Interaktiven Eingabe aus, damit Nutzer auf die alte Syntax aufmerksam wird
            print('\nAlte, interaktive Eingabe (Simulation wird nach Beenden mit \'cend\' fortgesetzt):\n')
            self.execute_cmd('help')

            while True:
                #   Es wird auf eine neue Eingabe gewartet
                cmd_input = input().lower()

                #   Falls 'cend' eingegeben wurde, wird die Schleife beendet und es wird mit der Simulation fortgefahren.
                if self.execute_cmd(cmd_input):
                    break

        #   Wurde -c eingegeben, damit die Liste der Gatter und Operationen gelöscht wird und n-qubits = 0, wird sich das
        #   in diesem Objekt gemerkt. Die Funktion clear_mem() wird erst später nach der Simulation ausgeführt.
        if args.clear_mem:
            self.clear_memory = True

        return False

    def process_cli(self, args):
        """
        Diese Funktion wird vom Parsor aufgerufen, wenn der Teilbefehl cli aufgerufen wurde.
        Sie verarbeitet die Argumente, die mit dem Parser ausgelesen wurden, indem sie kleinere Funktionen
        aufruft.
        :param args: Argumente aus dem Parsor des Teilbefehls cli.
        :return:
        """

        #   1: Setzte die Anzahl der Qubits
        self.process_n_qubits(args.n_qubits)

        #   Falls eine Initialisierung der Qubits eingegeben wurde, wird im phi_in Vektor das entsprechende Element
        #   auf 0 oder 1 gesetzt.
        if args.arg_phi_in:
            for element in args.arg_phi_in:
                index, value = element

                #   2
                self.initialize_qubits(index, value)

        #   Falls Operationen (Gatter oder Befehle wie der print state_vec Befehl) eingegeben wurden, werden diese über
        #   die Funktion process_operation() der Liste aller Operationen hinzugefügt
        if args.list_of_operations:
            for operation in args.list_of_operations:

                #   Falls gate nur 1 Element hat, ist die Operation kein Gatter, da Gatter mindestens 2 Elemente haben
                #   ['m', 1]. Nur Befehle wie ['print_state'] haben nur ein Element.
                if len(operation) == 1:

                    #   3
                    #   process_operation() nimmt als Operation den Befehl und fügt ihn der Liste an Operationen hinzu,
                    #   die Liste mit den Indizes bleibt leer.
                    self.process_operation(operation[0], [])

                #   Ansonsten ist es ein Gatter mit mindestens einem Index
                else:
                    #   Die Indizes, von denen das Gatter abhängig ist, sind in der Liste am Ende gespeichert
                    list_affected_qubits = operation[1:]

                    #   Das erste Element in der Liste bezeichnet das Gatter (m, h, z, x, ...)
                    gate_in = operation[0]

                    #   3
                    #   process_operation() fügt die Operation der Liste aller Operationen hinzu
                    self.process_operation(gate_in, list_affected_qubits)

        # ToDo Soll anders erfolgen
   #     if args.list_to_print:
    #        for element in args.list_to_print:
     #           #   7
      #          if element == 'gates':
       #             self.print_list_of_operations()
#
 #               elif element == 'state':
  #                  if Base.get_verbose() > 0:
   #                     print('Output actual state:')
    #                print(self.qstate_obj)

    def process_file(self, args):
        """
        Diese Funktion wird vom Parsor aufgerufen, wenn der Teilbefehl file aufgerufen wurde.
        Nachdem der erste Parsor aus der Datei die Argumente eingelesen hat, wird hier mit cmd_line_parser() der zweite
        Parsor aufgerufen, welcher die Argumente weiter verarbeitet.

        :param args: Argumente aus dem Parsor des Teilbefehls file.
        :return:
        """

        #   Der Parsor wird erneut aufgerufen, diesmal mit den Argumenten, die aus der Datei eingelesen wurden
        self.cmd_line_parser(args.file)

    #   1
    def process_n_qubits(self, n_qubits):
        """
        Setzt die Anzahl der QUbits und initialisiert sie mit 0.
        :param n_qubits:
        :return:
        """

        #   Falls der neue Wert größer ist als der bisherige Wert für die Qubits, wird die neue Anzahl
        #   gespeichert.
        if n_qubits >= Base.getnqubits():
            self.set_n_qubits(n_qubits)

            #   In der Liste phi_in wird für jedes neue Qubit eine 0 hinzugefügt.
            self.phi_in += (Base.getnqubits() - len(self.phi_in)) * [0]

        #   Dieser Fall sollte nach dem Parser nicht vorkommen, kann aber bei der interaktiven abfrage vorkommen
        else:
            raise ValueError('Number of qubits have to be greater than 0:', Base.getnqubits())

        #   Falls es bereits mehr Qubits gibt, als in dem Befehl vorgegeben, wird eine Warnung ausgegeben
        #   und alle darüberliegenden Qubits gelöscht

    #        else:
    #           print('\nWarnung!\n\tAnzahl der Qubits war', Base.getnqubits(), ', aber sollte auf',
    #                n_qubits, 'gesetzt werden.\n\tDie Anzahl an Qubits wurde auf', n_qubits,
    #               'geändert und alle darüber liegenden Qubits und deren Gatter wurden gelöscht!\n')
    #        self.set_n_qubits(n_qubits)

    #   Prüfen, dass Index wirklich weiter geht, als die neue Anzahl der Qubits
    #            if len(self.phi_in) > n_qubits:
    #               del self.phi_in[n_qubits:]

    #   Speichere die Operationen, die auf Qubits oberhalb von n_qubits angewendet werden
    #          list_of_elements = []
    #         for element in self.operation_obj.list_tuple_operation_qubit_i:
    #            if any(element):
    #               if max(element[1:]) >= n_qubits:
    #                  list_of_elements += [element]

    #   Entferne alle Gatter in der Liste aller Operationen, die auf Qubits angewendet werden sollen,
    #   die oben gelöscht wurden
    #            for element in list_of_elements:
    #               self.operation_obj.list_tuple_operation_qubit_i.remove(element)

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

        #   Die Anzahl der Qubits soll nicht automatisch festgelegt werden, sondern manuell mit -n
        if index >= Base.getnqubits():
            raise IndexError

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
            #      self.phi_in += (Base.getnqubits() - len(self.phi_in)) * [0]


            #   Wird ein Gatter auf ein Index über der Anzahl an Qubits angewendet, soll es einen Fehler geben
            if max(list_affected_qubits) >= Base.getnqubits():
                raise IndexError

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

            #   Das Bitmuster für den initialen Zustand, wird aus der Liste in einem String gespeichert
            phi_str = ""
            for value in self.phi_in:
                phi_str += str(value)

            #   Diese Funktion wandelt das Bitmuster 0011 in eine 3 um, und ruft dann die Funktion
            #   init_vec_with_bitsequence(self, int_in) in QState auf, die den zugehörigen Vektor im
            #   jeweiligen Objekt erzeugt
            self.init_qbit_sequence_to_statevec(phi_str)

            #   Führe Berechnung der eingelesenen Eingabe durch
            self.qstate_obj = self.calculate()

            #   Ausgabe der Zustände nach der Simulation, falls vebose level 0 (nicht quiet)
            if Base.get_verbose() >= 0:
                print('\n---------------\t Simulation completed: \t---------------\n')
            print(self.qstate_obj)

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

    def execute_cmd(self, cmd_input):
        """
        ToDo ist nicht ganz aktuell, könnte später gelöscht werden oder muss überarbeitet werden
        Diese Funktion führt die alten Befehle aus. Entweder wurden die Befehle aus dem Kommandofenster über die Funktion
        cmd_input_for_qsim() eingegeben, oder der Befehl cfile "PATH" liefert die eingelesenen Befehle aus einer Datei.

        :param cmd_input: Befehl, zu dem mit Hilfe von elif die Richtige Funktion zugewiesen wird, die ausgeführt wird.
        :return:
        """

        #   Gatter-Befehle
        if cmd_input[0] == 'g':

            #   Prüfe, ob mehr als nur 'g' eingegeben wurde
            if len(cmd_input) > 1:

                #   Für Gatter, die eine Quantenschaltung aufbauen
                if cmd_input[1] == 'h' or cmd_input[1] == 'x' or cmd_input[1] == 'z' or cmd_input[1] == 'm':

                    #   Finde Indizes der Variablen
                    #   g| name:h,x,z,cx |(| Zahl 1, 10, 100 |)
                    #   0      1 bis n   n+1    n bis m      m+1
                    i = cmd_input.find('(')
                    j = cmd_input.find(')')
                    gate_in = cmd_input[1:i]
                    list_affected_qubits = cmd_input[i + 1:j].split()
                    # ToDo: Prüfe richtige Anzahl an Parametern (betroffene Qubits) / Ist später unwichtig wenn Befehle anders aufgebaut sind
                    for i, x in enumerate(list_affected_qubits):
                        list_affected_qubits[i] = int(x)

                    #   3
                    self.process_operation(gate_in, list_affected_qubits)

                    #   Felermeldung soll nicht ausgegeben werden, daher wird an dieser Stelle schon die Funktion
                    #   beendet
                    return False

            print('\nFehler!\n\tUnbekanntes Gatter:', cmd_input, '\n')

        #   Sonstige Befehle
        elif cmd_input[0] == 'c':

            #   Debug-Modus und Verbose-Level verändern
            #   Syntax: cdebug true vl = 2
            if cmd_input[1:6] == 'debug':

                #   Debug-Modus aktivieren
                if cmd_input[7:11] == 'true':
                    index = cmd_input.find('= ') + 2

                    #   gültiges Verbose-Level auslesen
                    if index >= 0:
                        value = int(cmd_input[index:])
                    else:
                        value = 0

                    Base.set_verbose_level(value)

                #   Debug-Modus deaktivieren
                elif cmd_input[7:12] == 'false':
                    Base.reset_verbose_level()
                else:
                    print('\nFehler!\n\tSyntaxfehler:', cmd_input, cmd_input[7:11],
                          'entweder true oder fals(e), erwartete Syntax: cdebug true vl = 3, cdebug = false\n')

            #   Befehle aus Datei auslesen und ausführen
            elif cmd_input[1:5] == 'file':

                #   Finde Index, an dem der Dateipfad anfängt durch das Zeichen " und schneide alles davor ab
                i = cmd_input.find('\"') + 1
                file_name = cmd_input[i:]

                #   Suche Index, an dem der Dateipfad aufhört (wieder ") und schneide alles ab dem Zeichen " ab
                j = file_name.find('\"')
                file_name = file_name[0:j]

                # ---4
                #   file_obj erstellen, um zu prüfen, ob angegebene Datei existiert
                file_obj = Path(file_name)
                if file_obj.is_file():

                    #   Lese die gesammte Datei, Zeile für Zeile ein, und Speichere sie in einer Liste
                    list_of_cmds = open(file_name).readlines()

                    #   Führe die eingelesenen Befehle nacheinander aus. Falls der Befehl cend dabei war, gibt die
                    #   Funktion execute_cmd True zurück und das Programm wird beendet.
                    for cmd in list_of_cmds:
                        #   rstrip() entfernt Leerzeichen und Zeilenumbrüche am Ende eines Strings
                        if self.execute_cmd(cmd.rstrip()):
                            return True

                #   Falls die angegebene Datei nicht existiert:
                else:
                    # ---4
                    print('\nFehler!\n\tFolgende Datei wurde nicht gefunden:', file_name, '\n')

            #   Ausgabe bestimmter Parameter, wie der eingegebene Initialzustand oder die Liste der Gatter
            #   (cprint = gates|states)
            elif cmd_input[1:6] == 'print':

                #   Suche Index, wo Parameter des Befehls gespeichert sind
                index = cmd_input.find('= ') + 2

                #   Liste der gespeicherten Operationen ausgeben
                if cmd_input[index:index + 5] == 'gates':
                    #   7
                    self.print_list_of_operations()

                #   Aktuellen Initialzustand in Diracnotation ausgegben, z.B.: |10011)
                elif cmd_input[index:index + 5] == 'state':
                    #   7
                    self.print_init_state()
                else:
                    print('\nFehler!\n\tUnbekannte Syntax:', cmd_input,
                          '. Eingabe in der Form: cprint = state|gates erwartet.\n')

            #   Simulation ausführen, wenn Anzahl der Qubits größer 0 ist (Dann ist in self.phi_in auch ein Bitmuster
            #   in Form einer Liste gespeichert.
            elif cmd_input[1:9] == 'simulate':

                #   sim
                self.start_simulation()

            #   Zurücksetzen der Simulationsparameter
            elif cmd_input[1:6] == 'clear':

                #   8
                self.clear_mem()

            #   Beende das Programm
            elif cmd_input[1:4] == 'end':
                return True

            else:
                print('\nFehler!\n\tUnbekannter Befehl:', cmd_input, '\n')

        #   Quantenbefehle zur Initialisierung
        elif cmd_input[0] == 'q':

            #   Einlesen der Anzahl an Qubits
            #   Speichere Anzahl der Qubits global in der Klasse QuantumSimulation, sodass alle Objekte auf diese
            #   Information zugreifen können, mit get_n_qubits
            if cmd_input.find('b_n = ') >= 0:

                #   Suche Index, wo die Anzahl n steht uns speichere sie
                i = cmd_input.find('= ') + 2
                n_qubits = int(cmd_input[i:])

                #   1
                self.process_n_qubits(n_qubits)

            #   Initialisieren der Zustände der einzelnen Qubits (standardmäßig 0)
            elif cmd_input[0:3] == 'qb[':

                #   Index finden, an dem der Index des Qubit gespeichert ist. Kann mehrere Stellen haben...
                i = cmd_input.find('qb[') + 3
                j = cmd_input.find(']')
                index = int(cmd_input[i:j])

                #   Index, andem der Initialzustand des betreffenden Qubits gespeichert ist
                i = cmd_input.find('= ') + 2
                value = int(cmd_input[i])

                #   Falls der Zustand 0 oder 1 eingegeben wurde, wird dieser Wert in der Liste gespeichert
                if value == 0 or value == 1:

                    #   2
                    self.initialize_qubits(index, value)

                #   Andernfalls liegt ein Syntaxfehler vor, es wird angenommen dass der Zustand 1 sein sollte und
                #   es wird eine Warnung ausgegeben.
                else:
                    print('\nFehler!\n\tQubits können nur mit 0 oder 1 initialisiert werden, statdessen wurde der Wert',
                          value, 'eingegeben.\nQubit mit Index', index, 'wird mit 1 initialisiert.\n')
                    self.phi_in[index] = 1

            else:
                print('\nFehler!\n\tUnbekannte Initialisierung:', cmd_input, '\n')

        #   Befehl für die Hilfe: Auflistung aller möglichen Befehler mit ihrer Syntax
        elif cmd_input[0] == '?' or cmd_input == 'help' or cmd_input == 'h':

            print('\n##################################################\n')
            print('Liste aller Befehle für das Programm QuantumSimulation:\n'
                  '\tBefehle für den Initialzustand. Standardmäßig haben Qubits den Zustand 0.\n'
                  '\tqb_n = x\t\tLegt Anzahl n der Qubits entsprechend der Eingabe x fest.\n'
                  '\tqb[i] = x\t\tInitialisierung des i-ten Qubits auf den Wert x, x = {0, 1}.\n')
            print(
                '\tBefehle, um der Liste an Operationen verschiedene Gatter hinzuzufügen, welche auf das i-te Qubit angewendet werden.\n'
                '\tgx(i)\t\t\tPauli-X-Gatter.\n'
                '\tgz(i)\t\t\tPauli-Z-Gatter.\n'
                '\tgh(i)\t\t\tHadarmard-Gatter.\n'
                '\tgm(i)\t\t\tMessung des i-ten Qubits.\n')
            print('\tSonstige Befehle:\n'
                  '\tcdebug true|false vl = x Debug-Modus aktivieren oder deaktivieren. Beim aktivieren wird mit x das Verbose-Level 0-3 benötigt.\n'
                  '\tcfile "PATH"\t\t\tPATH gibt einen Dateipfad auf eine Textdatei an, aus der eine Liste an Befehlen eingelesen und ausgeführt werden soll. Z.b. cfile',
                  r' "C:\Users\NAME\Documents\test.txt"', '\n'
                                                          '\tcsimulate\t\t\t\tFalls die Anzahl an Qubits größer 0 ist, wird die Simulation gestartet.\n'
                                                          '\tcprint = state|gates\tGibt den aktuellen Initialzustand in Diracnotation oder die Liste der gespeicherten Gatter in ihrer Reihenfolge aus.\n'
                                                          '\tcclear\t\t\t\t\tLöscht alle Qubits und Gatter, und setzt die Anzahl an Qubits auf 0.\n'
                                                          '\tcend\t\t\t\t\tBeendet das Programm.\n'
                                                          '\t?|h|help\t\t\t\tListet alle Befehle auf.\n')
            print('##################################################\n')

        else:
            print('\nFehler!\n\tUnbekannter Eingabetyp:', cmd_input,
                  '. Tippe \'?\' oder \'help\' um alle Befehle aufgelistet zu bekommen.\n')

        return False
