import ast


def read_lines(filepath):
    """ file to lines """
    with open(filepath, "r") as f:
        lines = f.readlines()

    return lines


def count_lines_of_code(filepath):
    """ Count number of lines in code"""
    lines = read_lines(filepath)

    return len(lines)


def count_blank(filepath):
    """ Count number of blanks in file """
    num_blank = 0
    lines = read_lines(filepath)

    for aline in lines:
        if aline.strip() == '':
            num_blank += 1

    return num_blank


def count_comment(filepath):
    """ Count number of comments in file """


def parse_file(filepath):
    """ Parsing file to AST """
    with open(filepath, "r") as f:
        return ast.parse(f.read(), filename=filepath)


def count_function(filepath):
    """ Count number of functions in file with AST """
    ptree = parse_file(filepath)
    num_func = 0

    for item in ast.walk(ptree):
        if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
            num_func += 1

    return num_func
