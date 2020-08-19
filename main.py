#   Projektarbeit Literaturrecherge zu Simulationsalgorithmen für Quantencomputing
#   Author: Lukas Lepper, 19.08.2020
#   Betreuer: Martin Hardieck
#   Dateiname: main.py
#   Version: 0.2

# import numpy as np
from QuantumSimulation import QuantumSim
from QGate import QGate
from QState import QState

#   Hinweis, was das Programm berechnet. ToDo: An aktuelle Funktionen anpassen
print('Simulation für kleine Anzahl an Qubit. Wähle den Zustand (z.B. 0001011), mit dem Dieses initialisiert werden '
      'soll, und welche Operation angewendet werden soll {X,Z,H}. Die Operation wird auf das erste Qubit angewendet.\n')

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

#   Speichere Anzahl der Qubits in der Elternklasse, von der alle Objekte diese Information erben
QuantumSim.setnqubits(n_qubits)

#   Auswahl des Gatters
gate_in = input('Quantengatter:\t\t').lower()

#   Prüfe gültige Eingabe
while (gate_in != 'x') and (gate_in != 'z') and (gate_in != 'h'):
    print('Ungültige Eingabe. x/X oder z/Z oder h/H erwartet.\n')
    gate_in = input('Quantengatter:\t\t').lower()

#   Qubit auswählen, auf welches das Gatter ausgeführt wird
qubittochange = int(input('Auf welches Qubit soll dieses Quantengatter ausgeführt werden? (Index [0, n-1]):\t\t'))

#   Prüfe gültige Eingabe
while (qubittochange < 0) or (qubittochange >= QuantumSim.getnqubits()):
    print('Ungültige Eingabe. Index muss im Bereich [ 0, ', QuantumSim.getnqubits() - 1, '] liegen.\n')
    qubittochange = int(input('Index des Qubits:\t\t'))

#   Speichere den Index des Qubits, auf welches das Gatter angewendet wird, in der übergeordneten Klasse
QuantumSim.setqubittochange(qubittochange)

#   U-Matrix des Gatters auf Größe der Schaltung erweitern (BigGate=Gatter, welches die gesammte Schaltung beschreibt)
biggate = QGate(gate_in)
biggate.u_matrix = QGate.expandmatrix(biggate, QuantumSim.getnqubits(), QuantumSim.getqubittochange())

#   Objekt für Quantengatter erstellen (enthält Informationen zu Gatterart (Typ) und Matrix U)
# current_gate = QGate(gate_in)

#   Zustandvektor erstellen (Anstatt 0 oder Dirac-Notation |0) erfolgt eine Zuordnung des Zustandsvektors (1, 0) )
current_state = QState(phi_in)

#   Matrix auf Anzahl der Qubits vergrößern ToDo: Variables Qubit verändern
# current_gate.u_matrix = np.kron(current_gate.u_matrix, np.eye(pow(2, n_qubits - 1)))

#   Simulation ausführen (Matrixmultiplikation)
QGate.__mul__(biggate, current_state)
# QGate.__mul__(current_gate, current_state)
# current_state = current_gate * current_state       ToDo: Multiplikation in Elternklasse

#   Ausgabe der Simulation: Für jeden Eintrag des Zustandsvektors, der ungleich 0 ist, wird das Ergebnis ausgegeben.
print(current_state)


# i = 0
# while i < pow(2, n_qubits):
#    if current_state.possible_states[i, 0] != '':
#        sys.stdout.write('\nDer Zustand |')
#
#        for j in range(n_qubits):
#            sys.stdout.write(current_state.possible_states[i, j])
#
#        sys.stdout.write('), mit dem Eintrag im Zustandsvektor von ')
#        sys.stdout.write(np.str(current_state.phi_vec[i]))
#        sys.stdout.write(', hat die Wahrscheinlichkeit ')
#        sys.stdout.write(str(pow(abs(current_state.phi_vec[i]), 2)))
#
#    i += 1


# for element in current_state.diracnotation:
#    print('\n\nZustand: ', element[1], ', Wahrscheinlichkeit: ', pow(abs(element[2]), 2))
# print('\n\nZustand: ', element)
