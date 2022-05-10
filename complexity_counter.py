import sys
import ast


def parse_file(filepath):
    with open(filepath, "r", encoding="UTF-8") as f:
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
        fan_in = arguments_number(item_copy, fan_in)
        fan_out = return_number(item_copy, fan_out)
        new_list, fan_in = global_input(item_copy, fan_in)
        global_list.extend(new_list)
        fan_out = global_output(item_copy, global_list, fan_out)

    return branch, fan_in, fan_out


def arguments_number(item_arguments, fan_in):
    if isinstance(item_arguments, ast.arguments):
        fan_in += len(item_arguments.args)
    return fan_in


def return_number(item_return, fan_out):
    copy_ret = item_return
    if isinstance(copy_ret, ast.Return):
        for item in ast.walk(item_return):
            copy = item
            if isinstance(copy, ast.Return):
                continue
            elif isinstance(copy, ast.Tuple):
                fan_out += len(copy.elts)
                return fan_out
            else:
                break
        fan_out += 1

    return fan_out


def global_input(item_global, fan_in):
    new_list = []
    if isinstance(item_global, ast.Global):
        new_list.extend(item_global.names)
        fan_in += len(item_global.names)
    return new_list, fan_in


def global_output(item_assign, global_list, fan_out):
    if isinstance(item_assign, (ast.Assign, ast.AugAssign, ast.AnnAssign)):
        if len(global_list) > 0:
            count = 0
            if isinstance(item_assign, ast.Assign):
                variables = item_assign.targets[0]
            else:
                variables = item_assign.target

            # single variable assign
            if isinstance(variables, ast.Name):
                if variables.id in global_list:
                    count += 1
            # multiple variable assign
            elif isinstance(variables, ast.Tuple):
                for item in variables.elts:
                    if isinstance(item, ast.Name):
                        if item.id in global_list:
                            count += 1
            # list assign
            elif isinstance(variables, ast.Subscript):
                if isinstance(variables.value, ast.Name):
                    if variables.value.id in global_list:
                        count += 1
            fan_out += count

    return fan_out
