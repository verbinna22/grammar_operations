from typing import Dict, Set
from automatones.definitions import Automaton, State

def generate_stack_automaton(
        number_of_assign: int,
        reduced_alphabet: Set[str],
        full_alphabet: Set[str]) -> Automaton:
    q0 : State = State("q0")
    qf : State = State("qf")
    qd : State = State("qd")
    states: Set[State] = set({q0, qf, qd})
    transitions: Dict[State, Dict[str, State]] = dict()
    transitions[q0] = dict()
    transitions[qf] = dict()
    transitions[qd] = dict()
    for letter in full_alphabet:
        transitions[qf][letter] = qf
        transitions[qd][letter] = qd
    for letter in reduced_alphabet:
        transitions[q0][letter] = q0
    for i in range(number_of_assign):
        q_i : State = State(f"q_{i}")
        states.add(q_i)
        transitions[q_i] = dict()
        for letter in full_alphabet:
            transitions[q_i][letter] = q_i
        transitions[q0][f"assign_{i + 1}_open"] = q_i
        transitions[q0][f"assign_r_{i + 1}_open"] = q_i
        transitions[q0][f"assign_{i + 1}_close"] = qd
        transitions[q0][f"assign_r_{i + 1}_close"] = qd
        transitions[q_i][f"assign_{i + 1}_close"] = q0
        transitions[q_i][f"assign_r_{i + 1}_close"] = q0
        for j in range(number_of_assign):
            transitions[q_i][f"assign_{j + 1}_open"] = qf
            transitions[q_i][f"assign_r_{j + 1}_open"] = qf
            if j != i:
                transitions[q_i][f"assign_{j + 1}_close"] = qd
                transitions[q_i][f"assign_r_{j + 1}_close"] = qd
    return Automaton(
        alphabet=full_alphabet,
        initial_state=q0,
        states=states,
        transitions=transitions,
        accept_states=set({q0, qf}))