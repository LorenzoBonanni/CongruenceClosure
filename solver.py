import itertools
from dataclasses import dataclass

id_to_node = {}


class CongruenceClosureAlgorithm:

    def find(self, id1):
        if id1 == id_to_node[id1].find_id:
            return id1
        else:
            id_to_node[id1].find()

    def union(self, id1, id2):
        n1 = id_to_node[self.find(id1)]
        n2 = id_to_node[self.find(id2)]
        n1.find_id = n2.find_id
        n2.ccpar = n1.ccpar + n2.ccpar
        n1.ccpar = None

    def ccpar(self, id1):
        return id_to_node[self.find(id1)].ccpar

    def congruent(self, id1, id2):
        n1 = id_to_node[self.find(id1)]
        n2 = id_to_node[self.find(id2)]
        return n1.fn == n2.fn \
            and len(n1.args) == len(n2.args) \
            and all([self.find(n1.args[i]) == self.find(n2.args[i]) for i in range(len(n1.args))])

    def merge(self, id1: int, id2: int):
        if self.find(id1) != self.find(id2):
            p1 = self.ccpar(id1)
            p2 = self.ccpar(id2)
            for t1, t2 in itertools.product(p1, p2):
                if self.find(t1) != self.find(t2) and self.congruent(t1, t2):
                    self.merge(t1, t2)



@dataclass
class Node:
    node_id: int
    fn: str
    args: list
    find_id: int
    ccpar: tuple[int]

    def __post_init__(self):
        if len(self.ccpar) != 0:
            self.find_id = self.node_id
        id_to_node[self.node_id] = self
