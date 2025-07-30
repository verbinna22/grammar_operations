from typing import List, Set
from automatones.definitions import Automaton
from grammars.definitions import Grammar, NonTerminal, Rule

cnt : int = 1

def intersect(grammar: Grammar, dfa: Automaton) -> Grammar:
    global cnt
    artifitial_non_terminal : NonTerminal = NonTerminal("intersect_" + str(grammar.main_non_terminal))
    non_terminals : Set[NonTerminal] = set({artifitial_non_terminal})
    rules : List[Rule] = []
    for rule in grammar.rules:
        for q1 in dfa.states:
            for q2 in dfa.states:
                if cnt % 1000 == 0: #####
                    print(cnt, len(rules)) #####
                cnt += 1 #####
                left_non_terminal : NonTerminal = NonTerminal(str(q1) + "_" + str(q2) + "_" + str(rule.non_terminal))
                non_terminals.add(left_non_terminal)
                if len(rule.right_part) == 0:
                    rules.append(Rule(left_non_terminal))
                elif len(rule.right_part) == 1:
                    if isinstance(rule.right_part[0], str):
                        if dfa.transitions[q1][rule.right_part[0]] == q2:
                            rules.append(Rule(left_non_terminal, rule.right_part[0]))
                        else:
                            rules.append(Rule(left_non_terminal))
                    else:
                        right_non_terminal : NonTerminal = NonTerminal(str(q1) + "_" + str(q2) + "_" + str(rule.right_part[0]))
                        rules.append(Rule(left_non_terminal, right_non_terminal))
                elif len(rule.right_part) == 2:
                    if isinstance(rule.right_part[0], str):
                        q_k = dfa.transitions[q1][rule.right_part[0]]
                        if isinstance(rule.right_part[1], str):
                            if dfa.transitions[q_k][rule.right_part[1]] == q2:
                                rules.append(Rule(left_non_terminal,
                                                rule.right_part[0], rule.right_part[1]))
                            else:
                                rules.append(Rule(left_non_terminal))
                        else:
                            right_non_terminal : NonTerminal = NonTerminal(str(q_k) + "_" + str(q2) + "_" + str(rule.right_part[1]))
                            rules.append(Rule(left_non_terminal, rule.right_part[0], right_non_terminal))
                    else:
                        for q_k in dfa.states:
                            right_non_terminal_1 : NonTerminal = NonTerminal(str(q1) + "_" + str(q_k) + "_" + str(rule.right_part[0]))
                            right_non_terminal_2 : NonTerminal = NonTerminal(str(q_k) + "_" + str(q2) + "_" + str(rule.right_part[1]))
                            rules.append(Rule(left_non_terminal, right_non_terminal_1, right_non_terminal_2))
    for qf in dfa.accept_states:
        rules.append(Rule(artifitial_non_terminal, NonTerminal(f"{dfa.initial_state}_{qf}_{grammar.main_non_terminal}")))
    return Grammar(alphabet=grammar.alphabet,
                    main_non_terminal=artifitial_non_terminal,
                    non_terminals=non_terminals,
                    rules=rules
                    )