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


def analyser(function_item):
    branch = 0
    arg = 0
    ret = 0
    global_in = 0
    global_out = 0
    instance_assign = 0
    list_out = 0
    global_list = []
    arg_list = []

    for item in ast.walk(function_item):
        item_copy = item
        if isinstance(item_copy, (ast.While, ast.For, ast.If, ast.Assert, ast.Try)):
            branch += 1
        arg_list, arg = arguments_number(item_copy, arg_list, arg)  # in
        ret = return_number(item_copy, ret)  # out
        new_list, global_in = global_input(item_copy, global_in)  # in
        global_list.extend(new_list)
        global_out = global_output(item_copy, global_list, global_out)  # out
        instance_assign = instance_variable_assign_number(item_copy, arg_list, instance_assign)  # out
        list_out = list_assign(item_copy, arg_list, list_out)  # out

    fan_in = arg + global_in
    fan_out = ret + global_out + instance_assign + list_out

    return branch, fan_in, fan_out


def arguments_number(item_arguments, arg_list: list, fan_in):
    count = 0
    if isinstance(item_arguments, ast.arguments):
        count += len(item_arguments.args)
        args = item_arguments.args
        if len(arg_list) <= 0:
            for i in range(count):
                if isinstance(args[i], ast.arg):
                    arg_list.append(args[i].arg)

    fan_in += count
    return arg_list, fan_in


def return_number(item_return, fan_out):
    copy_ret = item_return
    index = 0
    if isinstance(copy_ret, ast.Return):
        for item in ast.walk(item_return):
            copy = item
            index += 1
            if isinstance(copy, ast.Return):
                continue
            elif isinstance(copy, ast.Tuple):
                fan_out += len(copy.elts)
                return fan_out
            else:
                break
        if index > 1:
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
            fan_out += count

    return fan_out


def instance_variable_assign_number(item_assign, arg_list, fan_out):
    if isinstance(item_assign, (ast.Assign, ast.AugAssign, ast.AnnAssign)):
        count = 0
        if isinstance(item_assign, ast.Assign):
            variables = item_assign.targets[0]
        else:
            variables = item_assign.target

        if isinstance(variables, ast.Attribute):
            count += find_arg(variables, arg_list)
        elif isinstance(variables, ast.Tuple):
            for variable in variables.elts:
                count += find_arg(variable, arg_list)
        fan_out += count

    return fan_out


def find_arg(variable, arg_list):
    item = variable
    while not isinstance(item, ast.Name):
        if isinstance(item, ast.Attribute):
            item = item.value

    if item.id in arg_list:
        return 1

    return 0


def list_assign(item, arg_list, fan_out):
    count = 0
    if isinstance(item, ast.Assign):
        target = item.targets[0]
        if isinstance(target, ast.Subscript):
            value = target.value
            if isinstance(value, ast.Name):
                if value.id in arg_list:
                    count += 1
    elif isinstance(item, ast.Expr):
        value = item.value
        if isinstance(value, ast.Call):
            func = value.func
            if isinstance(func, ast.Attribute):
                attr = func.attr
                func_value = func.value
                if isinstance(func_value, ast.Name):
                    if func_value.id in arg_list:
                        if attr == 'append' or attr == 'extend':
                            count += 1

    fan_out += count

    return fan_out


def file_write(outfile, name, cyclomatic_number, ifc_number):
    outfile.write(name + ":\n")
    outfile.write("   - cyclomatic: %d\n" % cyclomatic_number)
    outfile.write("   - ifc: %d\n" % ifc_number)


def main():
    if len(sys.argv) < 3:
        print(f"Usage: <{sys.argv[0]}> <in.file> <out.file>\n")
        exit(1)

    infile = sys.argv[1]
    outfile = open(sys.argv[2], "w", encoding="UTF-8")

    if infile[-3:] != '.py':
        print("\"in.file\" must be written by python language.")
        exit(1)

    ptree = parse_file(infile)
    for item in ast.walk(ptree):
        copy = item
        if isinstance(copy, (ast.FunctionDef, ast.AsyncFunctionDef)):
            branch, fan_in, fan_out = analyser(item)
            cyclomatic_number = cyclomatic(branch)
            ifc_number = ifc(fan_in, fan_out)
            file_write(outfile, copy.name, cyclomatic_number, ifc_number)


if __name__ == "__main__":
    main()
