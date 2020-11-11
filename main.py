#!/usr/bin/env python3
#   Projektarbeit Literaturrecherche zu Simulationsalgorithmen für Quantencomputing
#   Author: Lukas Lepper, 21.10.2020
#   Betreuer: Martin Hardieck
#   Dateiname: main.py
#   Version: 0.5

#   Klassen importieren, mit deren Memberfunktionen gearbeitet werden muss.
#   Die Klasse QuantumSimulation bietet die Hauptfunktionen für die Simulation an, die in der main gesteuert wird.
#   Sie benötigt daher Zugriff auf alle anderen Unterklassen der untersten Ebene. In den Funktionen dieser Hauptklasse
#   werden daher Objekte der untersten Ebene erzeugt. Die Klassen dieser Ebene erben von den darüber liegenden Klassen,
#   sodass alle Funktionen/Variablen in der Hauptklasse erreichbar sind.
from QuantumSimulation import QuantumSimulation
from Base import Base

import sys
import argparse


"""
Die Klassen ValidateInitialization, ValidateGate, ValidatePrint und CheckFilePath definieren benutzerdefinierte Aktionen 
für den Parser.
Dieser ist nachfolgend in der Funktion cmd_line_parser() implementiert. Je nach subcommand werden die 
Funktionen process_cli() oder process_file() aufgerufen, welche danach implementiert sind. 
Danach folgt der Programmstart mit if __name__ == '__main__': (siehe ganz unten).
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

        #   In Items wird die Liste gespeichert, die bisher in dem Parsor in namespace unter qsim_obj.dest gespeichert war.
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
    -g GATE INDEX Die beiden Parameter werden in der Liste der eingegebenen Gatter qsim_obj.dest gespeichert.
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
        valid_gates = ('x', 'h', 'z', 'm', 'custm', 'r_phi', 'y')

        #   Prüfe, ob das eingegebene Gatter in dem Tupel der möglichen Gatter vorkommt.
        #   Falls nein, wird eine Fehlermeldung ausgegeben und das Programm abgebrochen
        if gate not in valid_gates:
            raise argparse.ArgumentError(self, 'Invalid gate: {s!r}'.format(s=gate))

        #   Gates that change 1 qubit and need only one argument:
        #   Tupel mit allen möglichen Parametern, die für Gatter stehen, welche auf ein einzelnes Qubit angewendet
        #   werden und daher nur einen Index-Parameter benötigen
        gates_1_qb = ('x', 'h', 'z', 'm', 'custm', 'y')

        #   Falls das aktuelle Gatter in dieser Liste vorkommt, sollte es nur einen Index haben:
        if gate in gates_1_qb:

            #   Gehe die Liste der Indizes nacheinander durch. i ist der Index des aktuellen Elements in der Liste,
            #   x das Element selber
            for i, x in enumerate(indices_of_qbits):

                #   Versuche das aktuelle Element x in Integer zu konvertieren, sonst gebe eine Fehlermeldung aus
                #   Als Eingabe werden ganze Zahlen erwartet.
                try:
                    indices_of_qbits[i] = int(x)
                except ValueError:

                    #   Versuche das aktuelle Element x in Float zu konvertieren, sonst gebe eine Fehlermeldung aus
                    #   Als Eingabe werden ganze Zahlen für Indizes und Fließkommazahlen für Parameter von Gattern erwartet.
                    try:
                        indices_of_qbits[i] = float(x)
                    except ValueError:
                        raise argparse.ArgumentError(self, 'Value Error: {a!r} can\'t be converted to float, for index'
                                                           ' of the qubit an integer and for gate arguments float '
                                                           'was expected.'.format(a=x))

                #   Falls die Zahl negativ ist, wird ebenfalls ein Fehler ausgegeben
                if indices_of_qbits[0] < 0:
                    raise argparse.ArgumentError(self, 'Value Error: the index for a qubit must be positive: {a!r}'
                                                 .format(a=indices_of_qbits[i]))

            #   Fehlermelduung, wenn mehr Indizes eingegeben wurden
            if len(indices_of_qbits) != 1:
                raise argparse.ArgumentError(self, 'The number of arguments ({r!r}) does not match the required '
                                                   'number of this gate ({s!r}: 1).'
                                             .format(r=len(indices_of_qbits), s=gate))

        #   Gates that needs one index and one argument (gate change 1 Qubits and need 1 additional parameter):
        #   Tupel mit allen möglichen Parametern, die für Gatter stehen, welche auf zwei Qubits angewendet
        #   werden und daher zwei Index-Parameter benötigen.
        gates_2_arg = ('r_phi', 'hu')

        #   Falls das aktuelle Gatter in dieser Liste vorkommt, sollte es nur einen Index haben:
        if gate in gates_2_arg:

            #   Fehlermelduung, wenn mehr Indizes eingegeben wurden
            if len(indices_of_qbits) != 2:
                raise argparse.ArgumentError(self, 'The number of arguments ({r!r}) does not match the required '
                                                   'number of this gate ({s!r}: 2).'
                                             .format(r=len(indices_of_qbits), s=gate))

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


def cmd_line_parser(q_sim, cmd_in):
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

    #   im Argumlent_Objekt des Parser wird an der Stelle function 'qsim_obj.process_cli' gespeichert. Damit wird später
    #   der Funktionsaufruf args.function(args) zu qsim_obj.process_cli(args), wenn der Teilbefehl cli aufgerufen wurde.
    parser_from_cli.set_defaults(function=process_cli)

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

    #   im Argumlent_Objekt des Parser wird an der Stelle function 'qsim_obj.process_file' gespeichert. Damit wird
    #   später der Funktionsaufruf args.function(args) zu qsim_obj.process_file(args), wenn der Teilbefehl file
    #   aufgerufen wurde.
    parser_from_file.set_defaults(function=process_file)

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
    args = parser.parse_args(cmd_in)

    #   Je nach Teilbefehl wird in args.function ein bestimter Text gespeichert, der sich für die Teilbefehle
    #   unterscheidet. Für cli ist funcion = qsim_obj.process_cli, für file, qsim_obj.process_file. Somit werden je nach
    #   verwendetem Teilbefehl, verschiedene Funktionen aufgerufen.
    #   https://docs.python.org/3/library/argparse.html#sub-commands
    args.function(q_sim, args)

    #   5   Das Verboselevel, bzw quiet wird verarbeitet (die betreffenden Variablen gesetzt)
    if args.quiet:

        #   Quiet bedeutet Debug-Modus auf -1
        Base.set_verbose_level(-1)
    else:
        Base.set_verbose_level(args.verbose_level)

    #   Starte die Simulation
    q_sim.start_simulation()

    #   Entferne alle Gatter in der Liste aller Operationen, die ausgeführt werden sollen
    #   (auch wenn mehrere Befehle hintereinander ausgeführt werden und der Arbeitsspeicher mit clear nicht
    #   gelöscht werden soll, ist es sinnvoll, die bereits angenwndeten Gatter zu entfernen, damit sie nicht
    #   doppelt aufgerufen werden. Außerdem kann bei einem neuen Befehl die Anzahl an Qubits verringert werden,
    #   wodurch es zu einem Fehler kommt, wenn alte Gatter mit höheren Index noch in der Liste vorhanden sind.
    q_sim.operation_obj.list_tuple_operation_qubit_i = []

    #   Ausgabe der Zustände nach der Simulation, falls vebose level 0 (nicht quiet)
    if Base.get_verbose() >= 0:
        print('\n---------------\t Simulation completed: \t---------------\n')
    print(q_sim.qstate_obj)

    #   Die Liste aller Gatter und der Initialzustand wird gelöscht, die Anzahl der Qubits wird auf 0 gesetzt
    #   (Falls -c --clear im eingegebenen Befehl)
    if args.clear_mem:
        QuantumSimulation.clear_mem(q_sim)

    #   9   Sollen mehrere Befehle hintereinander ausgeführt werden, haben die Befehle das Argument --interactive_input.
    #       Wurde dieses Argument übergeben, gibt die Funktion cmd_line_parser() True zurück, ansonsten False
    #       Entsprechend wird diese Funktion in einer Schleife aufgerufen oder nicht.
    if args.interactive_input:
        return True

    return False


def process_cli(qsim_obj, args):
    """
    Diese Funktion wird vom Parsor aufgerufen, wenn der Teilbefehl cli aufgerufen wurde.
    Sie verarbeitet die Argumente, die mit dem Parser ausgelesen wurden, indem sie kleinere Funktionen
    aufruft.
    :param qsim_obj:
    :param args: Argumente aus dem Parsor des Teilbefehls cli.
    :return:
    """

    #   1: Setzte die Anzahl der Qubits
    qsim_obj.process_n_qubits(args.n_qubits)

    #   Falls eine Initialisierung der Qubits eingegeben wurde, wird im phi_in Vektor das entsprechende Element
    #   auf 0 oder 1 gesetzt.
    if args.arg_phi_in:
        for element in args.arg_phi_in:
            index, value = element

            #   2
            qsim_obj.initialize_qubits(index, value)

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
                qsim_obj.process_operation(operation[0], [])

            #   Ansonsten ist es ein Gatter mit mindestens einem Index
            else:
                #   Die Indizes, von denen das Gatter abhängig ist, sind in der Liste am Ende gespeichert
                list_affected_qubits = operation[1:]

                #   Das erste Element in der Liste bezeichnet das Gatter (m, h, z, x, ...)
                gate_in = operation[0]

                #   3
                #   process_operation() fügt die Operation der Liste aller Operationen hinzu
                qsim_obj.process_operation(gate_in, list_affected_qubits)


def process_file(q_sim, args):
    """
    Diese Funktion wird vom Parsor aufgerufen, wenn der Teilbefehl file aufgerufen wurde.
    Nachdem der erste Parsor aus der Datei die Argumente eingelesen hat, wird hier mit cmd_line_parser() der zweite
    Parsor aufgerufen, welcher die Argumente weiter verarbeitet.

    :param args: Argumente aus dem Parsor des Teilbefehls file.
    :return:
    """

    #   Der Parsor wird erneut aufgerufen, diesmal mit den Argumenten, die aus der Datei eingelesen wurden
    cmd_line_parser(q_sim, args.file)


if __name__ == '__main__':

    #   QuantumSimulation Objekt erstellen
    q_sim = QuantumSimulation()

    input_1 = []
    if len(sys.argv) <= 1:
        input_1 = input().split()
    else:
        input_1 = sys.argv[1:]

    #   Führe Simulation mit übergebenen Start-Parametern aus. Das Parsen, das Verabreiten der Eingabe, die Simulation
    #   und die bereinigung des Arbeitsspeichers erfolgt durch die Funktion q_sim.cmd_line_parser() der Klasse
    #   QuantumSimulation
    #
    #   Der Parser ist extra in der Funktion cmd_line_parser(), da er für eine Eingabe zweilmal aufgerufen
    #   werden soll, wenn Argumente aus einer Datei eingelesen werden sollen. Die Funktion gibt True oder False zurück,
    #   je nachdem, ob im Befehl mit --interactive_input das Ausführen von mehreren Befehlen hintereinander gefordert
    #   war, oder nicht.
    loop_for_cli = cmd_line_parser(q_sim, input_1)

    #   Gibt der Parser q_sim.cmd_line_parser() True zurück, wird auf eine neue Konsoleneingabe gewartet.
    #   Die Schleife ist solange aktiv, bis ein erneuter aufruf des Parsers in der Schleife False zurück gibt.
    while loop_for_cli:

        #   Speichere die neue Eingabe
        cmd_input = input().split()

        #   Parse den eingegebenen Befehl, verarbeite die eingegebenen Parameter.
        #   Speichere den zurückgegebenen Wert. split() zerlegt den eingegebenen Befehl in die Einzelnen Argumente
        #   pro Zeile. Es wird nach Leerzeichen getrennt.
        loop_for_cli = cmd_line_parser(q_sim, cmd_input)
