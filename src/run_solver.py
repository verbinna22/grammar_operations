from datetime import datetime
from os import system
from pathlib import Path

FOLDER_WITH_GRAPHS : str = "/mnt/data/MyOwnFolder/learning/p_algo/pointers/graphs"
FOLDER_WITH_SOLVER : str = "/mnt/data/MyOwnFolder/learning/p_algo/CFPQ_PyAlgo"
TIME_LIMIT : int  = 8 * 3600

def main() -> None:
    graphs = Path(FOLDER_WITH_GRAPHS)
    for graph in graphs.iterdir():
        print(graph)
        if ord(graph.name[0]) >= ord('j'):
            continue
        initial_time = datetime.now()
        command : str = fr'''
        /bin/bash -c "\
        cd {FOLDER_WITH_SOLVER} && source ./venv/bin/activate && python3 -m cfpq_cli.run_all_pairs_cflr \
            IncrementalAllPairsCFLReachabilityMatrix \
            {graph / f'{graph.name}.g'} \
            {graph / 'grammar.cfg'} \
            --time-limit {TIME_LIMIT} \
            --out {graph / 'results.txt'}"
        '''
        system(command)
        with open(graph / "time_to_solve_grammar.txt", mode='w', encoding='utf-8') as file:
            file.write(f"{datetime.now() - initial_time}\n")

if __name__ == "__main__":
    main()