from typing import Any, List, Self, Set

class NonTerminal:
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


class Rule:
    __non_terminal: NonTerminal
    __right_part: List[NonTerminal | str]

    def __init__(self: Self, non_terminal: NonTerminal, *args: NonTerminal | str) -> None:
        if len(args) > 2:
            raise ValueError("Error. len(args) > 2")
        self.__non_terminal = non_terminal
        self.__right_part = list(args)

    @property
    def non_terminal(self: Self) -> NonTerminal:
        return self.__non_terminal

    @property
    def right_part(self: Self) -> List[NonTerminal | str]:
        return self.__right_part[:]


class Grammar:
    __alphabet: Set[str]
    __main_non_terminal: NonTerminal
    __non_terminals: Set[NonTerminal]
    __rules: List[Rule]

    def __init__(self: Self, alphabet: Set[str], main_non_terminal: NonTerminal, non_terminals: Set[NonTerminal], rules: List[Rule]) -> None:
        if main_non_terminal not in non_terminals:
            raise ValueError("Error. Main non terminal not in non_terminals")
        self.__alphabet = alphabet
        self.__main_non_terminal = main_non_terminal
        self.__non_terminals = non_terminals
        self.__rules = rules

    @property
    def alphabet(self: Self) -> Set[str]:
        return set(self.__alphabet)

    @property
    def main_non_terminal(self: Self) -> NonTerminal:
        return self.__main_non_terminal

    @property
    def non_terminals(self: Self) -> Set[NonTerminal]:
        return self.__non_terminals.copy()

    @property
    def rules(self: Self) -> List[Rule]:
        return self.__rules[:]
