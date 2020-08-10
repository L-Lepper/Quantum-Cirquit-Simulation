
def getdiracnotation(index, n_qubits):
    """Wandelt Index in Bitmuster um. Benötigt Anzahl der Qubits für führende Nullen"""

    # global diracnotation

    #   Umwandlung von int in binärcode, Abschneiden der Information des Vorzeichenbits ( 0b / 1b )
    str_var = bin(index)[2:]

    diracnotation = '|' + (n_qubits - len(str_var)) * '0' + str_var + ')'

    return diracnotation



#               VORGEHENSWEISE 2

#   Speichern von den Zuständen, die im Zustandsvektor mit Einträgen ungleich 0 auftreten, in dem Array
#   possible_states (000, 001, 101, ...) Der Index entspricht aber immer noch dem Index des Zustandvektors
#   leere Einträge '' wenn Zustand nicht eintreten kann
#    for value in state_vector:
#        if value != 0. + 0.j:
#
#            if first_time:
#                str_var = bin(index)[2:]
#                str_var = '|' + (n_qubits - len(str_var)) * '0' + str_var + ')'
#
#                #   ToDo: Größe der Datentypen ist festgelegt
#                dt = np.dtype([('index', 'i4'), ('diracnotation', np.unicode, 20), ('value_s_vec', 'complex128')])
#                diracnotation = np.array([(index, str_var, value)], dt)
#
#                first_time = False
#            else:
#                str_var = bin(index)[2:]
#                str_var = '|' + (n_qubits - len(str_var)) * '0' + str_var + ')'
#                diracnotation = np.append(diracnotation, (index, str_var, value), 0)
#
#        index += 1
#
#    return diracnotation


#               VORGEHENSWEISE 1
#    i = 0
#    while i < state_obj.phi_vec.size:
#        #   Ist Eintrag im Zustandsvektor nicht 0, soll Dirac-Darstellung ermittelt werden |011)
#        if state_obj.phi_vec[i] != 0. + 0.j:
#
#            #   Es wird für q0, q1, ... geprüft, ob das Qubit 0 oder 1 ist (in diesem Zustand aus dem Zustandsvektor)
#            index_qubit = 0
#            while index_qubit < n_qubits:
#
#                #   Berechnung der Anzahl der möglichen Zustände aus den verbleibenden Qubits (einschließlich es betrachteten)
#                #   Die untere Hälfte hat q_i = 0, die obere Hälfte q_i = 1
#                if i < (pow(2, n_qubits - index_qubit) // 2):
#                    state_obj.possible_states[i] = np.char.add(state_obj.possible_states[i], ['0'])
#                else:
#                    state_obj.possible_states[i] = np.char.add(state_obj.possible_states[i], ['1'])
#                index_qubit += 1
#        i += 1
