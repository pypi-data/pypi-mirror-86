import numpy as np


class BasicGrowth:
    def __init__(self, graph, deg):
        self.gr = graph
        self.deg = deg

    def choice(self, gr, sz):
        return []

    def proceed(self, n, attr="cnt"):
        nw_graph = self.gr.clean_copy()
        for node in nw_graph.get_ids():
            nw_graph.set_attrs(node, attr, -1)

        count = self.gr.size()
        for _ in np.arange(n):
            print(_)
            if self.deg[0] == "const":
                nodes = self.choice(nw_graph, self.deg[1])
            else:
                nodes = self.choice(nw_graph, self.deg[0](self.deg[1]))

            for node in nodes:
                nw_graph.add_edge(str(count), node)
            nw_graph.set_attr(str(count), attr, _)
            count += 1
        return nw_graph
