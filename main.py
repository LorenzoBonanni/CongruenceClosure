from pysmt.smtlib.parser import SmtLibParser

smt_parser = SmtLibParser()

from parser import Parser

file_path = "inputs/input1.smt2"
p = Parser(path=file_path)
f_p, f_n = p.parse()

for f in f_p:
    si, ti = [_.strip() for _ in f.split('=')]
    print(si)
