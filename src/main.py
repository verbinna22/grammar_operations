from datetime import datetime
from pathlib import Path
from automatones.definitions import Automaton
from automatones.one_k_stack_automatone import generate_stack_automaton
from grammars.definitions import Grammar
from grammars.grammar_with_dfa_intersection import intersect
from grammars.points_to_grammar import generate_points_to_grammar
from grammars.text_io import write_grammar

FOLDER_WITH_GRAPHS : str = "/mnt/data/MyOwnFolder/learning/p_algo/pointers/graphs"

def main() -> None:
    graphs = Path(FOLDER_WITH_GRAPHS)
    for graph in graphs.iterdir():
        initial_time = datetime.now()
        print(graph)
        if ord(graph.name[0]) < ord('j'):
            continue
        with open(graph / "contexts_numbers.txt", encoding="utf-8") as file:
            context_numbers : int = int(file.readline())
        grammar, alphabet, reduced_alphabet = generate_points_to_grammar(context_numbers)
        # automaton : Automaton = generate_stack_automaton(context_numbers, reduced_alphabet, alphabet)
        # new_grammar : Grammar = intersect(grammar, automaton)
        write_grammar(str(graph / "grammar.cfg"), grammar)
        with open(graph / "time_to_generate_grammar.txt", mode='w', encoding='utf-8') as file:
            file.write(f"{datetime.now() - initial_time}\n")
        # break ##

if __name__ == "__main__":
    main()