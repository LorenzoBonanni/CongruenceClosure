import re
from dataclasses import dataclass

import networkx as nx
import numpy as np
from matplotlib import pyplot as plt, rcParams
from pysmt.smtlib.parser import SmtLibParser
from sympy import parse_expr
from sympy.core.function import Function
from sympy.core.relational import Equality, Unequality
from sympy.core.symbol import Symbol
from sympy.logic.boolalg import *


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
        if not is_dnf(expr):
            dnf_expr = to_dnf(expr, simplify=True)
        else:
            dnf_expr = expr
        print(f"DNF EXPRESSION:\n{dnf_expr}")
        # out = self.to_string(dnf_expr)
        return dnf_expr


op2str = {
    Or: ' | ',
    And: ' & ',
    Equality: ' = ',
    Unequality: ' != '
}
edges = []
last_id = 0

# Initialize a dictionary to map atoms to node_ids
id_to_node = {}
leaf_nodes = {}
counter = 0


@dataclass
class Node:
    node_id: int
    fn: str
    args: list
    find_id: int
    ccpar: list

    def __post_init__(self):
        if len(self.ccpar) != 0:
            self.find_id = self.node_id
        id_to_node[self.node_id] = self





def generate_dag(atoms):
    dict_roba = {}
    counter = 0

    # Initialize a counter for node_ids
    atoms = sorted([(a, str(a)) for a in atoms], key=lambda x: len(x[1]))
    for atom, full_str in atoms:
        str_atom = atom.name
        args = atom.args
        if dict_roba.get(full_str, None) is None:
            # Increment the counter before creating a node
            counter += 1
            node = Node(node_id=counter, fn=str_atom, find_id=counter, args=[], ccpar=[])
            dict_roba[full_str] = node
            if len(args) > 0:
                for arg in args:
                    child = dict_roba[str(arg)]
                    node.args.append(child.node_id)


def get_string(node, string):
    string += node.fn
    contain_arg = len(node.args) != 0
    if contain_arg:
        string += '('
    for i, arg in enumerate(node.args):
        string += get_string(id_to_node[arg], '')
        if len(node.args) - (i + 1) > 0:
            string += ','
    if contain_arg:
        string += ')'
    return string


def plot_nodes(G):
    # nx.spring_layout(G)
    # Create a dictionary of labels based on the fn attribute of each node
    labels = {}
    for n in G.nodes():
        labels[n] = f'{id_to_node[n].fn}'

    pos = nx.spring_layout(G, scale=10, k=3 / np.sqrt(G.order()))
    d = dict(G.degree)
    nx.draw(G, pos,
            node_color='lightblue',
            nodelist=list(d.keys()),
            labels=labels,
            arrows=True
            )
    plt.show()


def get_positive_negative_subsets(equation):
    equalities = equation.atoms(Equality, Unequality)
    equalities = list(equalities)
    f_plus = []
    f_minus = []
    for eq in equalities:
        if type(eq) is Equality:
            f_plus.append(eq)
        else:
            f_minus.append(eq)
    return f_plus, f_minus


def build_dag(nodes):
    # Create an empty graph
    G = nx.DiGraph()

    # Add nodes to the graph with labels as node ids
    for node in nodes:
        G.add_node(node.node_id)

    # Add edges to the graph based on the args attribute of each node
    for node in nodes:
        for arg in node.args:
            G.add_edge(node.node_id, arg)

    return G


def remove_duplicates(G):
    G_copy = G.copy()
    for n in G.nodes:
        edges = [e[1] for e in G.out_edges(n)]
        for n1 in G.nodes:
            if n == n1:
                continue
            if G.out_degree[n] > 0 and G.out_degree[n1] > 0 and id_to_node[n].fn == id_to_node[n1].fn:
                edges1 = [e[1] for e in G.out_edges(n1)]
                if edges == edges1:
                    if G_copy.has_node(n1):
                        in_edges = [e[0] for e in G.in_edges(n1)]
                        for e in in_edges:
                            G_copy.add_edge(e, n)
                        G_copy.remove_node(n1)
    return G_copy


def main():
    file_path = "inputs/input4.smt2"
    parsed = Parser(path=file_path).parse()
    atoms = parsed.atoms(Function, Symbol)
    print(atoms)
    f_plus, f_minus = get_positive_negative_subsets(parsed)
    generate_dag(atoms)
    nodes = list(id_to_node.values())
    G = build_dag(nodes)
    plot_nodes(G)
    # new_G = remove_duplicates(G)
    # plot_nodes(new_G)


if __name__ == '__main__':
    main()
