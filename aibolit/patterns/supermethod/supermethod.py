import javalang


class SuperMethod:

    def __init__(self):
        pass

    def __file_to_ast(self, filename: str) -> javalang.ast.Node:
        """
        Takes path to java class file and returns AST Tree
        :param filename:
        :return: Tree
        """
        with open(filename, encoding='utf-8') as file:
            res = javalang.parse.parse(file.read())
        return res

    def value(self, filename: str):
        """
        Iterates over functions and finds super.func() calls.
        Javalang doesn't have code line for super.func() call,
        that's why we can only count the first match of a call inside some function.
        It has MULTIPLE MATCHES if we call super.func() inside a ANONYMOUS CLASS.
        :param filename:
        :return: Lines of code
        """
        results = []
        tree = self.__file_to_ast(filename)
        with open(filename, encoding='utf-8') as file:
            text_lines = file.readlines()
        for _, method_decl_node in tree.filter(javalang.tree.MethodDeclaration):
            code_line = method_decl_node.position.line
            for _, super_method_inv in method_decl_node.filter(javalang.tree.SuperMethodInvocation):
                str_to_find = 'super.{method_name}({arguments})'.format(
                    method_name=super_method_inv.member,
                    arguments=','.join(super_method_inv.arguments)).strip()
                for iter, line in enumerate(text_lines[code_line - 1:]):
                    string_strip = line.strip().replace('\n', '').replace('\t', '')
                    if string_strip.find(str_to_find) > -1:
                        results.append(code_line + iter)
                        break
        return results

    def __traverse(self, tree, results):
        descendants = tree.children
        for children in descendants:
            if isinstance(children, tuple) or isinstance(children, list):
                for item in children:
                    if isinstance(item, javalang.tree.SuperMethodInvocation):
                        results.append([item.member])
                    else:
                        self.__traverse(item, results)
        return results