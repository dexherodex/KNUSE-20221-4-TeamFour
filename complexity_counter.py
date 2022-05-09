import sys
import ast


def parse_file(filepath):
    with open(filepath, "r") as f:
        ptree = ast.parse(f.read(), filename=filepath)
    f.close()
    return ptree


