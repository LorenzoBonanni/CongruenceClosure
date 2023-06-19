import re
from math import ceil

from pysmt.smtlib.parser import SmtLibParser
from sympy.logic.boolalg import *
from sympy.core.relational import Equality, Unequality
from sympy.core.function import UndefinedFunction
from sympy import parse_expr


class Parser:
    def __init__(self, path: str):
        self.smt_parser = SmtLibParser()
        self.script = SmtLibParser.get_script_fname(self.smt_parser, path)
        self.op2str = {
            Or: ' | ',
            And: ' & ',
            Equality: ' = ',
            Unequality: ' != '
        }

    def replace_ineq(self, text):
        idx_negative = re.finditer('!', text)
        new_str = text
        for idx in idx_negative:
            pos = idx.start()
            sub = text[pos:]
            eq_shift = sub.find('=')
            new_str = text[:pos + eq_shift] + '!=' + text[pos + eq_shift + 1:]
            new_str = new_str[:pos] + new_str[pos + 1:]
        return new_str

    def smt_to_sympy_string(self, expr):
        expr = self.replace_ineq(expr)
        expr = expr.replace(' = ', ' == ')
        return expr

    def to_string(self, root, string: list):
        """
        Converts a Formula written in sympy to a string
        :param root: the root of the subtree
        :param string: the string containing
        :return:
        """
        arguments = root.args
        if root.func.is_Symbol or isinstance(root.func, UndefinedFunction):
            func = root.name
        else:
            string.append('(')
            func = self.op2str[root.func]

        if len(arguments) == 0:
            string.append(func)
            return string
        n_symbols = ceil(len(arguments) / 2)
        skip_symbol = False
        additional_parenthesis = False
        for node in arguments:
            if isinstance(root.func, UndefinedFunction):
                skip_symbol = True
                string.append(func)
                string.append('(')
                n_symbols -= 1
            string = self.to_string(node, string)
            if n_symbols > 0 and not skip_symbol:
                string.append(func)
                n_symbols -= 1
        string.append(')')
        if additional_parenthesis:
            string.append(')')
        return string

    def parse(self):
        expr = self.script.get_strict_formula().serialize()
        expr = self.smt_to_sympy_string(expr)
        # convert string expression into sympy object
        expr = parse_expr(expr, evaluate=False)
        print(f"INPUT EXPRESSION:\n{expr}")
        # convert expression into dnf
        dnf_expr = to_dnf(expr)
        print(f"DNF EXPRESSION:\n{dnf_expr}")
        out = ''.join(self.to_string(dnf_expr, []))
        return out
