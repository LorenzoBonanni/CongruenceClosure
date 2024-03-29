import itertools

from parser import Parser
from utils import get_positive_negative_subsets, print_and_write


class CongruenceClosureAlgorithm:
    def __init__(self, id_to_node, f_plus, f_minus):
        self.id_to_node = id_to_node
        self.f_plus = f_plus
        self.f_minus = f_minus

    def find(self, id1):
        n = self.id_to_node[id1]
        if id1 == n.find_id:
            return id1
        return self.find(n.find_id)

    def union(self, id1, id2):
        n1 = self.id_to_node[self.find(id1)]
        n2 = self.id_to_node[self.find(id2)]

        # delete the one with largest ccpar
        if len(n2.ccpar) > len(n1.ccpar):
            n1.find_id = n2.find_id
            n2.ccpar = n2.ccpar.union(n1.ccpar)
            n1.ccpar = set()
        else:
            n2.find_id = n1.find_id
            n1.ccpar = n1.ccpar.union(n2.ccpar)
            n2.ccpar = set()

    def ccpar(self, id1):
        return self.id_to_node[self.find(id1)].ccpar

    def congruent(self, id1, id2):
        n1 = self.id_to_node[self.find(id1)]
        n2 = self.id_to_node[self.find(id2)]
        return n1.fn == n2.fn \
            and len(n1.args) == len(n2.args) \
            and all([self.find(n1.args[i]) == self.find(n2.args[i]) for i in range(len(n1.args))])

    def merge(self, id1: int, id2: int):
        if self.find(id1) != self.find(id2):
            p1 = self.ccpar(id1)
            p2 = self.ccpar(id2)
            self.union(id1, id2)
            for t1, t2 in itertools.product(p1, p2):
                if self.find(t1) != self.find(t2) and self.congruent(t1, t2):
                    self.merge(t1, t2)

    def solve(self):
        for s_i, t_i in self.f_plus:
            if (s_i, t_i) in self.f_minus or (t_i, s_i) in self.f_minus:
                return "UNSAT (Forbiddend List)"
            self.merge(s_i, t_i)
        for s_i, t_i in self.f_minus:
            if self.find(s_i) == self.find(t_i):
                return "UNSAT"
        return "SAT"
