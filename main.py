from parser import Parser
from utils import get_positive_negative_subsets


def main():
    file_path = "inputs/input1.smt2"
    dnf_expr, nodes, dict_created_formulas = Parser(path=file_path).parse()
    f_plus, f_minus = get_positive_negative_subsets(dnf_expr)



if __name__ == '__main__':
    main()
