from pathlib import Path

import networkx as nx
import numpy as np
from matplotlib import pyplot as plt
from sympy.core.relational import Equality, Unequality


def get_positive_negative_subsets(equation, dict_created_formulas):
    equalities = equation.atoms(Equality, Unequality)
    equalities = list(equalities)
    f_plus = []
    f_minus = []
    for eq in equalities:
        arguments = [dict_created_formulas[str(arg)].node_id for arg in eq.args]
        if type(eq) is Equality:
            f_plus.append(arguments)
        else:
            f_minus.append(arguments)
    return f_plus, f_minus


def print_and_write(text, path):
    print(text)
    file = 'outputs/' + Path(path).stem + '.out'
    with open(file, 'w') as f:
        f.write(text)


def plot_nodes(id_to_node):
    nodes = list(id_to_node.values())
    # Create an empty graph
    G = nx.DiGraph()

    # Add nodes to the graph with labels as node ids
    for node in nodes:
        G.add_node(node.node_id)

    # Add edges to the graph based on the args attribute of each node
    for node in nodes:
        for arg in node.args:
            G.add_edge(node.node_id, arg)

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
    plt.title("Equation DAG")
    plt.show()
