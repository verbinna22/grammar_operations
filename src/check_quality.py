
from pathlib import Path
from re import split
from typing import Dict, List, Set, Tuple


FOLDER_WITH_GRAPHS : str = "/mnt/data/MyOwnFolder/learning/p_algo/pointers/graphs"
FOLDER_WITH_BENCHMARKS : str = "/mnt/data/MyOwnFolder/learning/p_algo/pointers_example/src"

class AllocationInfo:
    alloc_id: int
    may_alias: List[str]
    not_may_alias: List[str]
    must_alias: List[str]
    not_must_alias: List[str]

class Allocation:
    path: str
    name: str
    function_name : str
    dictionary: List[AllocationInfo]

class Variable:
    path: str
    name: str
    line_number: int
    position: int | None
    function_name: str | None
    
    def is_arg(self) -> bool:
        return self.position is not None

def transform_to_list(value: str) -> List[str]:
    assert value[0] == "[" and value[-1] == "]"
    value = value[1:-1]
    if len(value) == 0:
        return []
    return value.split(",")

def transform_str_to_allocation_info(stri: str) -> AllocationInfo:
    result = AllocationInfo()
    # print(stri) #
    assert stri[-1] == '}'
    stri = stri[:-1]
    pairs = [cp.split(":") for cp in stri.split(", ")]
    for pair in pairs:
        if pair[0] == "allocId":
            result.alloc_id = int(pair[1])
        elif pair[0] == "mayAlias":
            result.may_alias = transform_to_list(pair[1])
        elif pair[0] == "mustAlias":
            result.must_alias = transform_to_list(pair[1])
        elif pair[0] == "notMayAlias":
            result.not_may_alias = transform_to_list(pair[1])
        elif pair[0] == "notMustAlias":
            result.not_must_alias = transform_to_list(pair[1])
        else:
            assert False
    return result

def main() -> None:
    graphs = Path(FOLDER_WITH_GRAPHS)
    benchmarks = Path(FOLDER_WITH_BENCHMARKS)
    for graph in graphs.iterdir():
        if ord(graph.name[0]) >= ord('j'):
            continue
        print(graph)
        benchmark = (benchmarks / graph.name).glob('**/*.java',)
        allocations: List[Allocation] = []
        location_to_name_to_variables: Dict[str, Dict[str, Variable]] = {}
        for filename in benchmark:
            with open(filename, encoding='utf-8') as file:
                code = file.read()
                line_number = 1
                location = f"{graph.name}.{filename.name.removesuffix(".java")}"
                location_to_name_to_variables[location] = dict()
                print(location) ##
                alloc_id_to_line : Dict[int, int] = dict()
                word = ""
                mode = "Benchmark find"
                number = 0
                allocation: Allocation = Allocation()
                
                for symbol in code:
                    if symbol == '\n':
                        line_number += 1

                    # print(mode, symbol) #
                    if mode == "Benchmark find":
                        if symbol == 'B':
                            word = 'B'
                            mode = "Benchmark found"
                    elif mode == "Benchmark found":
                        if symbol in [' ', '\t', '\n', '\r']:
                            if word != "Benchmark":
                                word = ""
                                mode = "Benchmark find"
                        elif symbol == '.':
                            if word == "Benchmark":
                                word += symbol
                                mode = "Function find"
                            else:
                                word = ""
                                mode = "Benchmark find"
                        else:
                            word += symbol
                    elif mode == "Function find":
                        if symbol == 'a':
                            word += symbol
                            mode = "Alloc found"
                        else:
                            word = ""
                            mode = "Benchmark find"
                    elif mode == "Alloc found":
                        if symbol in [' ', '\t', '\n', '\r']:
                            if word != "Benchmark.alloc":
                                word = ""
                                mode = "Benchmark find"
                        elif symbol == '(':
                            if word == "Benchmark.alloc":
                                word += symbol
                                number = 0
                                mode = "int parse"
                            else:
                                word = ""
                                mode = "Benchmark find"
                        else:
                            word += symbol
                    elif mode == "int parse":
                        word = ""
                        if symbol in "0123456789":
                            number = number * 10 + (ord(symbol) - ord('0'))
                        elif symbol == ")":
                            alloc_id_to_line[number] = line_number + 1
                            mode = "Benchmark find"
                        else:
                            mode = "Benchmark find"
                
                line_number = 1
                mode = "Benchmark find"
                word = ""
                
                parse_mode = "find type"
                type_name = ""
                variable_name = ""
                function_name = ""
                arg_mode = False
                arg_count = 0
                
                current_function_name = ""
                function_search_mode = False
                for symbol in code:
                    if symbol == '\n':
                        line_number += 1
                    if location == "collections.Array1":
                        print(f"{symbol} {parse_mode}") ##

                    # print(mode, symbol) #
                    if mode == "Benchmark find":
                        if symbol == 'B':
                            word = 'B'
                            mode = "Benchmark found"
                    elif mode == "Benchmark found":
                        if symbol in [' ', '\t', '\n', '\r']:
                            if word != "Benchmark":
                                word = ""
                                mode = "Benchmark find"
                        elif symbol == '.':
                            if word == "Benchmark":
                                word += symbol
                                mode = "Function find"
                            else:
                                word = ""
                                mode = "Benchmark find"
                        else:
                            word += symbol
                    elif mode == "Function find":
                        if symbol == 't':
                            word += symbol
                            mode = "Test found"
                        else:
                            word = ""
                            mode = "Benchmark find"
                    elif mode == "Test found":
                        if symbol in [' ', '\t', '\n', '\r']:
                            if word != "Benchmark.test":
                                word = ""
                                mode = "Benchmark find"
                        elif symbol == '(':
                            if word == "Benchmark.test":
                                word = ""
                                mode = "String parse"
                                allocation = Allocation()
                                allocation.path = location
                                allocation.function_name = current_function_name
                                # print(f"FIND test in {location}") #
                            else:
                                word = ""
                                mode = "Benchmark find"
                        else:
                            word += symbol
                    elif mode == "String parse":
                        if symbol == '"':
                            mode = "In String parse"
                        elif symbol == ",":
                            allocation.name = word
                            word = ""
                            mode = "String parse second"
                    elif mode == "String parse second":
                        if symbol == '"':
                            mode = "In String parse second"
                        elif symbol == ")":
                            allocation.dictionary = [transform_str_to_allocation_info(d) for d in word[1:].split(",{")]
                            for d in allocation.dictionary:
                                # print(alloc_id_to_line) #
                                d.alloc_id = alloc_id_to_line[d.alloc_id]
                            word = ""
                            mode = "Benchmark find"
                    elif mode == "In String parse":
                        if symbol == '"':
                            mode = "String parse"
                        else:
                            word += symbol
                    elif mode == "In String parse second":
                        if symbol == '"':
                            mode = "String parse second"
                        else:
                            word += symbol
                    
                    if parse_mode == "find type":
                        if symbol in " \t\n\r":
                            if len(type_name) > 0:
                                parse_mode = "find var"
                        elif (ord('a') <= ord(symbol) <= ord('z')) or (ord('A') <= ord(symbol) <= ord('Z')) or symbol == '_' or (ord('0') <= ord(symbol) <= ord('9')) or symbol in "[]":
                            type_name += symbol
                        else:
                            type_name = ""
                    elif parse_mode == "find var":
                        if symbol in " \t\n\r":
                            if len(variable_name) > 0:
                                parse_mode = "find end"
                        elif symbol in "=;":
                            parse_mode = "find type"
                            if len(variable_name) > 0:
                                result = Variable()
                                result.name = variable_name
                                result.line_number = line_number
                                result.position = arg_count if arg_mode else None
                                result.function_name = function_name
                                result.path = f"{graph.name}.{filename.name}"
                                location_to_name_to_variables[location][result.name] = result
                                print(f"FIND var ({variable_name}) in {location}") ##
                            type_name = variable_name = ""
                        elif (ord('a') <= ord(symbol) <= ord('z')) or (ord('A') <= ord(symbol) <= ord('Z')) or symbol == '_' or (ord('0') <= ord(symbol) <= ord('9')):
                            variable_name += symbol
                        elif symbol in ",)" and arg_mode:
                            parse_mode = "find type"
                            result = Variable()
                            result.name = variable_name
                            result.line_number = line_number
                            result.position = arg_count
                            result.function_name = function_name
                            result.path = f"{graph.name}.{filename.name}"
                            location_to_name_to_variables[location][result.name] = result
                            print(f"FIND var ({variable_name}) in {location}") ##
                            type_name = variable_name = ""
                        else:
                            if symbol == "(" and len(variable_name) > 0:
                                arg_mode = True
                                # print(f"FIND function {variable_name} in {location}") #
                                function_name = variable_name
                            parse_mode = "find type"
                            variable_name = ""
                            type_name = ""
                    elif parse_mode == "find end":
                        if symbol in " \t\n\r":
                            pass
                        elif symbol in "=;":
                            parse_mode = "find type"
                            result = Variable()
                            result.name = variable_name
                            result.line_number = line_number
                            result.position = arg_count if arg_mode else None
                            result.function_name = function_name
                            result.path = f"{graph.name}.{filename.name}"
                            location_to_name_to_variables[location][result.name] = result
                            print(f"FIND var ({variable_name}) in {location}") ##
                            type_name = variable_name = ""
                        elif symbol in ",)" and arg_mode:
                            parse_mode = "find type"
                            result = Variable()
                            result.name = variable_name
                            result.line_number = line_number
                            result.position = arg_count
                            result.function_name = function_name
                            result.path = f"{graph.name}.{filename.name}"
                            location_to_name_to_variables[location][result.name] = result
                            print(f"FIND var ({variable_name}) in {location}") ##
                            type_name = variable_name = ""
                        else:
                            if symbol == "(":
                                arg_mode = True
                                function_name = variable_name
                            if (ord('a') <= ord(symbol) <= ord('z')) or (ord('A') <= ord(symbol) <= ord('Z')) or symbol == '_' or (ord('0') <= ord(symbol) <= ord('9')):
                                type_name = variable_name
                                variable_name = symbol
                                parse_mode = "find var"
                            else:
                                parse_mode = "find type"
                                variable_name = ""
                                type_name = ""
                    
                    if function_search_mode:
                        # print(f"FSM {symbol} {line_number}") #
                        if symbol in " \n\t\r":
                            pass
                        elif symbol == "{":
                            current_function_name = function_name
                            function_search_mode = False
                        else:
                            function_search_mode = False
                    
                    if arg_mode and symbol == ')':
                        arg_mode = False
                        arg_count = 0
                        function_search_mode = True
                    if arg_mode and symbol == ',':
                        arg_count += 1
                    
                        

            allocations.append(allocation)
        
        file_to_line_number_to_alloc_id : Dict[str, Dict[int, int]] = dict()
        file_to_method_to_order_to_arg_id : Dict[str, Dict[str, Dict[int, int]]] = dict()
        file_to_function_to_name_to_local_id : Dict[str, Dict[str, Dict[str, int]]] = dict()
        with open(graph / "vertex_mappings.txt", encoding='utf-8') as file:
            for line in file.readlines():
                number, vertex = line.split(": ", maxsplit=2)
                number = int(number)
                if vertex.startswith("PtAllocVertex"):
                    # print(vertex) #
                    vertex = vertex.removeprefix("PtAllocVertex(")[:-2]
                    # _, method, *_, line_number = vertex.split(", ")
                    postmethod = vertex.split(", method=")[1]
                    method, line_number = postmethod.split(", lineNumber=")
                    # print(method) #
                    method = method.split(')', 1)[1]
                    location = method.split("#", 1)[0].split("$", 1)[0]
                    line_number = int(line_number)
                    if location not in file_to_line_number_to_alloc_id:
                        file_to_line_number_to_alloc_id[location] = dict()
                    file_to_line_number_to_alloc_id[location][line_number] = number
                elif vertex.startswith("PtArg"):
                    vertex = vertex.removeprefix("PtArg(")[:-2]
                    # print(vertex) #
                    method, *_, index = vertex.split(", ")
                    method = method.split(')', 1)[1]
                    method = method.split('(', 1)[0] # without arguments
                    # print(method) #
                    location, *_, method_name = split(r'[^\w_\.]', method) #method.split("#$")
                    index = int(index.removeprefix("index="))
                    if location not in file_to_method_to_order_to_arg_id:
                        file_to_method_to_order_to_arg_id[location] = dict()
                    if method_name not in file_to_method_to_order_to_arg_id[location]:
                        file_to_method_to_order_to_arg_id[location][method_name] = dict()
                    # print(file_to_method_to_order_to_arg_id) #
                    file_to_method_to_order_to_arg_id[location][method_name][index] = number
                elif vertex.startswith("PtLocalVar"):
                    vertex = vertex.removeprefix("PtLocalVar(")[:-2]
                    # print(vertex) #
                    method, *_, variable_name, _, line_number = vertex.split(", ")
                    method = method.split(')', 1)[1]
                    method = method.split('(', 1)[0] # without arguments
                    location, *_, method_name = split(r'[^\w_\.]', method)
                    line_number = int(line_number.removeprefix("lineNumber="))
                    variable_name = variable_name.removeprefix("name='")[:-1]
                    if location not in file_to_function_to_name_to_local_id:
                        file_to_function_to_name_to_local_id[location] = dict()
                    if method_name not in file_to_function_to_name_to_local_id[location]:
                        file_to_function_to_name_to_local_id[location][method_name] = dict()
                    file_to_function_to_name_to_local_id[location][method_name][variable_name] = number
                else:
                    continue
        may_be : Set[Tuple[int, int]] = set()
        may_not_be : Set[Tuple[int, int]] = set()
        must_be : Set[Tuple[int, int]] = set()
        must_not_be : Set[Tuple[int, int]] = set()
        alloc_id_to_info : Dict[int, str] = {}
        var_id_to_info : Dict[int, str] = {}
        
        loc_fun_num_name : List[Tuple[str, str, str, str]] = [
            ("basic.Branching1", "main", "%1", "a"),
            ("basic.Branching1", "main", "%3", "b"),
            ("basic.Interprocedural1", "main", "%4", "x"),
            ("basic.Interprocedural1", "main", "%4", "y"),
            ("basic.Interprocedural2", "main", "%4", "x"),
            ("basic.Interprocedural2", "main", "%4", "y"),
            ("basic.Loops2", "test", "%4", "o"),
            ("basic.Recursion1", "test", "%4", "n"),
            ("basic.ReturnValue1", "main", "%2", "b"),
            ("basic.ReturnValue2", "main", "%4", "b"),
            ("basic.SimpleAlias1", "main", "%0", "a"),
            ("basic.SimpleAlias1", "main", "%0", "b"),
            ("collections.Array1", "main", "b", "c"),
            ("collections.List1", "main", "%9", "c"),
            #("", "", "", ""),
        ]
        for loc, fun, num, name in loc_fun_num_name:
            if loc in file_to_function_to_name_to_local_id.keys():
                file_to_function_to_name_to_local_id[loc][fun][name] = file_to_function_to_name_to_local_id[loc][fun][num]
        
        loc_fun_pos_name : List[Tuple[str, str, int, str]] = [
            ("basic.Parameter1", "test", 0, "b"),
            ("basic.Parameter2", "test", 0, "b"),
        ]
        for loc, fun, pos, name in loc_fun_pos_name:
            if loc in file_to_function_to_name_to_local_id.keys():
                if fun not in file_to_function_to_name_to_local_id[loc].keys():
                    file_to_function_to_name_to_local_id[loc][fun] = dict()
                file_to_function_to_name_to_local_id[loc][fun][name] = file_to_method_to_order_to_arg_id[loc][fun][pos]
        
        for allocation in allocations:
            if allocation.path in {"basic.ReturnValue3"}:
                continue
            for concrete_alloc in allocation.dictionary:
                # print(file_to_line_number_to_alloc_local_id.keys(), allocation.path) #
                alloc_id = file_to_line_number_to_alloc_id[allocation.path][concrete_alloc.alloc_id]
                alloc_id_to_info[alloc_id] = f"{allocation.path} alloc {concrete_alloc.alloc_id}"
                for variable_name in concrete_alloc.may_alias:
                    var = location_to_name_to_variables[allocation.path][variable_name]
                    if var.is_arg():
                        assert var.function_name is not None
                        assert var.position is not None
                        var_id = file_to_method_to_order_to_arg_id[allocation.path][var.function_name][var.position]
                        var_id_to_info[var_id] = f"{allocation.path} argument {var.position} ({variable_name}) of {var.function_name}"
                    else:
                        print(f"PROCESS {allocation.path}") ##
                        print(var.line_number) ##
                        print(f"({allocation.function_name}) ({var.name})") ##
                        print(file_to_function_to_name_to_local_id[allocation.path][allocation.function_name].keys()) ##
                        var_id = file_to_function_to_name_to_local_id[allocation.path][allocation.function_name][var.name]
                        var_id_to_info[var_id] = f"{allocation.path} line {var.line_number} {variable_name}"
                    may_be.add((var_id, alloc_id))
                for variable_name in concrete_alloc.not_may_alias:
                    print(f"MNA {list(map(lambda x: f"{x[0]}, {x[1].line_number}", location_to_name_to_variables[allocation.path].items()))}") ##
                    var = location_to_name_to_variables[allocation.path][variable_name]
                    if var.is_arg():
                        assert var.function_name is not None
                        assert var.position is not None
                        var_id = file_to_method_to_order_to_arg_id[allocation.path][var.function_name][var.position]
                        var_id_to_info[var_id] = f"{allocation.path} argument {var.position} ({variable_name}) of {var.function_name}"
                    else:
                        var_id = file_to_function_to_name_to_local_id[allocation.path][allocation.function_name][var.name]
                        var_id_to_info[var_id] = f"{allocation.path} line {var.line_number} {variable_name}"
                    may_not_be.add((var_id, alloc_id))
                for variable_name in concrete_alloc.must_alias:
                    var = location_to_name_to_variables[allocation.path][variable_name]
                    if var.is_arg():
                        assert var.function_name is not None
                        assert var.position is not None
                        var_id = file_to_method_to_order_to_arg_id[allocation.path][var.function_name][var.position]
                        var_id_to_info[var_id] = f"{allocation.path} argument {var.position} ({variable_name}) of {var.function_name}"
                    else:
                        var_id = file_to_function_to_name_to_local_id[allocation.path][allocation.function_name][var.name]
                        var_id_to_info[var_id] = f"{allocation.path} line {var.line_number} {variable_name}"
                    must_be.add((var_id, alloc_id))
                for variable_name in concrete_alloc.not_must_alias:
                    var = location_to_name_to_variables[allocation.path][variable_name]
                    if var.is_arg():
                        assert var.function_name is not None
                        assert var.position is not None
                        var_id = file_to_method_to_order_to_arg_id[allocation.path][var.function_name][var.position]
                        var_id_to_info[var_id] = f"{allocation.path} argument {var.position} ({variable_name}) of {var.function_name}"
                    else:
                        var_id = file_to_function_to_name_to_local_id[allocation.path][allocation.function_name][var.name]
                        var_id_to_info[var_id] = f"{allocation.path} line {var.line_number} {variable_name}"
                    must_not_be.add((var_id, alloc_id))

        with open(graph / "results.txt", encoding='utf-8') as file:
            results = set(map(lambda l: tuple(map(int, l.split())), file.readlines()))
            for pair in results:
                if pair not in may_be:
                    print(f"Violation FP: pair {pair} not in may be")
                    
                    print(f"{alloc_id_to_info.get(pair[0])} <-> {var_id_to_info.get(pair[1])}")
                if pair in must_not_be:
                    print(f"Violation FP: pair {pair} in must not be\n{alloc_id_to_info.get(pair[0])} <-> {var_id_to_info.get(pair[1])}")
            for pair in must_be:
                if pair not in results:
                    print(f"Violation TN: pair {pair} must be but not in results\n{alloc_id_to_info.get(pair[0])} <-> {var_id_to_info.get(pair[1])}")

if __name__ == "__main__":
    main()