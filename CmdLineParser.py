#   Projektarbeit Literaturrecherche zu Simulationsalgorithmen für Quantencomputing
#   Author: Lukas Lepper, 19.10.2020
#   Betreuer: Martin Hardieck
#   Dateiname: DDEdge.py
#   Version: 0.5


from Base import Base
import argparse


class ValidateInitialization(argparse.Action, Base):
    def __call__(self, parser, namespace, values, option_string=None):
        # print '{n} {v} {o}'.format(n=namespace, v=values, o=option_string)
        valid_states = (0, 1)
        index, state = values
        if state not in valid_states:
            raise argparse.ArgumentError(self, 'Invalid state for initializing the qubit with index {r!r}: {s!r}'.format(r=index, s=state))

        items = getattr(namespace, self.dest, None)
        if items:
            items.append(values)
        else:
            items = [values]

        setattr(namespace, self.dest, items)

class ValidateGate(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        #print('{n} {v} {o}'.format(n=namespace, v=values, o=option_string))

        if len(values) <= 1:
            raise argparse.ArgumentError(self, 'Missing values for --gate GATE INDEX ...INDEX')

        valid_gates = ('x', 'h', 'z', 'm')
        gate = values[0]
        indices_of_qbits = values[1:]

        if gate not in valid_gates:
            raise argparse.ArgumentError(self, 'Invalid gate: {s!r}'.format(s=gate))

        for i, x in enumerate(indices_of_qbits):
            try:
                indices_of_qbits[i] = int(x)
            except ValueError:
                raise argparse.ArgumentError(self, 'Value Error: {a!r} can\'t be converted to integer, '
                                                   'for index of the qubit an integer was expected.'.format(a=x))
            if indices_of_qbits[i] < 0:
                raise argparse.ArgumentError(self, 'Value Error: the index must be positive: {a!r}'
                                             .format(a=indices_of_qbits[i]))

        #   Gates that change 1 qubit:
        gates_1_qb = ('x', 'h', 'z', 'm')
        if gate in gates_1_qb:
            if len(indices_of_qbits) != 1:
                raise argparse.ArgumentError(self, 'The number of indices ({r!r}) does not match the required '
                                                   'number of this gate ({s!r}: 1).'
                                             .format(r=len(indices_of_qbits), s=gate))

        #   Gates that change 2 qubits:
        #gates_2_qb = ('cx')

        new_item = [gate] + indices_of_qbits

        items = getattr(namespace, self.dest, None)
        if items:
            items.append(new_item)
        else:
            items = [new_item]

        setattr(namespace, self.dest, items)

class CheckFilePath(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):

        with open(values) as file:

            # ---4
            #   Lese die gesammte Datei, Zeile für Zeile ein, und Speichere sie in einer Liste
            list_of_cmds = file.readlines()
            # ---4

            args_list_from_file = []
            #   Führe die eingelesenen Befehle nacheinander aus. Falls der Befehl cend dabei war, gibt die
            #   Funktion execute_cmd True zurück und das Programm wird beendet.
            for cmd in list_of_cmds:
                #   rstrip() entfernt Leerzeichen und Zeilenumbrüche am Ende eines Strings
                #   split() trennt String nach den Leerzeichen --> Aus Parameter mit Argumenten pro Zeile / Element in
                #   der Liste wird Liste mit neuen Elementen für jedes Argument
                args_list_from_file += cmd.rstrip().split()

            parser.parse_args(args_list_from_file, namespace)

        # ---4
        setattr(namespace, self.dest, values)
