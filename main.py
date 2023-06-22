import sys
import time

import matplotlib

from parser import Parser
from solver import CongruenceClosureAlgorithm
from utils import get_positive_negative_subsets, print_and_write


def main():
    matplotlib.use('TkAgg')
    file_path = sys.argv[1]
    plots = len(sys.argv) > 2 and sys.argv[2] == '-p'
    start = time.time()
    parser = Parser(path=file_path, plots=plots)
    dnf_expr, nodes, dict_created_formulas = parser.parse()
    f_plus, f_minus = get_positive_negative_subsets(dnf_expr, dict_created_formulas)
    solver = CongruenceClosureAlgorithm(parser.id_to_node, f_plus, f_minus)
    result = solver.solve()
    end = time.time()
    time_elapsed = end - start
    print_and_write(text=f"Result: {result}\n"
                         f"Time: {round(time_elapsed, 5)} s", path=file_path)
    print('*' * 100)


if __name__ == '__main__':
    main()
