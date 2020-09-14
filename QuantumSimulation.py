#   Projektarbeit Literaturrecherche zu Simulationsalgorithmen für Quantencomputing
#   Author: Lukas Lepper, 14.09.2020
#   Betreuer: Martin Hardieck
#   Dateiname: DDEdge.py
#   Version: 0.4


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

    #   Funktion gibt Anweisungen in Konsole aus, und fragt nach Initialzustand, Quantengatter und Qubit,
    #   auf welches das Gatter angewendet werden soll.
    def read_input_from_cmd(self):
        """
        Funktion ließt eingabe über Konsole ein. Abgefragt wird Initialzustand, Quantengatter und betreffendes Qubit.
        ToDO: Eingabe als Kommando, mehrere Gatter hintereinander

        :return: void. Funktion speichert Eingabe selber in verschiedenen Objekten:
        1. QuantumSimulation: n_qubits
        2. QuantumSimulation: Funktion die den Zustandsvektor aus dem Initalzustand erstellt
            (speichert Ergebnis in self.qstate_obj)
        3. Operation: Funktion die der Liste der Operationen ein Tupel aus Gatter und Qubit_to_Change hinzufügt
        ToDo: Eventuell in einer Funktion Eingabe richtig abspeichern
        """

        #   Hinweis, was das Programm berechnet. ToDo: An aktuelle Funktionen anpassen
        print('Simulation für kleine Anzahl an Qubit. Wähle den Zustand (z.B. 0001011), mit dem Dieses initialisiert '
              'werden soll, und welche Operation angewendet werden soll {X,Z,H}. Die Operation wird auf das erste '
              'Qubit angewendet.\n')

        #   Eingabe des Schaltungsaufbaus
        #   Initialzustand (Basiszustand) - in der Form 0010110
        phi_in = input('Eingangszustand:\t')

        #   Prüfe gültige Eingabe, solange bis gültige Bitfolge eingetragen ist. Deren Länge gibt Anzahl der Qubits an.
        check_input = True
        n_qubits = 0
        while check_input:
            for x in phi_in:
                if (x == '0') or (x == '1'):
                    #   Zähle Anzahl der Qubits
                    n_qubits += 1

                else:
                    print('Ungültige Eingabe. Nur 0en oder 1en erwartet.')
                    phi_in = input('Eingangszustand:\t')
                    break

            check_input = False

        #   Speichere Anzahl der Qubits global in der Klasse QuantumSimulation, sodass alle Objekte auf diese
        #   Information zugreifen können, mit get_n_qubits
        self.set_n_qubits(n_qubits)

        #   Weise dem Initialzustand im QState-Objekt durch Funktionsaufruf init_qbit_sequence() den zugehörigen
        #   Basisvektor zu.
        #   Bitmuster als binäre Zahl, kann in int konvertiert werden --> entspricht dem Index im Zustandsvektor.
        #   (str aus 00101... als int zur Basis 2 wird konvertiert in int zur basis 10.
        phi_in = int(phi_in, 2)
        self.init_qbit_sequence_to_statevec(phi_in)

        #   Auswahl des Gatters
        gate_in = input('Quantengatter:\t\t').lower()

        #   Prüfe gültige Eingabe
        while (gate_in != 'x') and (gate_in != 'z') and (gate_in != 'h') and (gate_in != 'm'):
            print('Ungültige Eingabe. x/X oder z/Z oder h/H oder m/M erwartet.\n')
            gate_in = input('Quantengatter:\t\t').lower()

        #   Qubit auswählen, auf welches das Gatter ausgeführt wird
        qubit_to_change = int(input('Auf welches Qubit soll dieses Quantengatter ausgeführt werden? '
                                    '(Index [0, n-1]):\t\t'))

        #   Prüfe gültige Eingabe (ungültig wenn kleiner 0 oder größer gleich Anzahl der Qubits: Index des Vektors!)
        while (qubit_to_change < 0) or (qubit_to_change >= QuantumSimulation.getnqubits()):
            print('Ungültige Eingabe. Index muss im Bereich [ 0, ', QuantumSimulation.getnqubits() - 1, '] liegen.\n')
            qubit_to_change = int(input('Index des Qubits:\t\t'))

        #   Der Operationen-Liste wird über die Funktion aus dem Operation-Objekt ein Tupel aus Gatter und betreffendem
        #   Qubit hinzugefügt.
        self.operation_obj.add_tuple_to_operation_list([(gate_in, qubit_to_change)])

    #   Bitmuster kann als binäre Zahl in int umgewandelt werden, und wieder zurück. Vorgehen ist effizienter als
    #   String. Integer Zahl entspricht dann dem Index im Zustandsvektor, beginnend bei 0. Dadurch erfolgt leichtere
    #   Vektorzuordnung.
    #   Funktion erzeugt aus initialem Bitmuster im qstate_obj den zugehörigen Zustandsvektor
    def init_qbit_sequence_to_statevec(self, bit_seq_as_int):
        """
        Funktion erzeugt aus dem eingelesenen Initalzustand den zugehörigen Zustandsvektor im QState-Objekt, welches
        in dieser Klasse enthalten ist.

        :param bit_seq_as_int: Der Initialzustand kann als binäre Zahl in eine Dezimalzahl umgewandelt werden. Diese
        entspricht genau dem Index des Zustandes im Zustandsvektor. Dieses Vorgehen ist effizienter als die Verwendung
        des Strings 001101.
        :return: void.
        ToDo: Funktion hier ist unnötig, kann in einer Zeile wie unten aufgerufen werden
        """
        self.qstate_obj = self.qstate_obj.init_vec_with_bitsequence(bit_seq_as_int)

    #   Funktion zum einlesen einer Datei. ToDo: Muss noch implementiert werden
    @staticmethod
    def read_input_from_file():
        """
        Funktion zum Einlesen der Eingabe aus Dtei.
        :return:
        """
        print('nicht implementiert')
        pass

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
            #   Größe erweitert.  ToDo: Objekt für Messung
            if operation == 'x':
                self.qgate_obj = PauliX(qubit_to_change)
            elif operation == 'z':
                self.qgate_obj = PauliZ(qubit_to_change)
            elif operation == 'h':
                self.qgate_obj = HadamardH(qubit_to_change)
            elif operation == 'm':
                self.qgate_obj = Measurement(self.qstate_obj.general_matrix, qubit_to_change)

                # Index welches Tupel abgearbeitet wird, wird hcohgezählt
                i += 1

                break

            else:
                print('Diese Operation (Gatter oder Messung) wurde noch nicht implementiert:', operation)
                return -1

            #   Multiplikation führt Simulation aus: Neuer Zustandsvektor nachdem Gatter angewendet wurde
            self.qstate_obj = self.qgate_obj * self.qstate_obj

            # Index welches Tupel abgearbeitet wird, wird hcohgezählt
            i += 1

        return self.qstate_obj
