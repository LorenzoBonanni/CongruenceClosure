from parser import Parser
from solver import CongruenceClosureAlgorithm
from utils import get_positive_negative_subsets


def main():
    file_path = "inputs/input1.smt2"
    parser = Parser(path=file_path)
    dnf_expr, nodes, dict_created_formulas = parser.parse()
    f_plus, f_minus = get_positive_negative_subsets(dnf_expr, dict_created_formulas)
    solver = CongruenceClosureAlgorithm(parser.id_to_node, f_plus, f_minus)
    result = solver.solve()
    print(f"Result: {result}")

if __name__ == '__main__':
    main()
