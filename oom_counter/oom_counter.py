import ast
from pprint import pprint
from itertools import combinations


class Analyzer(ast.NodeVisitor):
    def __init__(self):
        self.step = 1

        # 1st visit
        self.class_names = []
        self.variables_of_class = []
        self.methods_in_class = []
        self.__variables = []
        self.__methods = []

        # 2nd visit
        self.__current_class = 0
        self.using_class = []
        self.using_field = []
        self.__use = []
        self.__using_variable = []

        # 3rd visit
        self.used_methods_number = []

    def report(self):
        print("1st visit")
        print("Class Name")
        print(self.class_names)
        print("Variables")
        pprint(self.variables_of_class)
        print("Methods")
        pprint(self.methods_in_class)
        print()

        print("2nd visit")
        print("Connected Class")
        pprint(self.using_class)
        print("Connected Function")
        pprint(self.using_field)
        print()

        print("3rd visit")
        print("Used Method Number")
        pprint(self.used_methods_number)

    def visit_ClassDef(self, node: ast.ClassDef):
        if self.step == 1:
            # clear temp lists
            self.__variables.clear()
            self.__methods.clear()
            # save class name
            self.class_names.append(node.name)
            # save variables
            self.__variable_check(node)
            self.variables_of_class.append(self.__variables[:])
            # save methods
            self.generic_visit(node)
            self.methods_in_class.append(self.__methods[:])

        if self.step == 2:
            self.__use.clear()
            self.__current_class = self.class_names.index(node.name)
            self.__connecting_check_class(node)
            self.using_class.append(self.__use[:])

            self.__use.clear()
            self.generic_visit(node)
            self.using_field.append(self.__use[:])

        if self.step == 3:
            pass

    def visit_FunctionDef(self, node: ast.FunctionDef):
        if self.step == 1:
            self.__methods.append(node.name)

        if self.step == 2:
            self.__using_variable.clear()
            self.__connecting_check_func(node)
            self.__use.append(self.__using_variable[:])

        if self.step == 3:
            method_list = self.__using_method_check(node)
            count_list = self.__count_using_methods(method_list)
            self.used_methods_number = count_list[:]

    # 1st visit
    def __variable_check(self, node: ast.ClassDef):
        for item in ast.walk(node):
            if isinstance(item, ast.Assign):
                self.__class_variable_check(item)
            elif isinstance(item, ast.FunctionDef):
                if item.name == '__init__':
                    self.__instance_variable_check(item)
                break

    def __instance_variable_check(self, node: ast.FunctionDef):
        for item in node.body:
            if isinstance(item, ast.Assign):
                for target in item.targets:
                    if isinstance(target, ast.Attribute):
                        if isinstance(target.value, ast.Name):
                            if target.value.id == 'self':
                                if not (target.attr in self.__variables):
                                    self.__variables.append(target.attr)

    def __class_variable_check(self, node: ast.Assign):
        for target in node.targets:
            if isinstance(target, ast.Name):
                self.__variables.append(target.id)
            elif isinstance(target, ast.Tuple):
                self.__variables.extend(self.__check_tuple(target))

    def __check_tuple(self, item: ast.Tuple):
        id_list = []
        self.__check_tuple_rotate(item, id_list)
        return id_list

    def __check_tuple_rotate(self, item: ast.Tuple, ids):
        for item_in_tuple in item.elts:
            if isinstance(item_in_tuple, ast.Tuple):
                self.__check_tuple_rotate(item_in_tuple, ids)
            elif isinstance(item_in_tuple, ast.Name):
                ids.append(item_in_tuple.id)

    # 2nd visit
    def __connecting_check_class(self, node: ast.ClassDef):
        for item in ast.walk(node):
            if isinstance(item, ast.Name):
                if (item.id in self.class_names) and not (item.id in self.__use):
                    self.__use.append(item.id)

    def __connecting_check_func(self, node: ast.FunctionDef):
        for item in ast.walk(node):
            if isinstance(item, ast.Attribute):
                if (item.attr in self.variables_of_class[self.__current_class]) \
                        and not (item.attr in self.__use) \
                        and not (item.attr in self.__using_variable):
                    self.__using_variable.append(item.attr)

    # 3rd visit
    def __methods_list_init(self):
        ret_list = []
        for i in range(len(self.methods_in_class)):
            ret_list.append([])
            for j in range(len(self.methods_in_class[i])):
                ret_list[i].append(0)
        return ret_list

    def __instance_list_init(self):
        ret_list = []
        for i in range(len(self.class_names)):
            ret_list.append([])
        return ret_list

    def __using_method_check(self, node: (ast.FunctionDef or ast.AsyncFunctionDef)):
        method_list = self.__methods_list_init()
        instance_list = self.__instance_list_init()

        for item in ast.walk(node):
            if isinstance(item, ast.Assign):
                instance_id = ''
                for target in item.targets:
                    if isinstance(target, ast.Name):
                        instance_id = target.id
                if isinstance(item.value, ast.Call):
                    if isinstance(item.value.func, ast.Name):
                        class_id = item.value.func.id
                        if class_id in self.class_names:
                            index = self.class_names.index(class_id)
                            instance_list[index].append(instance_id)
                            if method_list[index][0] == 0:
                                method_list[index][0] = 1

            elif isinstance(item, ast.Expr):
                if isinstance(item.value, ast.Call):
                    if isinstance(item.value.func, ast.Attribute):
                        instance_id = ''
                        i = 0
                        if isinstance(item.value.func.value, ast.Name):
                            instance_id = item.value.func.value.id
                        for index in range(len(instance_list)):
                            if instance_id in instance_list[index]:
                                i = index
                        if item.value.func.attr in self.methods_in_class[i]:
                            j = self.methods_in_class[i].index(item.value.func.attr)
                            if method_list[i][j] == 0:
                                method_list[i][j] = 1
        return method_list

    @staticmethod
    def __count_using_methods(method_list):
        count = []
        for i in range(len(method_list)):
            count.append(0)
            for num in method_list[i]:
                if num == 1:
                    count[i] += 1
        return count


class ComputeComplexity:
    def __init__(self, filepath):
        self.analyzer = Analyzer()
        self.class_names = []
        self.wmc_value = []
        self.cbo_value = []
        self.rfc_value = []
        self.lcom_value = []

        ptree = self.parse_file(filepath)
        self.analyzer.visit(ptree)
        self.class_names.extend(self.analyzer.class_names[:])
        self.analyzer.step = 2
        self.analyzer.visit(ptree)
        self.analyzer.step = 3
        self.analyzer.visit(ptree)

    @staticmethod
    def parse_file(filepath):
        with open(filepath, "r", encoding="UTF-8") as f:
            ptree = ast.parse(f.read(), filename=filepath)
        f.close()
        return ptree

    def wmc(self, class_name):
        if class_name in self.class_names:
            index = self.class_names.index(class_name)
            self.wmc_value.insert(index, len(self.analyzer.methods_in_class[index]))

    def cbo(self, class_name):
        cbo_value = 0
        if class_name in self.class_names:
            index = self.class_names.index(class_name)
            connected_classes = self.analyzer.using_class
            for i in range(len(connected_classes)):
                if i != index:
                    if class_name in connected_classes[i]:
                        cbo_value += 1
            self.cbo_value.insert(index, cbo_value)

    def rfc(self, class_name):
        if class_name in self.class_names:
            index = self.class_names.index(class_name)
            used_methods_number = self.analyzer.used_methods_number
            rfc_value = used_methods_number[index]
            self.rfc_value.insert(index, rfc_value)

    def lcom(self, class_name):
        q = 0
        p = 0
        if class_name in self.class_names:
            index = self.class_names.index(class_name)
            all_combinations = list(combinations(self.analyzer.using_field[index], 2))
            for aTuple in all_combinations:
                combi_set = set(aTuple[0]) & set(aTuple[1])
                if self.is_empty(combi_set):
                    p += 1
                else:
                    q += 1
            if p <= q:
                self.lcom_value.insert(index, 0)
            else:
                self.lcom_value.insert(index, p - q)

    @staticmethod
    def is_empty(item):
        return item == set()

    def run(self):
        for name in self.class_names:
            self.wmc(name)
            self.cbo(name)
            self.rfc(name)
            self.lcom(name)

    def write(self, outfile):
        self.run()
        outfile = open(outfile, "w", encoding="UTF-8")
        for name in self.class_names:
            index = self.class_names.index(name)
            outfile.write(name + ":\n")
            outfile.write("   - wmc: %d\n" % self.wmc_value[index])
            outfile.write("   - cbo: %d\n" % self.cbo_value[index])
            outfile.write("   - rfc: %d\n" % self.rfc_value[index])
            outfile.write("   - lcom: %d\n" % self.lcom_value[index])


def main():
    filepath = "../test.py"
    counter = ComputeComplexity(filepath)
    counter.write("out.file")


if __name__ == "__main__":
    main()
