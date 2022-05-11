import ast
import sys
from pprint import pprint


class Visitor(ast.NodeVisitor):
    def __init__(self):
        self.classes = []
        self.class_methods = {}
        self.functions = {"name": [], "cyclomatic": [], "ifc": []}
        self.methods = {"name": [], "cyclomatic": [], "ifc": []}
        self.analyzer = Analyzer()

    def visit_ClassDef(self, node):
        self.methods["name"].clear()
        self.methods["cyclomatic"].clear()
        self.methods["ifc"].clear()
        self.generic_visit(node)

        count = self.count_methods(node)
        name = self.methods["name"][:count]
        cyclomatic = self.methods["cyclomatic"][:count]
        ifc = self.methods["ifc"][:count]
        sliced_dict = {"name": name, "cyclomatic": cyclomatic, "ifc": ifc}

        i = 0
        while i < count:
            if sliced_dict["name"][i] in self.functions["name"]:
                self.functions["name"].remove(sliced_dict["name"][i])
                self.functions["cyclomatic"].remove(sliced_dict["cyclomatic"][i])
                self.functions["ifc"].remove(sliced_dict["ifc"][i])
            i += 1

        self.class_methods[node.name] = sliced_dict
        self.classes.append((node.name, count))

    @staticmethod
    def count_methods(node):
        count = 0
        for item in ast.walk(node):
            if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                count += 1
        return count

    def visit_FunctionDef(self, node):
        self.analyzer.analyse(node)

        self.methods["name"].append(node.name)
        self.methods["cyclomatic"].append(self.analyzer.cyclomatic())
        self.methods["ifc"].append(self.analyzer.ifc())

        self.functions["name"].append(node.name)
        self.functions["cyclomatic"].append(self.analyzer.cyclomatic())
        self.functions["ifc"].append(self.analyzer.ifc())

    def visit_AsyncFunctionDef(self, node):
        self.analyzer.analyse(node)

        self.methods["name"].append(node.name)
        self.methods["cyclomatic"].append(self.analyzer.cyclomatic())
        self.methods["ifc"].append(self.analyzer.ifc())

        self.functions["name"].append(node.name)
        self.functions["cyclomatic"].append(self.analyzer.cyclomatic())
        self.functions["ifc"].append(self.analyzer.ifc())

    def report(self):
        pprint(self.class_methods)
        pprint(self.classes)
        pprint(self.functions)

    def write(self, filepath):
        with open(filepath, "w", encoding="UTF-8") as source:
            for (class_name, count) in self.classes:
                methods_info = self.class_methods[class_name]
                for i in range(count):
                    name = class_name + ":" + methods_info["name"][i]
                    cyclomatic = methods_info["cyclomatic"][i]
                    ifc = methods_info["ifc"][i]
                    source.write(name + ":\n")
                    source.write("   - cyclomatic: %d\n" % cyclomatic)
                    source.write("   - ifc: %d\n" % ifc)
            for i in range(len(self.functions["name"])):
                source.write(self.functions["name"][i] + ":\n")
                source.write("   - cyclomatic: %d\n" % self.functions["cyclomatic"][i])
                source.write("   - ifc: %d\n" % self.functions["ifc"][i])


class Analyzer:

    def __init__(self):
        self.branch = 0
        self.fan_in = 0
        self.fan_out = 0

    def cyclomatic(self):
        cyclomatic_complexity = self.branch + 1
        return cyclomatic_complexity

    def ifc(self):
        ifc_complexity = (self.fan_in * self.fan_out) ** 2
        return ifc_complexity

    def analyse(self, function_item):
        branch = 0
        arg = 0
        ret = 0
        yld = 0
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
            arg_list, arg = self.__arguments_number(item_copy, arg_list, arg)  # in
            ret = self.__return_number(item_copy, ret)  # out
            yld = self.__yield_number(item_copy, yld)
            new_list, global_in = self.__global_input(item_copy, global_in)  # in
            global_list.extend(new_list)
            global_out = self.__global_output(item_copy, global_list, global_out)  # out
            instance_assign = self.__instance_variable_assign_number(item_copy, arg_list, instance_assign)  # out
            list_out = self.__list_assign(item_copy, arg_list, list_out)

        self.branch = branch
        self.fan_in = arg + global_in
        self.fan_out = ret + global_out + instance_assign + list_out + yld

    @staticmethod
    def __arguments_number(item_arguments, arg_list: list, fan_in):
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

    @staticmethod
    def __return_number(item_return, fan_out):
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

    @staticmethod
    def __yield_number(item_yield, fan_out):
        copy_yield = item_yield
        index = 0
        if isinstance(copy_yield, ast.Expr):
            if isinstance(copy_yield.value, ast.Yield):
                for item in ast.walk(item_yield):
                    copy = item
                    index += 1
                    if isinstance(copy, (ast.Expr, ast.Yield)):
                        continue
                    elif isinstance(copy, ast.Tuple):
                        fan_out += len(copy.elts)
                        return fan_out
                    else:
                        break
                if index > 1:
                    fan_out += 1
            elif isinstance(copy_yield.value, ast.YieldFrom):
                for item in ast.walk(item_yield):
                    copy = item
                    index += 1
                    if isinstance(copy, (ast.Expr, ast.YieldFrom)):
                        continue
                    else:
                        break
                if index > 1:
                    fan_out += 1

        return fan_out

    @staticmethod
    def __global_input(item_global, fan_in):
        new_list = []
        if isinstance(item_global, ast.Global):
            new_list.extend(item_global.names)
            fan_in += len(item_global.names)
        return new_list, fan_in

    @staticmethod
    def __global_output(item_assign, global_list, fan_out):
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

    def __instance_variable_assign_number(self, item_assign, arg_list, fan_out):
        if isinstance(item_assign, (ast.Assign, ast.AugAssign, ast.AnnAssign)):
            count = 0
            if isinstance(item_assign, ast.Assign):
                variables = item_assign.targets[0]
            else:
                variables = item_assign.target

            if isinstance(variables, ast.Attribute):
                count += self.__find_arg(variables, arg_list)
            elif isinstance(variables, ast.Tuple):
                for variable in variables.elts:
                    count += self.__find_arg(variable, arg_list)
            fan_out += count

        return fan_out

    @staticmethod
    def __find_arg(variable, arg_list):
        item = variable
        while not isinstance(item, ast.Name):
            if isinstance(item, ast.Attribute):
                item = item.value

        if item.id in arg_list:
            return 1

        return 0

    @staticmethod
    def __list_assign(item, arg_list, fan_out):
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


def parse_file(filepath):
    with open(filepath, "r", encoding="UTF-8") as f:
        ptree = ast.parse(f.read(), filename=filepath)
    f.close()
    return ptree


def main():
    if len(sys.argv) < 3:
        print(f"Usage: <{sys.argv[0]}> <in.file> <out.file>\n")
        exit(1)

    infile = sys.argv[1]
    outfile = sys.argv[2]

    ptree = parse_file(infile)
    counter = Visitor()
    counter.visit(ptree)
    # complexity_counter.report()
    counter.write(outfile)


if __name__ == "__main__":
    main()
