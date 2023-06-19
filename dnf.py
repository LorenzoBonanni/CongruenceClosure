import re
from math import floor, ceil

from sympy.core.relational import Equality, Unequality
from pysmt.smtlib.parser import SmtLibParser
from sympy import parse_expr
from sympy.logic.boolalg import *


def replace_ineq(text):
    idx_negative = re.finditer('!', text)
    new_str = text
    for idx in idx_negative:
        pos = idx.start()
        sub = text[pos:]
        eq_shift = sub.find('=')
        new_str = text[:pos + eq_shift] + '!=' + text[pos + eq_shift + 1:]
        new_str = new_str[:pos] + new_str[pos + 1:]
    return new_str


def smt_to_sympy(expr):
    expr = replace_ineq(expr)
    expr = expr.replace(' = ', ' == ')
    return expr


roba = {
    Or: ' | ',
    And: ' & ',
    Equality: ' = ',
    Unequality: ' != '
}


def to_string(root, string: list):
    """
    Converts a Formula written in sympy to a string
    :param root: the root of the subtree
    :param string: the string containing
    :return:
    """
    arguments = root.args
    if not root.func.is_Symbol:
        string.append('(')
        func = roba[root.func]
    else:
        func = root.name

    if len(arguments) == 0:
        string.append(func)
        return string
    n_symbols = ceil(len(arguments) / 2)
    for node in arguments:
        string = to_string(node, string)
        if n_symbols > 0:
            string.append(func)
            n_symbols -= 1
    string.append(')')
    return string


smt_parser = SmtLibParser()
file_path = "inputs/input3.smt2"
expr = smt_parser.get_script_fname("inputs/eq_diamond2.smt2")
expr = expr.get_strict_formula()
expr = expr.serialize()
expr = smt_to_sympy(expr)

a = parse_expr(expr, evaluate=False)
b = to_dnf(a),
print(b)
out = to_string(b, [])
print(''.join(out))
