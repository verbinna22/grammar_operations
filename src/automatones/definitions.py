from copy import deepcopy
from typing import Any, Dict, Self, Set

class State:
    __name: str

    def __init__(self: Self, name: str) -> None:
        self.__name = name

    def __str__(self: Self) -> str:
        return self.__name

    def __hash__(self: Self) -> int:
        return hash(self.__name)

    def __eq__(self: Self, other: Any) -> bool:
        return (
            self.__class__ == other.__class__ and
            self.__name == str(other)
        )

    @property
    def name(self: Self) -> str:
        return self.__name

class Automaton:
    __alphabet: Set[str]
    __initial_state: State
    __states: Set[State]
    __transitions: Dict[State, Dict[str, State]]
    __accept_states: Set[State]

    def __init__(self: Self, alphabet: Set[str], initial_state: State, states: Set[State], transitions: Dict[State, Dict[str, State]], accept_states: Set[State]) -> None:
        if initial_state not in states:
            raise ValueError("Error. Initial state must be state!")
        for state in accept_states:
            if state not in states:
                raise ValueError(f"Error. Accept state {state} must be state!")
        for (state, string_to_state_dict) in transitions.items():
            if state not in states:
                raise ValueError(f"Error. Accept state {state} must be state!")
            if len(string_to_state_dict) != len(alphabet):
                raise ValueError("Error. Some transitions were not defined!")
            for (_, finish_state) in string_to_state_dict.items():
                if finish_state not in states:
                    raise ValueError(f"Error. Accept state {finish_state} must be state!")
        self.__alphabet = alphabet
        self.__initial_state = initial_state
        self.__states = states
        self.__transitions = transitions
        self.__accept_states = accept_states

    @property
    def alphabet(self: Self) -> Set[str]:
        return set(self.__alphabet)

    @property
    def initial_state(self: Self) -> State:
        return self.__initial_state

    @property
    def states(self: Self) -> Set[State]:
        return set(self.__states)

    @property
    def transitions(self: Self) -> Dict[State, Dict[str, State]]:
        return deepcopy(self.__transitions)

    @property
    def accept_states(self: Self) -> Set[State]:
        return set(self.__accept_states)
