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
import numpy as np
import argparse
from CmdLineParser import ValidateGate
from CmdLineParser import ValidateInitialization
from CmdLineParser import CheckFilePath

class QuantumSimulation(Base):
    """
    In dieser Klasse sind die Hauptfunktionen des Programms definiert. Diese werden in der main Datei gesteuert. Die
    hier definierten Funktionen erstellen Objekte der anderen Klassen. Diese Klassen erben von übergeordneeten Klassen,
    sodass Objekte nur aus den Kind-Klassen benötigt werden.

    Funktionen sind das Einlesen der Eingabe, das Initialisieren des Zustandsvektors und das Durchführen der Berechnung.
    ToDo: Ausgabe kann hier in einer Funktion definiert werden, anstatt alleine in der Klasse QState.
    """

    def __init__(self):
        super().__init__()

        #   Erstellen von Objekten, die in dieser Klasse benötigt werden
        #   ToDo: Sollen alle Objekte direkt hier im Konsstruktor erstellt werden? Geht erstmal nicht da sie mit Werten
        #    initialisiert werden müssen. Eventuell sollte besser in vielen Klassen der Konstruktor überarbeitet werden.
        #    Schnell passiert, dass Funktion Fehler ausgibt, da Variable nicht initialisiert ist (None).
        self.qstate_obj = QState()
        self.operation_obj = Operation()

    #   Bitmuster kann als binäre Zahl in int umgewandelt werden, und wieder zurück. Vorgehen ist effizienter als
    #   String. Integer Zahl entspricht dann dem Index im Zustandsvektor, beginnend bei 0. Dadurch erfolgt leichtere
    #   Vektorzuordnung.
    #   Funktion erzeugt aus initialem Bitmuster im qstate_obj den zugehörigen Zustandsvektor
    def init_qbit_sequence_to_statevec(self, bit_seq_as_str):
        """
        Funktion erzeugt aus dem eingelesenen Initalzustand den zugehörigen Zustandsvektor im QState-Objekt, welches
        in dieser Klasse enthalten ist. Der Initalzustand wird als String aus 0en und 1en übergeben.

        :param bit_seq_as_int: Der String des Initialzustandes kann als binäre Zahl in eine Dezimalzahl umgewandelt
        werden. Diese entspricht genau dem Index des Zustandes im Zustandsvektor. Dieses Vorgehen ist effizienter als
        die Verwendung des Strings.
        :return: void.
        """

        bit_seq_as_int = int(bit_seq_as_str, 2)
        self.qstate_obj = self.qstate_obj.init_vec_with_bitsequence(bit_seq_as_int)

    def cmd_line_parser(self, phi_in, cmd_input):
        #   , usage=
        parser = argparse.ArgumentParser(prog='%(prog)s',
                                         description='Simulation of Quantum Algorithm',
                                         epilog='by Lukas Lepper')
        verbose_groupe = parser.add_mutually_exclusive_group()

        #   1
        parser.add_argument('--n_qubits', '-n',
                            dest='n_qubits',
                            action='store',
                            type=int,
                            default=Base.getnqubits(),
                            help='Set number of qubits. Initialize new qubits with 0 and delete old qubits and gates above it.')

        #   2
        parser.add_argument('--init_qubit', '-i',
                            dest='phi_in',
                            action=ValidateInitialization,
                            type=int,
                            nargs=2,
                            metavar=('INDEX', 'STATE'),
                            help='Initialize qubit i with j = {0|1}.'
                            )

        #   3
        parser.add_argument('--gate', '-g',
                            dest='list_of_gates',
                            action=ValidateGate,
                            nargs='+',
                            metavar=('GATE', 'INDEX_1'),
                            help='Gate and indices of the affected qubits.'
                            )

        #   4
        parser.add_argument('--file', '-f',
                            dest='file_path',
                            action=CheckFilePath,
                            help='Read command parameters from file.'
                            )

        #   5
        verbose_groupe.add_argument('--verbose', '-v',
                            dest='verbose_level',
                            action='count',
                            default=0,
                            help='Increase output verbosity.'
                            )

        #   6
        verbose_groupe.add_argument('--quiet', '-q',
                            dest='quiet',
                            action='store_true',
                            help='Print only results.')

        #   7 ToDo: In Liste der Operationen Speichern, sodass Zwischenergebnisse ausgegeben werden können
        # ToDo: Oder für jeden Parameter action implementeiren
        parser.add_argument('--print', '-p',
                            dest='to_print',
                            choices=['init_state', 'state_vec', 'gates'],
                            help='Print the initial state, the state vector or the list of gates')

        #   8
        parser.add_argument('--clear', '-c',
                            dest='clear_memory',
                            action='store_true',
                            help='Delete the number of qubits, the list of gates, ... in memory.')

        #   9
        parser.add_argument('--interactive_input',
                            action='store_true',
                            help='Enter parameters one by one.')

        args = parser.parse_args(cmd_input)



        # ---1
        #   Falls der neue Wert größer ist als der bisherige Wert für die Qubits, wird die neue Anzahl
        #   gespeichert.
        if args.n_qubits >= Base.getnqubits():
            self.set_n_qubits(args.n_qubits)

            #   In der Liste phi_in wird für jedes neue Qubit eine 0 hinzugefügt.
            phi_in += (Base.getnqubits() - len(phi_in)) * [0]

        #   Falls es bereits mehr Qubits gibt, als in dem Befehl vorgegeben, wird eine Warnung ausgegeben
        #   und alle darüberliegenden Qubits gelöscht
        else:
            print('\nWarnung!\n\tAnzahl der Qubits war', Base.getnqubits(), ', aber sollte auf',
                  args.n_qubits, 'gesetzt werden.\n\tDie Anzahl an Qubits wurde auf', args.n_qubits,
                  'geändert und alle darüber liegenden Qubits und deren Gatter wurden gelöscht!\n')
            self.set_n_qubits(args.n_qubits)

            #   Prüfen, dass Index wirklich weiter geht, als die neue Anzahl der Qubits
            if len(phi_in) > args.n_qubits:
                del phi_in[args.n_qubits:]

            #   Speichere die Indizes, an denen Operatoren gespeichert sind, die auf Qubits oberhalb von
            #   n_qubits angewendet werden
            list_of_index = []
            for index, tuple in enumerate(self.operation_obj.list_tuple_operation_qubit_i):
                if any(tuple):
                    if int(tuple[1]) >= args.n_qubits:
                        list_of_index += [index]

            #   Entferne alle Gatter in der Liste aller Operationen, die auf Qubits angewendet werden sollen,
            #   die eben gelöscht wurden
            self.operation_obj.list_tuple_operation_qubit_i = np.delete(
                self.operation_obj.list_tuple_operation_qubit_i,
                list_of_index, 0)
        # ---1

        if args.phi_in:
            for element in args.phi_in:
                index, value = element
                # ---2
                #   Falls der Index des zu initialisierenden Qubits aus dem Bereich der Anzahl an Qubits hinaus geht,
                #   wird eine Warnung ausgegeben und die Anzahl angepasst.
                if index >= Base.getnqubits():
                    print('\nWarnung!\n\tAnzahl der Qubits war', Base.getnqubits(), ', aber das Qubit mit Index',
                          index, 'liegt darüber.\n\tDie Anzahl an Qubits wurde auf', index + 1,
                          'geändert!\n')
                    Base.set_n_qubits(index + 1)

                #   Der Liste der initialen Zustände der Qubits wird mit 0en für die neuen Qubits erweitert
                phi_in += (Base.getnqubits() - len(phi_in)) * [0]
                # ---2

                #   Der Zustand wird in der Liste phi_in gespeichert
                # ---2
                phi_in[index] = value
        # ---2

        if args.list_of_gates:
            for gate in args.list_of_gates:
                qubit_to_change = gate[1]  # ToDo: Mehrere Qubits in einem Gatter
                gate_in = gate[0]
                # ---3
                #   Falls die Anzahl der Qubits kleiner ist, als der Index des Qubits welches initialisiert wird, wird
                #   eine Warnung ausgegeben und die Anzahl angepasst. Die restlichen neuen Qubits haben den Zustand 0.
                if qubit_to_change >= Base.getnqubits():
                    print('\nWarnung!\n\tAnzahl der Qubits war', Base.getnqubits(), ', aber das Qubit mit Index',
                          qubit_to_change, 'liegt darüber.\n\tDie Anzahl an Qubits wurde auf', qubit_to_change + 1,
                          'geändert!\n')
                    Base.set_n_qubits(qubit_to_change + 1)
                    phi_in += (Base.getnqubits() - len(phi_in)) * [0]

                #   Der Operationen-Liste wird über die Funktion aus dem Operation-Objekt ein Tupel aus Gatter und
                #   betreffendem Qubit hinzugefügt.
                self.operation_obj.add_tuple_to_operation_list([(gate_in, qubit_to_change)])
        # ---3

        #---5
        if args.quiet:
            Base.disable_debug()
        else:
            Base.enable_debug(args.verbose_level)

        ###########

# ---sim
            if Base.getnqubits() > 0:

                #   Das Bitmuster für den initialen Zustand, wird aus der Liste in einem String gespeichert
                phi_str = ""
                for value in phi_in:
                    phi_str += str(value)

                #   Diese Funktion wandelt das Bitmuster 0011 in eine 3 um, und ruft dann die Funktion
                #   init_vec_with_bitsequence(self, int_in) in QState auf, die den zugehörigen Vektor im
                #   jeweiligen Objekt erzeugt
                self.init_qbit_sequence_to_statevec(phi_str)

                #   Führe Berechnung der eingelesenen Eingabe durch
                self.qstate_obj = self.calculate()

            else:
                print('\nFehler!\n\tSimulation wurde nicht gestartet, die Anzahl der Qubits beträgt',
                      Base.getnqubits(), '.\n')
    # ---sim

        ##########

        if args.to_print == 'gates':
        # ---7

            print('Liste der gespeicherten Gatter:')

            #   Falls in der Liste der Operationen Elemente vorhanden sind:
            if np.size(
                    self.operation_obj.list_tuple_operation_qubit_i) > 0:  # ToDo Operation List mit Listen, nicht Numpy. 2 ist hier jetzt notwendig, da gelöschte Liste so aussieht: [['', '']]
                print('\tGatter\t| Index der Qubits, auf die das Gatter angewendet wird')

                for operation in self.operation_obj.list_tuple_operation_qubit_i:
                    str_out = '\t\t' + operation[0] + '\t|\t' + operation[1]
                    print(str_out)
            else:
                print('Die Liste ist leer.')
    # ---7

        #   Aktuellen Initialzustand in Diracnotation ausgegben, z.B.: |10011)
        elif args.to_print == 'init_state':
# ---7
            #   Ausgabestring erstellen
            #   For-Schleife notwendig, da Liste in String gespeichert werden soll. Mit Strings konnte vorher
            #   nicht gearbeitet werden, da z.B. bsp_str[2]='g' nicht funktioniert.
            phi_str = "|"
            for value in phi_in:
                phi_str += str(value)
            phi_str += ")"

            print('Der Initialzustand in Diracnotation lautet', phi_str, '.')
# ---7
        elif args.to_print == 'state_vec':
            pass

#---9
        if args.interactive_input:
            while True:

                if self.execute_cmd(phi_in, cmd_input):
                    break

                #   Es wird auf eine neue Eingabe gewartet
                cmd_input = input().lower()

        if args.clear_memory:
            del args
# ---8
            #   Entferne alle Gatter in der Liste aller Operationen, die ausgeführt werden sollen
            self.operation_obj.list_tuple_operation_qubit_i = np.array([[]])

            #   Setze die Anzahl der Qubits auf 0
            self.set_n_qubits(0)

            #   Lösche die Initialisierung aller Qubits
            del phi_in[:]
# ---8


        #print(phi_in, Base.getnqubits(), str(args.list_of_gates), self.operation_obj.list_tuple_operation_qubit_i)
        return False


    #   Funktion nimmt nacheinander Befehler aus dem Konsolenfenster entgegen und startet entsprechend die Simulation
    #   Einlesen von Befehlen aus Datei erfolgt über Befehl mit Dateipfad in der Konsole
    def cmd_input_for_qsim(self):
        """
        Diese Funktion nimmt mit hilfe einer Endlosschleife nacheinander neue Befehle an. Es wird zwischen Quanten-
        Befehlen q, Gattern g und sonstigen Befehlen c unterschieden. Sie ruft die Funktion execute_cmd auf, in der
        ähnlich wie bei einem Switch Case für jeden Befehl eine andere Funktion ausgeführt wird. (Initialzustand setzen,
        Schaltungsaufbau einlesen, Simulation starten, Debug-Modus einstellen, ...) Befehle werden auf gültige Eingaben
        überprüft, wobei die Anzahl der Qubits entsprechend der Eingabe erweitert oder gekürzt wird, unter aussenden
        einer Warnung. Das Einlesen einer Datei erfolgt mit Hilfe eines Befehls mit Dateipfad (zb. cfile """
        #      "C:\Users\NAME\Documents\test.txt") <-- ACHTUNG! Pfad erzeugt unicode error, wenn er innerhalb
        #      von """...""" steht! Im Code muss er in der Form r"C:\Users\NAME\Documents\test.txt" angegeben werden!
        #      https://stackoverflow.com/questions/1347791/unicode-error-unicodeescape-codec-cant-decode-bytes-cannot-open-text-file
        """ 
        Mit dem Befehl help werden alle Befehle aufgelistet, die Eingabe wird in Kleinbuchstaben umgewandelt.
        :return:
        """
        #   Speichere die erste Eingabe
        cmd_input = input().lower()
        #   Erstelle eine leere Liste für den Ausganszustand aus den initialisierten Qubits
        phi_in = []

        #   Solange die Funktion execute_cmd() Fals zurück gibt, wird immer auf eine neue Konsoleneingabe gewartet.
        #   Der Befehl cend beendet das Programm, die Funktion gibt False zurück und die Schleife wird beendet.
        while True:
            if self.cmd_line_parser(phi_in, cmd_input.split()):
                break

#            if self.execute_cmd(phi_in, cmd_input):
 #               break

            #   Es wird auf eine neue Eingabe gewartet
            cmd_input = input().lower()

    def execute_cmd(self, phi_in, cmd_input):
        """
        Diese Funktion führt die Befehle aus. Entweder wurden die Befehle aus dem Kommandofenster über die Funktion
        cmd_input_for_qsim() eingegeben, oder der Befehl cfile "PATH" liefert die eingelesenen Befehle aus einer Datei.

        :param phi_in: Speichert die Initialzustände der verwendeten Qubits. Diese Liste wird übergeben, damit auch
        nach einem rekursiven Funktionsaufruf diese Information auserhalb einer Stufe verfügbar ist.
        ToDo: phi_in global speichern, anstatt Parameter übergeben (phi_in als Liste wirkt als Pointer)
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
                    qubit_to_change = int(cmd_input[i + 1:j])

#---3
                    #   Falls die Anzahl der Qubits kleiner ist, als der Index des Qubits welches initialisiert wird, wird
                    #   eine Warnung ausgegeben und die Anzahl angepasst. Die restlichen neuen Qubits haben den Zustand 0.
                    if qubit_to_change >= Base.getnqubits():
                        print('\nWarnung!\n\tAnzahl der Qubits war', Base.getnqubits(), ', aber das Qubit mit Index',
                              qubit_to_change, 'liegt darüber.\n\tDie Anzahl an Qubits wurde auf', qubit_to_change + 1,
                              'geändert!\n')
                        Base.set_n_qubits(qubit_to_change + 1)
                        phi_in += (Base.getnqubits() - len(phi_in)) * [0]

                    #   Der Operationen-Liste wird über die Funktion aus dem Operation-Objekt ein Tupel aus Gatter und
                    #   betreffendem Qubit hinzugefügt.
                    self.operation_obj.add_tuple_to_operation_list([(gate_in, qubit_to_change)])
#---3

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

                    Base.enable_debug(value)

                #   Debug-Modus deaktivieren
                elif cmd_input[7:12] == 'false':
                    Base.disable_debug()
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

#---4
                #   file_obj erstellen, um zu prüfen, ob angegebene Datei existiert
                file_obj = Path(file_name)
                if file_obj.is_file():

                    #   Lese die gesammte Datei, Zeile für Zeile ein, und Speichere sie in einer Liste
                    list_of_cmds = open(file_name).readlines()

                    #   Führe die eingelesenen Befehle nacheinander aus. Falls der Befehl cend dabei war, gibt die
                    #   Funktion execute_cmd True zurück und das Programm wird beendet.
                    for cmd in list_of_cmds:
                        #   rstrip() entfernt Leerzeichen und Zeilenumbrüche am Ende eines Strings
                        if self.execute_cmd(phi_in, cmd.rstrip()):
                            return True

                #   Falls die angegebene Datei nicht existiert:
                else:
#---4
                    print('\nFehler!\n\tFolgende Datei wurde nicht gefunden:', file_name, '\n')

            #   Ausgabe bestimmter Parameter, wie der eingegebene Initialzustand oder die Liste der Gatter
            #   (cprint = gates|states)
            elif cmd_input[1:6] == 'print':

                #   Suche Index, wo Parameter des Befehls gespeichert sind
                index = cmd_input.find('= ') + 2

                #   Liste der gespeicherten Operationen ausgeben
                if cmd_input[index:index + 5] == 'gates':
# ---7
                    print('Liste der gespeicherten Gatter:')

                    #   Falls in der Liste der Operationen Elemente vorhanden sind:
                    if np.size(self.operation_obj.list_tuple_operation_qubit_i) > 0:    #   ToDo Operation List mit Listen, nicht Numpy. 2 ist hier jetzt notwendig, da gelöschte Liste so aussieht: [['', '']]
                        print('\tGatter | Index der Qubits, auf die das Gatter angewendet wird')

                        for operation in self.operation_obj.list_tuple_operation_qubit_i:
                            str_out = '\t\tg' + operation[0] + ' | ' + operation[1]
                            print(str_out)
                    else:
                        print('Die Liste ist leer.')
# ---7

                #   Aktuellen Initialzustand in Diracnotation ausgegben, z.B.: |10011)
                elif cmd_input[index:index + 5] == 'state':
# ---7
                    #   Ausgabestring erstellen
                    #   For-Schleife notwendig, da Liste in String gespeichert werden soll. Mit Strings konnte vorher
                    #   nicht gearbeitet werden, da z.B. bsp_str[2]='g' nicht funktioniert.
                    phi_str = "|"
                    for value in phi_in:
                        phi_str += str(value)
                    phi_str += ")"

                    print('Der Initialzustand in Diracnotation lautet', phi_str, '.')
# ---7
                else:
                    print('\nFehler!\n\tUnbekannte Syntax:', cmd_input, '. Eingabe in der Form: cprint = state|gates erwartet.\n')

            #   Simulation ausführen, wenn Anzahl der Qubits größer 0 ist (Dann ist in phi_in auch ein Bitmuster
            #   in Form einer Liste gespeichert.
            elif cmd_input[1:9] == 'simulate':
#---sim
                if Base.getnqubits() > 0:

                    #   Das Bitmuster für den initialen Zustand, wird aus der Liste in einem String gespeichert
                    phi_str = ""
                    for value in phi_in:
                        phi_str += str(value)

                    #   Diese Funktion wandelt das Bitmuster 0011 in eine 3 um, und ruft dann die Funktion
                    #   init_vec_with_bitsequence(self, int_in) in QState auf, die den zugehörigen Vektor im
                    #   jeweiligen Objekt erzeugt
                    self.init_qbit_sequence_to_statevec(phi_str)

                    #   Führe Berechnung der eingelesenen Eingabe durch
                    self.qstate_obj = self.calculate()

                else:
                    print('\nFehler!\n\tSimulation wurde nicht gestartet, die Anzahl der Qubits beträgt',
                          Base.getnqubits(), '.\n')
# ---sim

            #   Zurücksetzen der Simulationsparameter
            elif cmd_input[1:6] == 'clear':
#---8
                #   Entferne alle Gatter in der Liste aller Operationen, die ausgeführt werden sollen
                self.operation_obj.list_tuple_operation_qubit_i = np.array([[]])

                #   Setze die Anzahl der Qubits auf 0
                self.set_n_qubits(0)

                #   Lösche die Initialisierung aller Qubits
                del phi_in[:]
# ---8

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
#---1
                #   Falls der neue Wert größer ist als der bisherige Wert für die Qubits, wird die neue Anzahl
                #   gespeichert.
                if n_qubits >= Base.getnqubits():
                    self.set_n_qubits(n_qubits)

                    #   In der Liste phi_in wird für jedes neue Qubit eine 0 hinzugefügt.
                    phi_in += (Base.getnqubits() - len(phi_in)) * [0]

                #   Falls es bereits mehr Qubits gibt, als in dem Befehl vorgegeben, wird eine Warnung ausgegeben
                #   und alle darüberliegenden Qubits gelöscht
                else:
                    print('\nWarnung!\n\tAnzahl der Qubits war', Base.getnqubits(), ', aber sollte auf',
                          n_qubits, 'gesetzt werden.\n\tDie Anzahl an Qubits wurde auf', n_qubits,
                          'geändert und alle darüber liegenden Qubits und deren Gatter wurden gelöscht!\n')
                    self.set_n_qubits(n_qubits)

                    #   Prüfen, dass Index wirklich weiter geht, als die neue Anzahl der Qubits
                    if len(phi_in) > n_qubits:
                        del phi_in[n_qubits:]

                    #   Speichere die Indizes, an denen Operatoren gespeichert sind, die auf Qubits oberhalb von
                    #   n_qubits angewendet werden
                    list_of_index = []
                    for index, tuple in enumerate(self.operation_obj.list_tuple_operation_qubit_i):
                        if int(tuple[1]) >= n_qubits:
                            list_of_index += [index]

                    #   Entferne alle Gatter in der Liste aller Operationen, die auf Qubits angewendet werden sollen,
                    #   die eben gelöscht wurden
                    self.operation_obj.list_tuple_operation_qubit_i = np.delete(self.operation_obj.list_tuple_operation_qubit_i, list_of_index, 0)
#---1

            #   Initialisieren der Zustände der einzelnen Qubits (standardmäßig 0)
            elif cmd_input[0:3] == 'qb[':

                #   Index finden, an dem der Index des Qubit gespeichert ist. Kann mehrere Stellen haben...
                i = cmd_input.find('qb[') + 3
                j = cmd_input.find(']')
                index = int(cmd_input[i:j])

#---2
                #   Falls der Index des zu initialisierenden Qubits aus dem Bereich der Anzahl an Qubits hinaus geht,
                #   wird eine Warnung ausgegeben und die Anzahl angepasst.
                if index >= Base.getnqubits():
                    print('\nWarnung!\n\tAnzahl der Qubits war', Base.getnqubits(), ', aber das Qubit mit Index',
                          index, 'liegt darüber.\n\tDie Anzahl an Qubits wurde auf', index + 1,
                          'geändert!\n')
                    Base.set_n_qubits(index + 1)

                #   Der Liste der initialen Zustände der Qubits wird mit 0en für die neuen Qubits erweitert
                phi_in += (Base.getnqubits() - len(phi_in)) * [0]
#---2

                #   Index, andem der Initialzustand des betreffenden Qubits gespeichert ist
                i = cmd_input.find('= ') + 2
                value = int(cmd_input[i])

                #   Falls der Zustand 0 oder 1 eingegeben wurde, wird dieser Wert in der Liste gespeichert
                if value == 0 or value == 1:
#---2
                    phi_in[index] = value
#---2

                #   Andernfalls liegt ein Syntaxfehler vor, es wird angenommen dass der Zustand 1 sein sollte und
                #   es wird eine Warnung ausgegeben.
                else:
                    print('\nFehler!\n\tQubits können nur mit 0 oder 1 initialisiert werden, statdessen wurde der Wert',
                          value, 'eingegeben.\nQubit mit Index', index, 'wird mit 1 initialisiert.\n')
                    phi_in[index] = 1

            else:
                print('\nFehler!\n\tUnbekannte Initialisierung:', cmd_input, '\n')

        #   Befehl für die Hilfe: Auflistung aller möglichen Befehler mit ihrer Syntax
        elif cmd_input[0] == '?' or cmd_input == 'help' or cmd_input == 'h':

            print('\n##################################################\n')
            print('Liste aller Befehle für das Programm QuantumSimulation:\n'
                  '\tBefehle für den Initialzustand. Standardmäßig haben Qubits den Zustand 0.\n'
                  '\tqb_n = x\t\tLegt Anzahl n der Qubits entsprechend der Eingabe x fest.\n'
                  '\tqb[i] = x\t\tInitialisierung des i-ten Qubits auf den Wert x, x = {0, 1}.\n')
            print('\tBefehle, um der Liste an Operationen verschiedene Gatter hinzuzufügen, welche auf das i-te Qubit angewendet werden.\n'
                  '\tgx(i)\t\t\tPauli-X-Gatter.\n'
                  '\tgz(i)\t\t\tPauli-Z-Gatter.\n'
                  '\tgh(i)\t\t\tHadarmard-Gatter.\n'
                  '\tgm(i)\t\t\tMessung des i-ten Qubits.\n')
            print('\tSonstige Befehle:\n'
                  '\tcdebug true|false vl = x Debug-Modus aktivieren oder deaktivieren. Beim aktivieren wird mit x das Verbose-Level 0-3 benötigt.\n'
                  '\tcfile "PATH"\t\t\tPATH gibt einen Dateipfad auf eine Textdatei an, aus der eine Liste an Befehlen eingelesen und ausgeführt werden soll. Z.b. cfile', r' "C:\Users\NAME\Documents\test.txt"', '\n'
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

    def calculate(self):
        """
        Funktion führt Operationen aus der Operation_List aus. Elemente dieser Liste werden abgearbeitet:
        Erstellt Objekt für Operation, und führt Multiplikation aus.
        ToDo: Anderer Operator wenn Messung durchgeführt werden soll
        :return qstate_obj: Mit Ergebnis als Zustandsvektor.
        """

        #   Index in der operation_list
        i = 0

        #   Führe nacheinander die Operationen aus operation_obj.list_tuple_operation_qubit_i
        for operation in self.operation_obj.list_tuple_operation_qubit_i[:, 0]:

            #   ToDo: Hier gibt es einen Fehler: Eigentlich soll Operationsliste das qubit to change als int speichern,
            #    wird aber irgendwie als numpy_str verwandelt. Desswegen ist hier konvertierung in int notwendig
            #   In der Liste wird aus dem Tuple mit dem aktuellen Index i, das zweite Element (Index des Qubit,
            #   welches verändert werden soll) ausgelesen
            qubit_to_change = int(self.operation_obj.list_tuple_operation_qubit_i[i, 1])

            #   Erzeugen des benötigten Objekt für das Gatter (Gatter werden durch Konstruktor automatisch auf richtige
            #   Größe erweitert.
            if operation == 'x':
                self.qgate_obj = PauliX(qubit_to_change)
            elif operation == 'z':
                self.qgate_obj = PauliZ(qubit_to_change)
            elif operation == 'h':
                self.qgate_obj = HadamardH(qubit_to_change)
            elif operation == 'm':
                self.qgate_obj = Measurement(self.qstate_obj.general_matrix, qubit_to_change)

                #   gebe Zustände des Zustandsvektors vor der Messung aus
                    # ----------
                if Base.get_debug()[0]:
                    print('\nZustände des Zustandsvektors vor der Messung:\n', self.qstate_obj)
                    # ----------

                #   Bei der Messung wird anstatt der Multiplikation unten, die Funktion measure() aufgerufen.
                self.qstate_obj.general_matrix = self.qgate_obj.measure()

                #   gebe Zustände des Zustandsvektors nach der Messung aus
                    # ----------
                if Base.get_debug()[0]:
                    print('\nZustände des Zustandsvektors nach der Messung:\n', self.qstate_obj)
                    # ----------

                # Index welches Tupel abgearbeitet wird, wird hochgezählt
                i += 1

                continue

            #   Fehler: Operation wird als gültige Eingabe erkannt, ist oben aber nicht aufgeführt
            else:
                print('\nFehler!\n\tFolgende Operation wurde in QuantumSimulation.py: cmd_input_for_qsim() nicht als '
                      'Falsch erkannt, aber ist in QuantumSimulation.py: calculate() nicht implementiert:', operation,
                      '\n')
                return self.qstate_obj

            #   Multiplikation führt Simulation aus: Neuer Zustandsvektor nachdem Gatter angewendet wurde
            #   (Messung wird ebenfalls durch den Operator __mul__() aufgerufen)
            self.qstate_obj = self.qgate_obj * self.qstate_obj

            # Index welches Tupel abgearbeitet wird, wird hochgezählt
            i += 1

        print(self.qstate_obj)
        return self.qstate_obj
