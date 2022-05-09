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
    for item in ast.walk(function_item):
        item_copy = item
        if isinstance(item_copy, (ast.While, ast.For, ast.If)):
            branch += 1
        elif isinstance(item_copy, ast.arguments):
            fan_in += arguments_number(item_copy)
        elif isinstance(item_copy, ast.Return):
            fan_out += return_number(item_copy)

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

