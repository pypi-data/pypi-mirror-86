import numpy as np

from pge.model.growth.basic import BasicGrowth
from pge.model.growth.basic_fix import FixGrowth


class PAGrowth(BasicGrowth):
    def choice(self, graph, sz):
        probs = np.array([graph.count_in_degree(node) for node in graph.get_ids()])
        probs = probs / np.sum(probs)
        return np.random.choice(graph.get_ids(), sz, replace=False, p=probs)


class PAFixGrowth(FixGrowth):
    def choice(self, graph, sz):
        probs = np.array([graph.count_in_degree(node) for node in graph.get_ids()])
        probs = probs / np.sum(probs)
        return np.random.choice(graph.get_ids(), sz, replace=False, p=probs)
