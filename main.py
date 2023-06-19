from pysmt.smtlib.parser import SmtLibParser
from parser import Parser
smt_parser = SmtLibParser()

file_path = "inputs/input3.smt2"
p = Parser(path=file_path)
parsed = p.parse()
print(parsed)
