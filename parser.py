import re
from dataclasses import dataclass

from pysmt.smtlib.parser import SmtLibParser
from sympy import parse_expr
from sympy.core.function import Function
from sympy.core.symbol import Symbol
from sympy.logic.boolalg import *

from utils import plot_nodes


@dataclass
class Node:
    node_id: int
    fn: str
    args: list
    find_id: int
    ccpar: set

    def __post_init__(self):
        if len(self.ccpar) != 0:
            self.find_id = self.node_id


class Parser:
    def __init__(self, path: str, plots: bool):
        self.smt_parser = SmtLibParser()
        self.script = self.smt_parser.get_script_fname(path)
        self.id_to_node = {}
        self.plots = plots

    def replace_ineq(self, text):
        idx_negative = re.finditer('!', text)
        new_str = text[:]
        for idx in idx_negative:
            pos = idx.start()
            sub = new_str[pos:]
            eq_shift = sub.find('=')
            new_str = new_str[:pos + eq_shift] + '!=' + new_str[pos + eq_shift + 1:]
            new_str = new_str[:pos] + new_str[pos + 1:]
        return new_str

    def smt_to_sympy_string(self, expr):
        expr = self.replace_ineq(expr)
        expr = expr.replace(' = ', ' == ')
        return expr

    def generate_dag(self, atoms):
        dict_created_formulas = {}
        counter = 0

        # Initialize a counter for node_ids
        atoms = sorted([(a, str(a)) for a in atoms], key=lambda x: len(x[1]))
        for atom, full_str in atoms:
            str_atom = atom.name
            args = atom.args
            if dict_created_formulas.get(full_str, None) is None:
                # Increment the counter before creating a node
                counter += 1
                node = Node(node_id=counter, fn=str_atom, find_id=counter, args=[], ccpar=set())
                self.id_to_node[counter] = node
                dict_created_formulas[full_str] = node
                if len(args) > 0:
                    for arg in args:
                        child = dict_created_formulas[str(arg)]
                        node.args.append(child.node_id)
        return dict_created_formulas

    def populate_ccpar(self, nodes):
        for node in nodes:
            for arg in node.args:
                self.id_to_node[arg].ccpar.add(node.node_id)

    def parse(self):
        expr = self.script.get_strict_formula().serialize()
        result = [cmd for cmd in self.script.commands if ((cmd.name == "set-info") and (":status" in cmd.args))]
        ground_truth = result[0].args[1]
        expr = self.smt_to_sympy_string(expr)
        # convert string expression into sympy object
        expr = parse_expr(expr, evaluate=False)
        print(f"INPUT EXPRESSION:\n{expr}")
        dnf_expr = expr
        if not is_dnf(expr):
            dnf_expr = to_dnf(expr)
        atoms = dnf_expr.atoms(Function, Symbol)
        dict_created_formulas = self.generate_dag(atoms)
        nodes = list(self.id_to_node.values())
        self.populate_ccpar(nodes)
        if self.plots:
            plot_nodes(self.id_to_node)
        print(f"DNF EXPRESSION:\n{dnf_expr}")

        return dnf_expr, nodes, dict_created_formulas, ground_truth
