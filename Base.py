#   Projektarbeit Literaturrecherche zu Simulationsalgorithmen für Quantencomputing
#   Author: Lukas Lepper, 25.08.2020
#   Betreuer: Martin Hardieck
#   Dateiname: Base.py
#   Version: 0.3


class Base:
    """
    Basisklasse, von der alle anderen Klassen direkt oder indirekt erben. Somit können alle Objekte auf die hier
    gespeicherte Anzahl der Qubits zugreifen.
    """

    #   Private Attribute: Zugriff über Funktion / Klassenmethode.
    __nqubits = 0
    #   Ist das Verbose-Level 0, ist der Debug-Modus deaktiviert
    __debug_verbose_level = 0

    #   Die Genauigkeiten hängen von der Genauigkeit der Eingegebenen Parameter oder im Fall der zum Test benutzten
    #   Zustandsvektoren, auch von der Anzahl an Nachkommastellen der Zahlen im verwendeten Zustandsvektor ab
    #   (Bei 16 Stellen, wurde auf 13 Stellen gerundet, um das Entscheidungsidagramm wie erwartet zusammen zu fassen.)
    #   ToDo Genauigkeit

    #   Genauigkeit der Ausgabe
    #   (Parameter der Gatter sollten mit einer etwas höherer Genauigkeit eingegeben worden sein)
    __accuracy = 4
    #   Wortbreite, beim Vergleichen von Werten in den Kanten/Knoten: Beim Zusammenfassen des Entscheidungsdiagramms
    #   in Schritt 7, Welche Zahlen werden noch als gleich angesehen?
    __compare_decimal_places = 6
    #   Wortbreite, mit der eine Kanteneigenschaft bei der Messung als 0 angesehen wird
    __dd_zero_decimal_places = 13
    #   Wortbreite, mit der ein Zustand im Zustandsvektor als 0 angesehen wird
    __vec_zero_decimal_places = 13

    def __init__(self):
        pass

    #   get Anzahl der Qubits
    @staticmethod
    def getnqubits():
        return Base.__nqubits

    #   set Anzahl der Qubits
    @staticmethod
    def set_n_qubits(n_qubits):
        Base.__nqubits = n_qubits

    #   Aktiviere Verbose-Level
    @staticmethod
    def set_verbose_level(verbose_level):
        Base.__debug_verbose_level = verbose_level

    #   Deaktiviere Verbose-Level
    @staticmethod
    def reset_verbose_level():
        Base.__debug_verbose_level = 0

    #   get Verbose-Level
    @staticmethod
    def get_verbose():
        return Base.__debug_verbose_level

    #   Lege die Genauigkeit für die eingegebenen Parameter und die Ausgabe der Wahrscheinlichkeiten fest
    @staticmethod
    def set_accuracy(accuracy):
        Base.__accuracy = accuracy

    #   get Genauigkeit
    @staticmethod
    def get_accuracy():
        return Base.__accuracy


    #   get compare_decimal_places
    @staticmethod
    def get_compare_decimal_places():
        return Base.__compare_decimal_places

    #   get compare_decimal_places
    @staticmethod
    def get_dd_zero_decimal_places():
        return Base.__dd_zero_decimal_places

    #   get compare_decimal_places
    @staticmethod
    def get_vec_zero_decimal_places():
        return Base.__vec_zero_decimal_places
