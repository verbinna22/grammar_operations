
from pathlib import Path
from typing import Dict, Set

FOLDER_WITH_GRAPHS : str = "/mnt/data/MyOwnFolder/learning/p_algo/pointers/graphs"

def main():
    graphs = Path(FOLDER_WITH_GRAPHS)
    for graph in graphs.iterdir():
        print(graph)
        number_to_type: Dict[int, str] = dict()
        number_to_var: Dict[int, str] = dict()
        with open(graph / "vertex_mappings.txt", encoding='utf-8') as file:
            for line in file.readlines():
                number, vertex = line.split(": ", maxsplit=2)
                number = int(number)
                if vertex.startswith("PtAllocVertex"):
                    # print(vertex) #
                    vertex = vertex.removeprefix("PtAllocVertex(")[:-2]
                    posttype = vertex.split(", type=")[1]
                    typeinfo = posttype.split(", lineNumber=")[0]
                    number_to_type[number] = typeinfo
                else:
                    number_to_var[number] = vertex[:-1]
        name_to_types : Dict[str, Set[str]] = dict()
        with open(graph / "results.txt", encoding='utf-8') as file:
            for line in file.readlines():
                var_id, obj_id = line.split("\t")
                var_id = int(var_id)
                obj_id = int(obj_id)
                if var_id == 0:
                    continue
                var_name = number_to_var[var_id]
                if var_name not in name_to_types:
                    name_to_types[var_name] = set()
                # print(var_id, obj_id) ##
                name_to_types[var_name].add(number_to_type[obj_id])
        with open(graph / 'type_analysis_results.txt', mode='w', encoding='utf-8') as file:
            for var_name, types in name_to_types.items():
                file.write(f"{var_name}")
                for t in types:
                    file.write(f"\t{t}")
                file.write("\n")

if __name__ == "__main__":
    main()
