from pysmt.smtlib.parser import SmtLibParser


class Parser:
    def __init__(self, path:str):
        self.smt_parser = SmtLibParser()
        self.script = SmtLibParser.get_script_fname(self.smt_parser, path)

    def parse(self):
        f = self.script.get_strict_formula()
        symbols = self.script.get_declared_symbols()

        # Get a list of Atoms and the Equations
        formulas = list(map(lambda x: x.serialize(), list(f.args())))
        atoms = list(map(lambda x: x.serialize(), list(f.get_atoms())))
        f_plus = []
        f_minus = []
        for f in formulas:
            if '!' in f[:2]:
                f_minus.append(f[3:-1].replace('=', '!='))
            else:
                f_plus.append(f)

        return f_plus, f_minus
