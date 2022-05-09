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
