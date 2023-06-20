import re

from pysmt.smtlib.parser import SmtLibParser
from sympy import parse_expr, to_dnf
from sympy.core.relational import Equality, Unequality
from sympy.logic.boolalg import Or, And, to_cnf


class Parser:
    def __init__(self, path: str):
        self.smt_parser = SmtLibParser()
        self.script = self.smt_parser.get_script_fname(path)
        self.op2str = {
            Or: ' | ',
            And: ' & ',
            Equality: ' == ',
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

    def to_string(self, root):
        if isinstance(root, Or):
            return "(" + self.op2str[Or].join(self.to_string(arg) for arg in root.args) + ")"
        elif isinstance(root, And):
            return "(" + self.op2str[And].join(self.to_string(arg) for arg in root.args) + ")"
        elif isinstance(root, (Equality, Unequality)):
            return "(" + self.to_string(root.args[0]) + self.op2str[type(root)] + self.to_string(root.args[1]) + ")"
        else:
            return str(root)

    def parse(self):
        expr = self.script.get_strict_formula().serialize()
        expr = self.smt_to_sympy_string(expr)
        # convert string expression into sympy object
        expr = parse_expr(expr, evaluate=False)
        print(f"INPUT EXPRESSION:\n{expr}")
        dnf_expr = to_cnf(expr)
        print(f"DNF EXPRESSION:\n{dnf_expr}")
        out = self.to_string(dnf_expr)
        return out
