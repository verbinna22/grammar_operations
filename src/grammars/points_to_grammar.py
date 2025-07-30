from typing import List, Set, Tuple
from grammars.definitions import Grammar, NonTerminal, Rule

def generate_points_to_grammar(number_of_assign: int) -> Tuple[Grammar, Set[str], Set[str]]:
    reduced_alphabet : Set[str] = set({
        "alloc", "assign", "assign_r", "ld_i", "st_i", "alloc_r", "st_r_i", "ld_r_i"
    })
    full_alphabet : Set[str] = reduced_alphabet.copy()
    PT : NonTerminal = NonTerminal("PT")
    Assign : NonTerminal = NonTerminal("Assign")
    Assign_r : NonTerminal = NonTerminal("Assign_r")
    ld_PT_FT_st_i : NonTerminal = NonTerminal("ld_PT_FT_st_i")
    ld_PT_i : NonTerminal = NonTerminal("ld_PT_i")
    FT_st_i : NonTerminal = NonTerminal("FT_st_i")
    FT : NonTerminal = NonTerminal("FT")
    st_r_PT_FT_ld_r_i : NonTerminal = NonTerminal("st_r_PT_FT_ld_r_i")
    st_r_PT_i : NonTerminal = NonTerminal("st_r_PT_i")
    FT_ld_r_i : NonTerminal = NonTerminal("FT_ld_r_i")
    non_terminals : Set[NonTerminal] = set({PT, Assign, Assign_r, ld_PT_FT_st_i, ld_PT_i, FT_st_i, FT, st_r_PT_FT_ld_r_i, st_r_PT_i, FT_ld_r_i})
    rules : List[Rule] = [
            Rule(PT, Assign, PT),
            Rule(PT, "alloc"),
            Rule(PT, ld_PT_FT_st_i, PT),
            Rule(Assign, "assign"),
            Rule(Assign_r, "assign_r"),
            Rule(ld_PT_FT_st_i, ld_PT_i, FT_st_i),
            Rule(ld_PT_i, "ld_i", PT),
            Rule(FT_st_i, FT, "st_i"),
            Rule(FT, "alloc_r"),
            Rule(FT, FT, st_r_PT_FT_ld_r_i),
            Rule(FT, FT, Assign_r),
            Rule(st_r_PT_FT_ld_r_i, st_r_PT_i, FT_ld_r_i),
            Rule(st_r_PT_i, "st_r_i", PT),
            Rule(FT_ld_r_i, FT, "ld_r_i"),
        ]
    for i in range(1, number_of_assign + 1):
        full_alphabet.add(f"assign_{i}_open")
        full_alphabet.add(f"assign_{i}_close")
        full_alphabet.add(f"assign_r_{i}_open")
        full_alphabet.add(f"assign_r_{i}_close")
        rules.append(Rule(Assign, f"assign_{i}_open"))
        rules.append(Rule(Assign, f"assign_{i}_close"))
        rules.append(Rule(Assign_r, f"assign_r_{i}_open"))
        rules.append(Rule(Assign_r, f"assign_r_{i}_close"))
    return (Grammar(alphabet=full_alphabet,
                    main_non_terminal=PT,
                    non_terminals=non_terminals,
                    rules = rules),
                full_alphabet, reduced_alphabet)
