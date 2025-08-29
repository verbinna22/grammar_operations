from datetime import datetime
from os import system
from pathlib import Path

FOLDER_WITH_GRAPHS : str = "/mnt/data/MyOwnFolder/learning/p_algo/pointers/graphs"
FOLDER_WITH_BUILDER : str = "/mnt/data/MyOwnFolder/learning/p_algo/grammar_operations_cpp/build"
TIME_LIMIT : int  = 3600

def main() -> None:
    graphs = Path(FOLDER_WITH_GRAPHS)
    for graph in graphs.iterdir():
        # if ord(graph.name[0]) >= ord('j') or graph.name == "com_fasterxml_jackson":
        #     continue
        print(graph)
        initial_time = datetime.now()
        command : str = fr'''
        /bin/bash -c "\
        cd {FOLDER_WITH_BUILDER} && ./grammarOperations \
            {graph / "slx_result.txt.ctxn"} \
            {graph / 'grammar.cfg'} "\
        '''
        # print(command)
        system(command)
        with open(graph / "time_to_generate_grammar.txt", mode='w', encoding='utf-8') as file:
            file.write(f"{datetime.now() - initial_time}\n")
        # break ##

if __name__ == "__main__":
    main()