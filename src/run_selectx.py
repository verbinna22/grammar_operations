from datetime import datetime
from os import system
from pathlib import Path

FOLDER_WITH_GRAPHS : str = "/mnt/data/MyOwnFolder/learning/p_algo/pointers/graphs"
FOLDER_WITH_SELECTX : str = "/mnt/data/MyOwnFolder/learning/p_algo/SelectX/SelectX"

def main() -> None:
    graphs = Path(FOLDER_WITH_GRAPHS)
    for graph in graphs.iterdir():
        # if ord(graph.name[0]) >= ord('j') or graph.name == "com_fasterxml_jackson":
        #     continue
        print(graph)
        selectx_folder = Path(FOLDER_WITH_SELECTX)
        with open(selectx_folder / "graphs.txt", mode="w", encoding="utf-8") as file:
            file.write(f"{graph / f'{graph.name}.g'} {graph / 'vertex_mappings.txt'} {graph / 'slx_result.txt'}")
        initial_time = datetime.now()
        command : str = fr'''
        /bin/bash -c "\
        cd {FOLDER_WITH_SELECTX} && ./gradlew run"
        '''
        system(command)
        with open(graph / "time_to_preanalyse.txt", mode='w', encoding='utf-8') as file:
            file.write(f"{datetime.now() - initial_time}\n")

if __name__ == "__main__":
    main()