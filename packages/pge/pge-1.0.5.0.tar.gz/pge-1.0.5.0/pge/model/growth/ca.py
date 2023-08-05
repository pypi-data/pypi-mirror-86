import networkx as nx
import numpy as np

from pge.model.growth.basic import BasicGrowth
from pge.model.growth.basic_fix import FixGrowth


class CAGrowth(BasicGrowth):
    def __init__(self, graph, deg, alpha, eps):
        super().__init__(graph, deg)
        self.alpha = alpha
        self.eps = eps

    def choice(self, graph, sz):
        cs = nx.clustering(graph.get_nx_graph())
        probs = np.power(list(cs.values()), self.alpha) + self.eps
        probs = probs / np.sum(probs)
        return np.random.choice(list(cs.keys()), sz, replace=False, p=probs)


class CAFixGrowth(FixGrowth):
    def __init__(self, graph, deg, typ, alpha, eps):
        super().__init__(graph, deg, typ)
        self.alpha = alpha
        self.eps = eps

    def choice(self, graph, sz):
        cs = nx.clustering(graph.get_nx_graph())
        probs = np.power(list(cs.values()), self.alpha) + self.eps
        probs = probs / np.sum(probs)
        return np.random.choice(list(cs.keys()), sz, replace=False, p=probs)
