import numpy as np
import networkx as nx


def phi(gr, nodes, other=None):
    if gr.directed():
        ind_i = np.arange(gr.size())[[node in nodes for node in gr.get_ids()]]
        if other is not None:
            ind_j = np.arange(gr.size())[[node in other for node in gr.get_ids()]]
        else:
            ind_j = np.arange(gr.size())[[node not in nodes for node in gr.get_ids()]]
        pi = gr.get_stat_dist()
        c = np.sum(pi[ind_i])
        v = np.sum(pi[ind_j])

        p = gr.get_prob_matrix()
        w = np.multiply(p, pi)

        p1 = np.sum(w[np.ix_(ind_j, ind_i)])
        p2 = np.sum(w[np.ix_(ind_i, ind_j)])
        return np.max([p1 / c, p2 / v])
    else:
        if gr.size() == len(nodes):
            return 0
        return nx.algorithms.cuts.conductance(gr.get_nx_graph(), nodes, other)


def conductance(gr, start_node=None, al=False):
    if start_node is None:
        if al:
            comm = gr.get_ids(stable=True)
        else:
            comm = np.random.choice(
                gr.get_ids(stable=True),
                replace=False,
                size=max([int(gr.size() / 2), 1]),
            )

        reses = []
        for node in comm:
            reses.append(conductance_iter(gr, node))

        reses = np.array(reses)
        if reses.size == 0:
            return 1

        reses = reses[reses > 0]
        if reses.size == 0:
            return 1
        return np.min(reses[reses > 0])
    else:
        return conductance_iter(gr, start_node)


def conductance_iter(gr, start_node):
    comm = [start_node]

    rs = 1
    rs_old = 2
    while rs_old > rs and len(comm) <= gr.size() / 2:
        rs_old = rs
        tst_add = []
        comm_add = []
        comm_del = []
        tst_del = []

        for node_out in gr.get_out_degrees(comm, un=True):
            if node_out in comm:
                continue

            try:
                tst_add.append(phi(gr, comm + [node_out]))
                comm_add.append(comm + [node_out])
            except:
                continue

        for node in comm:
            nw_comm = comm.copy()
            nw_comm.remove(node)
            if len(nw_comm) == 0:
                continue

            gr_ = gr.subgraph(nw_comm)
            if nx.number_connected_components(gr_.get_nx_graph()) != 1:
                continue

            try:
                r = phi(gr_, nw_comm)
                if r > 0:
                    tst_del.append(r)
                    comm_del.append(nw_comm)
            except:
                continue

        if len(tst_del) == 0:
            if len(tst_add) == 0:
                break

            if np.min(tst_add) < rs and np.min(tst_add) != 0:
                rs = np.min(tst_add)
                comm = comm_add[np.argmin(tst_add)]
            continue

        if np.min(tst_del) < rs and len(tst_add) == 0:
            rs = np.min(tst_del)
            comm = comm_del[np.argmin(tst_del)]
            continue

        if np.min(tst_add) <= np.min(tst_del):
            if np.min(tst_add) < rs:
                rs = np.min(tst_add)
                comm = comm_add[np.argmin(tst_add)]
                continue
        else:
            if np.min(tst_del) < rs:
                rs = np.min(tst_del)
                comm = comm_del[np.argmin(tst_del)]
                continue
    return rs


def weak_conductance(gr, c):
    return np.min(
        [weak_conductance_node(gr, node, gr.size() / c - 1) for node in gr.get_ids()]
    )


def weak_conductance_nodes(gr, attr, c):
    for node in gr.get_ids():
        gr.set_attr(node, attr, 0)

    for node in gr.get_ids():
        weak_conductance_node(gr, attr, node, gr.size() / c - 1)


def weak_conductance_nodes_comm(gr, attr, c_attr=None):
    ids = gr.get_ids(stable=True)
    for node in ids:
        gr.set_attr(node, attr, 1)
        gr.set_attr(node, attr + "mn", 0)

    if c_attr is None:
        for node in ids:
            if gr.get_attr(node, attr + "mn") == 0:
                weak_conductance_node_comm(gr, attr, (node,), ids)
    else:
        attrs = gr.get_attributes(c_attr)
        for un in np.unique(attrs):
            nodes = ids[attrs == un]
            print(un, nodes.size)
            for node in nodes:
                if gr.get_attr(node, attr + "mn") == 0:
                    weak_conductance_node_comm(gr, attr, (node,), nodes)


def weak_conductance_node(gr, attr, node, c):
    print(node, "!")
    comms = [(node,)]
    rs = 0

    for _ in np.arange(gr.size() - 2):
        new_comms = []
        conds = []
        dicts = {}

        print(_, rs, len(comms))
        for comm in comms:
            for node_out in gr.get_out_degrees(comm, un=True):
                if node_out in comm:
                    continue
                if _ >= c:
                    cond = conductance(gr.subgraph(list(comm) + [node_out]), al=True)
                    if cond <= rs:
                        continue
                    conds.append(cond)
                    new_comms.append(tuple(list(comm) + [node_out]))
                else:
                    cns = conductance(
                        gr.subgraph(list(comm) + [node_out]),
                        al=np.random.uniform(0, 1, 1) > 0.5,
                    )
                    if cns == 0:
                        continue
                    dicts.update({tuple(list(comm) + [node_out]): cns})

        if _ >= c:
            if len(conds) == 0:
                break

            rs = np.max(conds)
            comms_ = []
            for i in np.arange(len(conds)):
                if conds[i] == rs:
                    comms_.append(new_comms[i])

            if len(comms_) == 0:
                for comm in comms:
                    for nd in comm:
                        if rs > gr.get_attr(nd, attr):
                            gr.set_attr(nd, attr, rs)
                break
            comms = comms_
        else:
            rs_ = np.max(list(dicts.values()))
            comms = []
            count = 0
            for ky in dicts.keys():
                if rs_ == dicts.get(ky) and (
                    np.random.uniform(0, 1, 1) > 0.5 or count <= 50
                ):
                    count += 1
                    comms.append(ky)

                if count >= 2000:
                    break

    if rs > gr.get_attr(node, attr):
        gr.set_attr(node, attr, rs)


def weak_conductance_node_comm(gr, attr, prt, com, rs=(1, 1)):
    new_comms = {}

    for node_out in gr.get_out_degrees(prt, un=True):
        if node_out in prt or node_out not in com:
            continue

        cmm = tuple(np.sort(list(prt) + [node_out]))
        new_comms.update({cmm: conductance(gr.subgraph(cmm), al=True)})

    if len(new_comms) != 0:
        if np.max(list(new_comms.values())) <= rs[0] != 1 and rs[0] >= rs[1]:
            for node in prt:
                if gr.get_attr(node, attr) > rs[0]:
                    print(node, rs[0])
                    gr.set_attr(node, attr, rs[0])
                    gr.set_attr(node, attr + "mn", 1)
            return
        else:
            for comm in new_comms.keys():
                if (new_comms[comm] >= rs[0] or rs[0] == 1) and (
                    np.sum(gr.get_attributes(attr + "mn", comm) == 1) != len(comm)
                ):
                    weak_conductance_node_comm(
                        gr, attr, comm, com, rs=(new_comms[comm], rs[0])
                    )
