import ast
import sys
from pprint import pprint
from itertools import combinations


class Analyzer(ast.NodeVisitor):
    """
    Class for visit each node of abstract syntax tree.
        - 1st visit: Save information of each class. (class name, method name, variable name, global variable name)
        - 2nd visit: Save usage information of each class and class's method.
    """
    ##################
    # Public Methods #
    ##################

    def __init__(self):
        self.step = 1  # order of visit
        self.__in_class = False
        self.__in_function = False

        # 1st visit
        self.class_names = []
        self.variables_in_class = {}
        self.methods_in_class = {}
        self.global_variables = []
        self.__variables = []
        self.__methods = []

        # 2nd visit
        self.__current_class = ""
        self.using_class = {}
        self.using_method = {}
        self.using_variable = {}
        self.using_global_variable = {}
        self.__using_classes = []
        self.__using_methods = []
        self.__using_variables = []
        self.__use1 = []
        self.__use2 = []
        self.__use3 = []

    def report(self):
        """
        Report all public variables. \n
        :return: Print out public instance variables
        """
        print("1st visit")
        print("Class Name")
        print(self.class_names)
        print()
        print("Global Variables")
        pprint(self.global_variables)
        print()
        print("Variables")
        pprint(self.variables_in_class)
        print()
        print("Methods")
        pprint(self.methods_in_class)
        print('\n')

        print("2nd visit")
        print("Used Class")
        pprint(self.using_class)
        print()
        print("Used variable")
        pprint(self.using_variable)
        print()
        print("Used Method")
        pprint(self.using_method)
        print()
        print("Used Global variable")
        pprint(self.using_global_variable)
        print('\n')

    def visit_ClassDef(self, node: ast.ClassDef):
        """
        When visit ClassDef, save class' information. \n
        step1: Get class_names, variable_in_class, methods_in_class \n
        step2: Get using_class, using_variable, using_method \n
        :param node: Node that is instance of ClassDef
        :return: None
        """
        self.__in_class = True

        if self.step == 1:
            # clear temp lists
            self.__variables.clear()
            self.__methods.clear()

            # save class name
            self.class_names.append(node.name)

            # save variables
            self.__variable_check(node)
            self.variables_in_class[node.name] = self.__variables[:]

            # save methods
            self.generic_visit(node)
            self.methods_in_class[node.name] = self.__methods[:]

        if self.step == 2:
            # save the classes used by each class
            self.__using_classes.clear()
            self.__current_class = node.name
            self.__check_class_use(node)
            self.using_class[self.__current_class] = self.__using_classes[:]

            # save the global variables used by each class
            self.__use3.clear()
            self.__check_global_variable_use(node)
            self.using_global_variable[self.__current_class] = self.__use3[:]

            self.__use1.clear()
            self.__use2.clear()
            self.generic_visit(node)
            # save the variables used by each class's each method
            self.using_variable[self.__current_class] = self.__use1[:]
            # save the methods used by each class's local method
            self.using_method[self.__current_class] = self.__use2[:]

        self.__in_class = False

    def visit_FunctionDef(self, node: ast.FunctionDef):
        """
        When visit FunctionDef, save function's information. \n
        step1: Get method's name \n
        step2: Get using methods and variables \n
        :param node: Node that is instance of FunctionDef
        :return: None
        """
        self.__in_function = True

        if self.step == 1:
            # save method's name
            self.__methods.append(node.name)

        if self.step == 2:
            # save the instance or class variables used by method
            self.__using_variables.clear()
            self.__check_variable_use(node)
            self.__use1.append(self.__using_variables[:])

            # save the local methods used by method
            self.__using_methods.clear()
            self.__check_method_use(node)
            self.__use2.append(self.__using_methods[:])

        self.__in_function = False

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef):
        """
        When visit AsyncFunctionDef, save function's information. \n
        step1: Get method's name \n
        step2: Get using methods and variables \n
        :param node: Node that is instance of FunctionDef
        :return: None
        """
        self.__in_function = True

        if self.step == 1:
            # save method's name
            self.__methods.append(node.name)

        if self.step == 2:
            # save the instance or class variables used by method
            self.__using_variables.clear()
            self.__check_variable_use(node)
            self.__use1.append(self.__using_variables[:])

            # save the local methods used by method
            self.__using_methods.clear()
            self.__check_method_use(node)
            self.__use2.append(self.__using_methods[:])

        self.__in_function = False

    def visit_Assign(self, node: ast.Assign):
        """
        When visit Assign node, if node is outside of class or function, save variable's name. \n
        This function is working when step is 1. \n
        :param node: Assign node
        :return: None
        """
        if self.__in_class is False and self.__in_function is False:
            if self.step == 1:
                self.__global_variable_check(node)

    def visit_AnnAssign(self, node: ast.AnnAssign):
        """
        When visit AnnAssign node, if node is outside of class or function, save variable's name. \n
        This function is working when step is 1. \n
        :param node: AnnAssign node
        :return: None
        """
        if self.__in_class is False and self.__in_function is False:
            if self.step == 1:
                self.__global_variable_check(node)

    ###################
    # Private Methods #
    ###################

    # 1st visit
    def __variable_check(self, node: ast.ClassDef):
        """
        Check class' class variable and instance variable. \n
        :param node: ClassDef node to check
        :return: None
        """
        for item in ast.walk(node):
            if isinstance(item, ast.Assign):
                self.__class_variable_check(item)
            elif isinstance(item, ast.FunctionDef):
                if item.name == '__init__':
                    self.__instance_variable_check(item)
                break

    def __class_variable_check(self, node: ast.Assign):
        """
        Check class' class variable. \n
        :param node: Assign node to check variable's name
        :return: None
        """
        for item in node.targets:
            if isinstance(item, ast.Name):
                self.__variables.append(item.id)

    def __instance_variable_check(self, node: (ast.FunctionDef, ast.AsyncFunctionDef)):
        """
        Check class' instance variable. \n
        :param node: FunctionDef node with name '__init__'
        :return: None
        """
        for item in node.body:
            if isinstance(item, ast.Assign):
                for target in item.targets:
                    if isinstance(target, ast.Attribute):
                        if isinstance(target.value, ast.Name):
                            if target.value.id == 'self':
                                if not (target.attr in self.__variables):
                                    self.__variables.append(target.attr)

    def __global_variable_check(self, node: (ast.Assign, ast.AnnAssign)):
        """
        Check global variables in target file. \n
        :param node: Assign or AnnAssign node
        :return: None, Save global variables name in list(global_variables)
        """
        if isinstance(node, ast.Assign):
            for target in node.targets:
                for name in ast.walk(target):
                    if isinstance(name, ast.Name):
                        if not (name.id in self.global_variables):
                            self.global_variables.append(name.id)
        elif isinstance(node, ast.AnnAssign):
            if isinstance(node.target, ast.Name):
                if not (node.target.id in self.global_variables):
                    self.global_variables.append(node.target.id)

    # 2nd visit
    def __check_class_use(self, node: ast.ClassDef):
        """
        Check which classes used in this class. \n
        :param node: ClassDef node to check
        :return: None
        """
        base = []
        for name in node.bases:
            if isinstance(name, ast.Name):
                base.append(name.id)
        for item in ast.walk(node):
            if isinstance(item, ast.Name):
                if (item.id in self.class_names) and not (item.id in self.__using_classes):
                    if not (item.id in base) and item.id != node.name:
                        self.__using_classes.append(item.id)

    def __check_variable_use(self, node: (ast.FunctionDef, ast.AsyncFunctionDef)):
        """
        Check which variables used in this function. \n
        :param node: FunctionDef node to check
        :return: None
        """
        for item in ast.walk(node):
            if isinstance(item, ast.Attribute):
                if (item.attr in self.variables_in_class[self.__current_class]) \
                        and not (item.attr in self.__use1) \
                        and not (item.attr in self.__using_variables):
                    self.__using_variables.append(item.attr)

    def __check_method_use(self, node: (ast.FunctionDef, ast.AsyncFunctionDef)):
        """
        Check which methods used in this function. \n
        :param node: FunctionDef node to check
        :return: None
        """
        for item in ast.walk(node):
            item_ast = item
            if isinstance(item, ast.Call):
                for var in ast.walk(item_ast):
                    if isinstance(var, ast.Attribute):
                        if isinstance(var.value, ast.Name):
                            if var.value.id != 'self' and var.value.id != self.__current_class:
                                continue
                        if (var.attr in self.methods_in_class[self.__current_class]) \
                                and not (var.attr in self.__use2) \
                                and not (var.attr in self.__using_methods):
                            self.__using_methods.append(var.attr)

    def __check_global_variable_use(self, node: ast.ClassDef):
        """
        Check which global variable used in this class. \n
        :param node: ClassDef node to check
        :return: None
        """
        global_var = []
        for global_item in ast.walk(node):
            if isinstance(global_item, ast.Global):
                for name in global_item.names:
                    global_var.append(name)

        for global_assign in ast.walk(node):
            if isinstance(global_assign, ast.Assign):
                for target in global_assign.targets:
                    for item in ast.walk(target):
                        if isinstance(item, ast.Name):
                            if item.id in global_var:
                                self.__use3.append(item.id)
            elif isinstance(global_assign, ast.AugAssign):
                if isinstance(global_assign.target, ast.Name):
                    if global_assign.target.id in global_var:
                        self.__use3.append(global_assign.target.id)


class ComplexityCounter:
    """
    Class for calculate complexity. (wmc, cbo, rfc, lcom)
    """
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

    @staticmethod
    def parse_file(filepath):
        """
        Parsing Python files to AST nodes. \n
        :param filepath: Path of file to parse
        :return: AST node
        """
        with open(filepath, "r", encoding="UTF-8") as f:
            ptree = ast.parse(f.read(), filename=filepath)
        f.close()
        return ptree

    def wmc(self, class_name):
        """
        Calculate 'wmc' complexity. \n
        :param class_name: Name of class to analyze
        :return: None
        """
        if class_name in self.class_names:
            index = self.class_names.index(class_name)
            self.wmc_value.insert(index, len(self.analyzer.methods_in_class[class_name]))

    def cbo(self, class_name):
        """
        Calculate 'cbo' complexity. \n
        :param class_name: Name of class to analyze
        :return: None
        """
        cbo_value = 0
        cbo_list = []
        if class_name in self.class_names:
            index = self.class_names.index(class_name)
            using_classes = self.analyzer.using_class
            using_global_var = self.analyzer.using_global_variable
            cbo_list.extend(using_classes[class_name][:])

            for name in using_classes:
                if name != class_name:
                    if class_name in using_classes[name]:
                        cbo_list.append(name)
            cbo_value += len(cbo_list)

            for name in using_global_var:
                if name != class_name:
                    intersection = set(using_global_var[class_name]) & set(using_global_var[name])
                    if not self.is_empty(intersection) and not (name in cbo_list):
                        cbo_value += 1

            self.cbo_value.insert(index, cbo_value)

    def rfc(self, class_name):
        """
        Calculate 'rfc' complexity. \n
        :param class_name: Name of class to analyze
        :return: None
        """
        if class_name in self.class_names:
            index = self.class_names.index(class_name)
            used_method = self.analyzer.using_method[class_name]
            temp = []
            M = len(used_method)
            for i in range(M):
                if not used_method[i]:
                    continue
                if self.is_empty(set(temp) & set(used_method[i])):
                    temp.extend(used_method[i])
                else:
                    temp.extend(list(set(used_method[i]) - set(temp)))
            L = len(temp)
            rfc_value = M + L
            self.rfc_value.insert(index, rfc_value)

    def lcom(self, class_name):
        """
        Calculate 'lcom' complexity. \n
        :param class_name: Name of class to analyze
        :return: None
        """
        Q = 0
        P = 0
        if class_name in self.class_names:
            index = self.class_names.index(class_name)
            all_combinations = list(combinations(self.analyzer.using_variable[class_name], 2))
            for aTuple in all_combinations:
                combi_set = set(aTuple[0]) & set(aTuple[1])
                if self.is_empty(combi_set):
                    P += 1
                else:
                    Q += 1
            if P <= Q:
                self.lcom_value.insert(index, 0)
            else:
                self.lcom_value.insert(index, P - Q)

    @staticmethod
    def is_empty(item):
        """
        Check set is empty or not. \n
        :param item: Set to check
        :return: bool
        """
        return item == set()

    def run(self):
        """
        Execute complexity methods. \n
        :return: None
        """
        for name in self.class_names:
            self.wmc(name)
            self.cbo(name)
            self.rfc(name)
            self.lcom(name)

    def write(self, outfile):
        """
        Write complexity value in outfile. \n
        :param outfile: File to write complexity information
        :return: None
        """
        outfile = open(outfile, "w", encoding="UTF-8")
        for name in self.class_names:
            index = self.class_names.index(name)
            outfile.write(name + ":\n")
            outfile.write("   - wmc: %d\n" % self.wmc_value[index])
            outfile.write("   - cbo: %d\n" % self.cbo_value[index])
            outfile.write("   - rfc: %d\n" % self.rfc_value[index])
            outfile.write("   - lcom: %d\n" % self.lcom_value[index])


def main():
    if len(sys.argv) < 3:
        print(f"Usage: {sys.argv[0]} <in.file> <out.file>\n")
        print("<in.file> must be written in Python.\n")
        exit(1)

    infile = sys.argv[1]
    outfile = sys.argv[2]
    oom_counter = ComplexityCounter(infile)
    oom_counter.run()
    oom_counter.write(outfile)


if __name__ == "__main__":
    main()
