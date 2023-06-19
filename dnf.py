import re
from math import floor, ceil

from sympy.core.relational import Equality, Unequality
from pysmt.smtlib.parser import SmtLibParser
from sympy import parse_expr
from sympy.logic.boolalg import *

smt_parser = SmtLibParser()
file_path = "inputs/input3.smt2"
expr = smt_parser.get_script_fname("inputs/eq_diamond2.smt2")
expr = expr.get_strict_formula()
expr = expr.serialize()



a = parse_expr(expr, evaluate=False)
b = to_dnf(a),
print(b)
out = to_string(b, [])
print(''.join(out))
