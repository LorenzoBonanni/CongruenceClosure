import sys
import time
from pathlib import Path

import matplotlib
import pandas as pd

from parser import Parser
from solver import CongruenceClosureAlgorithm
from utils import get_positive_negative_subsets, print_and_write


def main():
    matplotlib.use('TkAgg')
    file_path = sys.argv[1]
    plots = len(sys.argv) > 2 and sys.argv[2] == '-p'
    print(f"INPUT FILE: {file_path}")
    start = time.time()
    parser = Parser(path=file_path, plots=plots)
    dnf_expr, nodes, dict_created_formulas, ground_truth = parser.parse()
    ground_truth = ground_truth.upper()
    f_plus, f_minus = get_positive_negative_subsets(dnf_expr, dict_created_formulas)
    solver = CongruenceClosureAlgorithm(parser.id_to_node, f_plus, f_minus)
    result = solver.solve()
    end = time.time()
    time_elapsed = end - start
    print_and_write(text=f"Result: {result}\n"
                         f"Ground Truth: {ground_truth}\n"
                         f"Clauses in Dnf: {len(f_plus) + len(f_minus)}\n"
                         f"Time: {round(time_elapsed, 5)} s",
                    path=file_path
                    )
    out = {"Result": result,
           "Ground Truth": ground_truth,
           "Clauses": len(f_plus) + len(f_minus),
           "Time": {round(time_elapsed, 5)}
           }
    df = pd.Series(out)
    df.to_csv(f'./outputs/csv/{Path(file_path).stem}.csv')
    print('*' * 100)


if __name__ == '__main__':
    main()
