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
    num_comment = 0
    lines = read_lines(filepath)
    # num_comment = hash(#) comment + quote(""") comment


def count_hash(stripped_line):
    """ Count number of hash(#) comment """
    num_hash = 0
    first = stripped_line[:1]

    if '#' in stripped_line:
        if first == ['#']:
            num_hash = 0
        elif hash_in_string(stripped_line, '"'):
            num_hash = 0
        elif hash_in_string(stripped_line, "'"):
            num_hash = 0
        else:
            num_hash = 1

    return num_hash


def hash_in_string(stripped_line, quote):
    """ Check whether hash(#) is in string """
    quote_is_open = False
    hash_in_str = False

    compare_quote = ""
    if quote == '"':
        compare_quote = '"'
    if quote == "'":
        compare_quote = "'"

    for item in stripped_line:
        if item == compare_quote:
            if not quote_is_open:
                quote_is_open = True
            else:
                quote_is_open = False

        if item == '#':
            if quote_is_open:
                hash_in_str = True
            else:
                hash_in_str = False

    return hash_in_str


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
