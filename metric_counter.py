import ast
import sys


def read_lines(filepath):
    """ file to lines """
    with open(filepath, "r", encoding="UTF-8") as f:
        lines = f.readlines()

    f.close()

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
    num_comment_only = 0
    quote_is_open = False  # Variable of whether single quote is open
    double_quote_is_open = False  # Variable of whether double quote is open
    paren_is_open = [False, False, False]  # List of whether parenthesis is open (0: (), 1: {}, 2: [])
    lines = read_lines(filepath)

    for aline in lines:
        stripped_line = list(aline.strip())
        paren_is_open = check_paren(stripped_line, paren_is_open, quote_is_open, double_quote_is_open)

        if not paren_is_open[0] and not paren_is_open[1] and not paren_is_open[2]:
            # when code with parentheses is closed, check about quote comment
            value, quote_is_open, double_quote_is_open \
                = count_three_quotes(stripped_line, quote_is_open, double_quote_is_open)

            if value > 0:
                # if quote comment is open at current line
                if not stripped_line[len(stripped_line) - 1] in [')', '}', ']']:
                    num_comment += value
                    num_comment_only += value
                else:
                    quote_is_open = False
                    double_quote_is_open = False

            elif value <= 0 and not quote_is_open and not double_quote_is_open:
                # if quote comment is not open then check hash(#) comment
                value = count_hash(stripped_line)
                if value == 1:
                    num_comment += 1
                    num_comment_only += value
                elif value == 2:
                    num_comment += 1
                else:
                    continue

    return num_comment, num_comment_only


def count_hash(stripped_line):
    """ Count number of hash(#) comment """
    num_hash = 0
    first = stripped_line[:1]

    if '#' in stripped_line:
        if first == ['#']:
            num_hash = 1
        elif hash_in_string(stripped_line, '"'):
            num_hash = 0
        elif hash_in_string(stripped_line, "'"):
            num_hash = 0
        else:
            num_hash = 2

    return num_hash


def hash_in_string(stripped_line, quote):
    """ Check whether hash(#) is in string """
    quote_is_open = False
    hash_in_str = False
    quote_can_in_str = False

    compare_quote = ""
    if quote == '"':
        compare_quote = '"'
    if quote == "'":
        compare_quote = "'"

    for item in stripped_line:
        if item == '\\' and quote_is_open and not quote_can_in_str:
            quote_can_in_str = True
            continue
        elif quote_is_open and quote_can_in_str:
            quote_can_in_str = False
            continue

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


def count_three_quotes(stripped_line, quote_is_open, double_quote_is_open):
    """ Count number of quotes comment """
    num_comment = 0

    quotes_pair = check_three_quotes(stripped_line, "'", quote_is_open)
    double_quotes_pair = check_three_quotes(stripped_line, '"', double_quote_is_open)

    """ single quote """
    if quotes_pair == 2 and not quote_is_open:
        num_comment += 1
    elif quotes_pair == 1:
        if not quote_is_open:
            quote_is_open = True
        else:
            quote_is_open = False
        num_comment += 1
    elif quote_is_open and quotes_pair != -1:
        num_comment += 1

    """ double quote """
    if double_quotes_pair == 2 and not double_quote_is_open:
        num_comment += 1
    elif double_quotes_pair == 1:
        if not double_quote_is_open:
            double_quote_is_open = True
        else:
            double_quote_is_open = False
        num_comment += 1
    elif double_quote_is_open and double_quotes_pair != -1:
        num_comment += 1

    return num_comment, quote_is_open, double_quote_is_open


def check_three_quotes(stripped_line, quote, quote_open):
    """ Check whether three quote comment is exist """
    if not stripped_line:
        return -1

    compare_quote = ''
    encase_quote = ''

    if quote == '"':
        compare_quote = '"'
        encase_quote = "'"
    elif quote == "'":
        compare_quote = "'"
        encase_quote = '"'

    stack_open = []
    stack_close = []
    full = 3

    is_encase_open = False
    encase_stack = 0
    encase_full = 2

    paren_is_open = [False, False, False]  # List of whether parenthesis is open (0: (), 1: {}, 2: [])

    for item in stripped_line:
        if item == '#' and not quote_open:
            # when quotes are in hash(#) comment
            return 0
        if item == '=' and not quote_open:
            # when quotes assign to some variable
            return 0

        # when quote is in parentheses
        paren_is_open = check_paren(stripped_line, paren_is_open, quote_open, quote_open)

        if not paren_is_open[0] and not paren_is_open[1] and not paren_is_open[2]:
            if item == compare_quote:
                if len(stack_open) < full and len(stack_close) < full:
                    stack_open.append(item)
                elif len(stack_open) == full:
                    stack_close.append(item)
                else:
                    continue
            elif item == encase_quote:
                # if quotes are in the other quotes
                # Example: '"""' or "'''"
                if not is_encase_open:
                    encase_stack += 1
                    is_encase_open = True
                elif is_encase_open:
                    encase_stack += 1
                    if encase_stack > encase_full:
                        encase_stack = 0
                        is_encase_open = False
            else:
                if len(stack_open) != full:
                    stack_open.clear()
                if len(stack_close) != full:
                    stack_close.clear()

    if len(stack_open) == full and len(stack_close) == full:
        return 2  # a quote comment is open and close
    elif len(stack_open) == full:
        return 1  # a quote comment is just open or close
    else:
        return 0


def parse_file(filepath):
    """ Parsing file to AST """
    with open(filepath, "r", encoding="UTF-8") as f:
        ptree = ast.parse(f.read(), filename=filepath)

    f.close()

    return ptree


def count_function(filepath):
    """ Count number of functions in file with AST """
    ptree = parse_file(filepath)
    num_func = 0

    for item in ast.walk(ptree):
        if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
            num_func += 1

    return num_func


def check_paren(stripped_line, paren_is_open, quote_is_open, double_quote_is_open):
    """ Check whether parentheses are open or close """
    for item in stripped_line:
        if item == '(' and not paren_is_open[0] and not quote_is_open and not double_quote_is_open:
            paren_is_open[0] = True
        elif item == ')' and paren_is_open[0]:
            paren_is_open[0] = False
        elif item == '{' and not paren_is_open[1] and not quote_is_open and not double_quote_is_open:
            paren_is_open[1] = True
        elif item == '}' and paren_is_open[1]:
            paren_is_open[1] = False
        elif item == '[' and not paren_is_open[2] and not quote_is_open and not double_quote_is_open:
            paren_is_open[2] = True
        elif item == ']' and paren_is_open[2]:
            paren_is_open[2] = False
        else:
            continue

    return paren_is_open


def count_standalone_paren(filepath):
    """ Count standalone parenthesis """
    num_standalone = 0
    is_standalone = False

    with open(filepath, "r", encoding="UTF-8") as f:
        lines = f.readlines()

    for aline in lines:
        striped_line = list(aline.strip())
        for item in striped_line:
            if item == '':
                continue
            elif item in ['[', ']', '{', '}', '(', ')']:
                is_standalone = True
            else:
                is_standalone = False
                break

        if is_standalone:
            num_standalone += 1
            is_standalone = False

    f.close()

    return num_standalone


def main():
    if len(sys.argv) < 3:
        print(f"Usage: <{sys.argv[0]}> <in.file> <out.file>\n")
        exit(1)

    # input file's path
    infile = sys.argv[1]
    if infile[-3:] != ".py":
        print("\"in.file\" must be written by python language.")
        exit(1)

    # count number of lines if file
    num_all_code_lines = count_lines_of_code(infile)
    # count number of blanks in file
    num_blank = count_blank(infile)
    # count number of comment lines
    num_comment, num_only_comment = count_comment(infile)
    # count standalone parenthesis
    num_standalone = count_standalone_paren(infile)
    # count number of function
    num_function = count_function(infile)

    # number of lines without blanks (LOC)
    num_code_lines = num_all_code_lines - num_blank - num_only_comment
    # number of effective lines (eLOC)
    effective = num_all_code_lines - num_blank - num_only_comment - num_standalone

    outfile = open(sys.argv[2], "w", encoding="UTF-8")

    loc = "LOC: %d\n" % num_code_lines
    eloc = "eLOC: %d\n" % effective
    comment = "Comment: %d\n" % num_comment
    blank = "Blank: %d\n" % num_blank
    no_of_function = "No. of Functions: %d\n" % num_function

    outfile.write(loc)
    outfile.write(eloc)
    outfile.write(comment)
    outfile.write(blank)
    outfile.write(no_of_function)

    outfile.close()


if __name__ == "__main__":
    main()
