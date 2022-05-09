import sys
import ast


def parse_file(filepath):
    with open(filepath, "r") as f:
        ptree = ast.parse(f.read(), filename=filepath)
    f.close()
    return ptree


def cyclomatic(branch):
    cyclomatic_complexity = branch + 1
    return cyclomatic_complexity


def ifc(fan_in, fan_out):
    ifc_complexity = (fan_in * fan_out) ** 2
    return ifc_complexity


def analyser(function_item, branch, fan_in, fan_out):
    global_list = []
    for item in ast.walk(function_item):
        item_copy = item
        if isinstance(item_copy, (ast.While, ast.For, ast.If)):
            branch += 1
        elif isinstance(item_copy, ast.arguments):
            fan_in += arguments_number(item_copy)
        elif isinstance(item_copy, ast.Global):
            new_list = global_number(item_copy)
            global_list.extend(new_list)
            fan_in += len(new_list)
        elif isinstance(item_copy, ast.Return):
            fan_out += return_number(item_copy)
        elif isinstance(item_copy, (ast.Assign, ast.AugAssign, ast.AnnAssign)):
            if len(global_list) > 0:
                fan_out += global_assign_number(item_copy, global_list)

    return branch, fan_in, fan_out


def arguments_number(item_arguments):
    return len(item_arguments.args)


def return_number(item_return):
    for item in ast.walk(item_return):
        copy = item
        if isinstance(copy, ast.Return):
            continue
        elif isinstance(copy, ast.Tuple):
            return len(copy.elts)
        else:
            break
    return 1


def global_number(item_global):
    return item_global.names


def global_assign_number(item_assign, global_list):
    count = 0
    variables = item_assign.targets[0]
    if isinstance(variables, ast.Name):
        if variables.id in global_list:
            count += 1
    elif isinstance(variables, ast.Tuple):
        for item in variables.elts:
            if isinstance(item, ast.Name):
                if item.id in global_list:
                    count += 1
    elif isinstance(variables, ast.Subscript):
        if isinstance(variables.value, ast.Name):
            if variables.value.id in global_list:
                count += 1

    return count
