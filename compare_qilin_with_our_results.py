from typing import Dict, Set, Tuple

ENCODING = 'utf-8'

def parse_qilin_function_name(rest: str):
    corner_count = 0
    flag = False
    for i in range(len(rest)):
        if rest[i] == '<':
            corner_count += 1
            flag = True
        elif rest[i] == '>':
            corner_count -= 1
        if corner_count == 0:
            break
    function_name = rest[:i + 1] # type: ignore
    function_name_pretty = function_name[1:-1]
    class_name, f_name = function_name_pretty.split(': ', maxsplit=2)
    real_f_name, _ = f_name.split("(", maxsplit=2) # split args
    corner_count = 0
    flag = False
    for i in range(len(real_f_name) - 1, -1, -1):
        if rest[i] == '>':
            corner_count += 1
            flag = True
        elif rest[i] == '<':
            corner_count -= 1
        if corner_count == 0 and flag:
            break
    if real_f_name[i - 1] == ' ': # type: ignore
        name_without_type = real_f_name[i:] # type: ignore
    else:
        name_without_type = real_f_name[:i] # type: ignore
    return class_name, name_without_type

def parse_qilin_file(filename: str) -> Set[Tuple[Tuple[str, str], Tuple[str, str]]]:
    label_to_data: Dict[str, Tuple[str, str]] = dict()
    with open(filename, encoding=ENCODING) as file:
        lines = file.readlines()
    ignored_types: Set[str] = set()
    variable_names: Set[str] = set()
    result: Set[Tuple[Tuple[str, str], Tuple[str, str]]] = set()
    for line in lines:
        if line.startswith('['):
            label, line_without_braces = line.split(']', maxsplit=2)
            label = label[1:]
            node_type, line_rest = line_without_braces.split(' ', maxsplit=2)
            if node_type == "ContextVarNode":
                _, line_rest = line_rest.split(' ', maxsplit=2) # remove unused digit
                line_rest = line_rest[1:-1] # remove braces
                node_type, line_rest = line_rest.split(' ', maxsplit=2)
            if node_type == "ContextAllocNode":
                _, line_rest = line_rest.split(' ', maxsplit=2) # remove unused digit
                line_rest = line_rest[1:-1] # remove braces
                node_type, line_rest = line_rest.split(' ', maxsplit=2)
            if node_type == "LocalVarNode":
                _, line_rest = line_rest.split(' ', maxsplit=2) # remove unused digit
                variable_name, line_rest = line_rest.split(' ', maxsplit=2)
                if variable_name in set({"virtualinvoke", "staticinvoke", "dynamicinvoke"}):
                    continue
                if variable_name.startswith('$'):
                    continue
                if variable_name == "Parm":
                    index, line_rest = line_rest.split(' ', maxsplit=2)
                    class_name, name_without_type = parse_qilin_function_name(line_rest)
                    label_to_data[label] = (index, f"{class_name}:{name_without_type}")
                    continue
                variable_names.add(variable_name)
                if line_rest.startswith('='):
                    _, _, line_rest = line_rest.split(' ', maxsplit=3)
                    corner_count = 0
                    flag = False
                    for i in range(len(line_rest)):
                        if line_rest[i] == '<':
                            corner_count += 1
                            flag = True
                        elif line_rest[i] == '>':
                            corner_count -= 1
                        if corner_count == 0 and flag:
                            break
                    line_rest = line_rest[i + 1:] # type: ignore
                    line_rest = line_rest.strip()
                class_name, name_without_type = parse_qilin_function_name(line_rest)
                label_to_data[label] = (variable_name, f"{class_name}:{name_without_type}")
            elif node_type == "AllocNode":
                _, line_rest = line_rest.split(' ', maxsplit=2) # remove unused digit
                _, line_rest = line_rest.split(' ', maxsplit=2) # remove unused new keyword
                t, f = line_rest.split(" in method ", maxsplit=2)
                class_name, name_without_type = parse_qilin_function_name(f)
                label_to_data[label] = (t, f"{class_name}:{name_without_type}")
            else:
                ignored_types.add(line_rest)
    for line in lines:
        if line.startswith('['):
            break
        variable_label, pointers = line.split(" -> ", maxsplit=2)
        pointers = pointers[1:-1]
        pointers_labels = pointers.split(' ')
        if variable_label not in label_to_data:
            continue
        variable = label_to_data[variable_label]
        for pointer_label in pointers_labels:
            if pointer_label in label_to_data:
                pointer = label_to_data[pointer_label]
                result.add((variable, pointer))
    return result

def main():
    pass

if __name__ == "__main__":
    main()
