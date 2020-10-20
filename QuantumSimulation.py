#   Projektarbeit Literaturrecherche zu Simulationsalgorithmen für Quantencomputing
#   Author: Lukas Lepper, 19.10.2020
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

    #   Funktion zum einlesen einer Datei. ToDo: Muss noch implementiert werden
    def read_input_from_file(self):
        pass

    #   Funktion nimmt nacheinander Befehler aus dem Consolenfenster entgegen und startet entsprechend die Simulation
    def cmd_input_for_qsim(self):
        """
        Diese Funktion nimmt mit hilfe einer Endlosschleife nacheinander neue Befehle an. Es wird zwischen Quanten-
        Befehlen q, Gattern g und sonstigen Befehlen c unterschieden. Ähnlich einem Switch Case wird für jeden Befehl
        eine andere Funktion ausgeführt, beginnend beim Initialzustand, über den Schaltungsaufbau und zur Simulation,
        bis zu Debug Funktionen.
        Befehle werden auf gültige Eingaben überprüft, wobei die Anzahl der Qubits entsprechend der Eingabe erweitert
        oder gekürzt wird, unter ausgabe einer Warnung.
        Mit dem Befehl help werden alle Befehle aufgelistet, die Eingabe wird in Kleinbuchstaben umgewandelt.
        :return:
        """

        #   Speichere die erste Eingabe
        cmd_input = input().lower()
        #   Erstelle eine leere Liste für den Ausganszustand aus den initialisierten Qubits
        phi_in = []

        while True:
            #   Gatter-Befehle
            if cmd_input[0] == 'g':

                #   Für Gatter, die eine Quantenschaltung aufbauen
                if cmd_input[1] == 'h' or cmd_input[1] == 'x' or cmd_input[1] == 'z' or cmd_input[1] == 'm':
                    # g| name:h,x,z,cx |(| Zahl 1, 10, 100 |)
                    # 0      1 bis n   n+1    n bis m      m+1      Index
                    i = cmd_input.find('(')
                    j = cmd_input.find(')')
                    gate_in = cmd_input[1:i]
                    qubit_to_change = int(cmd_input[i + 1:j])

                    if qubit_to_change >= Base.getnqubits():
                        print('\nWarnung!\n\tAnzahl der Qubits war', Base.getnqubits(), ', aber das Qubit mit Index',
                              qubit_to_change, 'liegt darüber.\n\tDie Anzahl an Qubits wurde auf', qubit_to_change + 1,
                              'geändert!\n')
                        Base.set_n_qubits(qubit_to_change + 1)
                        phi_in += (Base.getnqubits() - len(phi_in)) * '0'

                    #   Der Operationen-Liste wird über die Funktion aus dem Operation-Objekt ein Tupel aus Gatter und betreffendem
                    #   Qubit hinzugefügt.
                    self.operation_obj.add_tuple_to_operation_list([(gate_in, qubit_to_change)])

                else:
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
                        print('\nFehler!\n\tSyntaxfehler:', cmd_input, cmd_input[7:11], 'entweder true oder fals(e), erwartete Syntax: cdebug true vl = 3, cdebug = false\n')

                #   Befehle aus Datei auslesen und ausführen
                elif cmd_input[1:5] == 'file':
                    pass

                #   Aktuellen Initialzustand in Diracnotation ausgegben, z.B.: |10011)
                elif cmd_input[1:6] == 'print':

                    #   Ausgabestring erstellen
                    #   For-Schleife notwendig, da Liste in String gespeichert werden soll. Mit Strings konnte vorher
                    #   nicht gearbeitet werden, da z.B. bsp_str[2]='g' nicht funktioniert.
                    phi_str = "|"
                    for char in phi_in:
                        phi_str += char
                    phi_str += ")"

                    print('Der Initialzustand in Diracnotation lautet', phi_str, '.')

                #   Simulation ausführen, wenn Anzahl der Qubits größer 0 ist (Dann ist in phi_in auch ein Bitmuster
                #   in Form einer Liste gespeichert.
                elif cmd_input[1:9] == 'simulate':
                    if Base.getnqubits() > 0:

                        #   Das Bitmuster für den initialen Zustand, wird aus der Liste in eimen String gespeichert
                        phi_str = ""
                        for char in phi_in:
                            phi_str += char

                        #   Diese Funktion wandelt das Bitmuster 0011 in eine 3 um, und ruft dann die Funktion
                        #   init_vec_with_bitsequence(self, int_in) in QState auf, die den zugehörigen Vektor im
                        #   jeweiligen Objekt erzeugt
                        self.init_qbit_sequence_to_statevec(phi_str)

                        #   Nachdem die Simulation gestartet wurde, wird diese Schleife beendet (Aufruf der Berechnung
                        #   in der main.py)
                        break

                    else:
                        print('\nFehler!\n\tSimulation wurde nicht gestartet, die Anzahl der Qubits beträgt', Base.getnqubits(), '.\n')

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

                    #   Falls der neue Wert größer ist als der bisherige Wert für die Qubits, wird die neue Anzahl
                    #   gespeichert.
                    if n_qubits >= Base.getnqubits():
                        self.set_n_qubits(n_qubits)

                        #   In der Liste phi_in wird für jedes neue Qubit eine 0 hinzugefügt.
                        phi_in += (Base.getnqubits() - len(phi_in)) * '0'

                    #   Falls es bereits mehr Qubits gibt, als in dem Befehl vorgegeben, wird eine Warnung ausgegeben
                    #   und alle darüberliegenden Qubits gelöscht
                    else:
                        print('\nWarnung!\n\tAnzahl der Qubits war', Base.getnqubits(), ', aber sollte auf',
                              n_qubits, 'gesetzt werden.\n\tDie Anzahl an Qubits wurde auf', n_qubits,
                              'geändert und alle darüber liegenden Qubits wurden gelöscht!\n')
                        self.set_n_qubits(n_qubits)

                        #   Prüfen, dass Index wirklich weiter geht, als die neue Anzahl der Qubits
                        if len(phi_in) > n_qubits:
                            phi_in = phi_in[0:n_qubits]

                #   Initialisieren der Zustände der einzelnen Qubits (standardmäßig 0)
                elif cmd_input[0:3] == 'qb[':

                    #   Index finden, an dem der Index des Qubit gespeichert ist. Kann mehrere Stellen haben...
                    i = cmd_input.find('qb[') + 3
                    j = cmd_input.find(']')
                    index = int(cmd_input[i:j])

                    #   Falls der Index des zu initialisierenden Qubits aus dem Bereich der Anzahl an Qubits hinaus geht,
                    #   wird eine Warnung ausgegeben und die Anzahl angepasst.
                    if index >= Base.getnqubits():
                        print('\nWarnung!\n\tAnzahl der Qubits war', Base.getnqubits(), ', aber das Qubit mit Index',
                              index, 'liegt darüber.\n\tDie Anzahl an Qubits wurde auf', index + 1,
                              'geändert!\n')
                        Base.set_n_qubits(index + 1)

                    #   Der Liste der initialen Zustände der Qubits wird mit 0en für die neuen Qubits erweitert
                    phi_in += (Base.getnqubits() - len(phi_in)) * '0'

                    #   Index, andem der Initialzustand des betreffenden Qubits gespeichert ist
                    i = cmd_input.find('= ') + 2
                    value = cmd_input[i]

                    #   Falls der Zustand 0 oder 1 eingegeben wurde, wird dieser Wert in der Liste gespeichert
                    if value == '0' or value == '1':
                        phi_in[index] = value

                    #   Andernfalls liegt ein Syntaxfehler vor, es wird angenommen dass der Zustand 1 sein sollte und
                    #   es wird eine Warnung ausgegeben.
                    else:
                        print(
                            '\nFehler!\n\tQubits können nur mit 0 oder 1 initialisiert werden, statdessen wurde der Wert',
                            value, 'eingegeben.\nQubit mit Index', index, 'wird mit 1 initialisiert.\n')
                        phi_in[index] = '1'

                else:
                    print('\nFehler!\n\tUnbekannte Initialisierung:', cmd_input, '\n')

            #   Befehl für die Hilfe: Auflistung aller möglichen Befehler mit ihrer Syntax
            elif cmd_input[0] == '?' or cmd_input == 'help' or cmd_input == 'h':

                print('\n##################################################\n')
                print('Liste aller Befehle für das Programm QuantumSimulation:\n'
                      '\tBefehle für den Initialzustand. Standardmäßig haben Qubits den Zustand 0.\n'
                      '\tqb_n = x\t\tLegt Anzahl n der Qubits entsprechend der Eingabe x fest.\n'
                      '\tqb[i] = x\t\tInitialisierung des i-ten Qubits auf den Wert x, x = {0, 1}.\n'
                      '\n'
                      '\tBefehle, um der Liste an Operationen verschiedene Gatter hinzuzufügen, welche auf das i-te Qubit angewendet werden.\n'
                      '\tgx(i)\t\t\tPauli-X-Gatter.\n'
                      '\tgz(i)\t\t\tPauli-Z-Gatter.\n'
                      '\tgh(i)\t\t\tHadarmard-Gatter.\n'
                      '\tgm(i)\t\t\tMessung des i-ten Qubits.\n'
                      '\n'
                      '\tSonstige Befehle:\n'
                      '\tcdebug true|false vl = x\tDebug-Modus aktivieren oder deaktivieren. Beim aktivieren wird mit x das Verbose-Level 0-3 benötigt.\n'
                      '\tcfile PATH\t\t\t\tPATH gibt einen Dateipfad auf eine Textdatei an, aus der eine Liste an Befehlen eingelesen und ausgeführt werden soll.\n'
                      '\tcsimulate\t\t\t\tFalls die Anzahl an Qubits größer 0 ist, wird die Simulation gestartet.\n'
                      '\tcprint\t\t\t\t\tGibt den aktuellen Initialzustand in Diracnotation 0110 aus.\n')
                print('##################################################\n')

            else:
                print('\nFehler!\n\tUnbekannter Eingabetyp:', cmd_input, '. Tippe \'?\' oder \'help\' um alle Befehle aufgelistet zu bekommen.\n')

            #   Es wird auf eine neue Eingabe gewartet
            cmd_input = input().lower()

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
                print(self.qstate_obj)

                #   Bei der Messung wird anstatt der Multiplikation unten, die Funktion measure() aufgerufen.
                self.qstate_obj.general_matrix = self.qgate_obj.measure()

                # Index welches Tupel abgearbeitet wird, wird hochgezählt
                i += 1

                break

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

        return self.qstate_obj
