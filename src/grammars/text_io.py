from typing import List, Set
from grammars.definitions import Grammar, NonTerminal, Rule

def read_grammar(file_name: str) -> Grammar:
    with open(file_name, encoding='utf-8') as file:
        lines: list[str] = file.readlines()
    lines : List[str] = list(filter(lambda line: len(line) > 0, lines))
    if len(lines) < 2:
        raise ValueError("Error. Invalid file!")
    if lines[-2] != "Count:":
        raise ValueError("Error. Invalid file!")
    main_non_terminal: NonTerminal = NonTerminal(lines[-1])
    non_terminals: Set[NonTerminal] = set([main_non_terminal])
    lines = lines[:-2]
    prerules : List[List[str]] = []
    for line in lines:
        symbols: List[str] = line.split()
        if len(symbols) < 1 or len(symbols) > 3:
            raise ValueError("Error. Invalid file!")
        prerules.append(symbols)
        non_terminals.add(NonTerminal(symbols[0]))
    rules: List[Rule] = []
    alphabet: Set[str] = set()
    for prerule in prerules:
        right_part : List[str | NonTerminal] = []
        for symbol in prerule[1:]:
            non_terminal = NonTerminal(symbol)
            if non_terminal in non_terminals:
                right_part.append(non_terminal)
            else:
                right_part.append(symbol)
                alphabet.add(symbol)
        rules.append(Rule(NonTerminal(prerule[0]), *right_part))
    return Grammar(alphabet, main_non_terminal, non_terminals, rules)


def write_grammar(file_name: str, grammar: Grammar) -> None:
    with open(file_name, encoding='utf-8', mode="w") as file:
        for rule in grammar.rules:
            file.write(f"{rule.non_terminal}")
            for symbol in rule.right_part:
                file.write(f"\t{symbol}")
            file.write("\n")
        file.write(f"Count:\n{grammar.main_non_terminal}\n")
