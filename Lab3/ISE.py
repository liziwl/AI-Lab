# encoding: utf-8
import copy
import graph
import random
import numpy as np


def sample(model, seed, graph):
    if model == 'IC':
        sample_list = []
        for i in range(0, 10000):
            sample_list.append(ic(seed, graph))
        return np.mean(sample_list)
    elif model == 'LT':
        sample_list = []
        for i in range(0, 10000):
            sample_list.append(lt(seed, graph))
        return np.mean(sample_list)
    else:
        return -1


def ic(seed_list, graph):
    activated = set(seed_list)
    activity = set(seed_list)
    count = len(activity)
    while len(activity) > 0:
        new_activity = set()
        for it in activity:
            neighbor = graph.get_neighbor(it)
            for nei in neighbor:
                if nei in activated:
                    # 除去已经激活的点
                    continue
                prob = random.random()
                if prob <= graph.get_weight(it, nei):
                    # if prob <= 1:
                    activated.add(nei)
                    new_activity.add(nei)
        count += len(new_activity)
        activity = new_activity
    return count


def lt(seed_list, graph):
    activated = set(seed_list)
    activity = set(seed_list)
    count = len(activity)
    while len(activity) > 0:
        new_activity = set()
        for it in activity:
            neighbor = graph.get_neighbor(it)
            for nei in neighbor:
                if nei in activated:
                    # 除去已经激活的点
                    continue
                parent = graph.get_parent(nei)
                w_total = 0
                for p in parent:
                    if p in activated:
                        w_total += graph.get_weight(p, nei) * random.random()
                if w_total >= random.random():
                    activated.add(nei)
                    new_activity.add(nei)
        count += len(new_activity)
        activity = new_activity
    return count


if __name__ == "__main__":
    d = graph.read_network("network.txt")
    # print d

    seed = graph.read_seed("seeds.txt")
    print seed

    d1 = graph.list2dict(d[2])
    graph.print_graph(d1)

    d2 = graph.inv_list2dict(d[2])

    test = graph.Graph(d1, d2)
    # seed = [30]
    print sample('IC', seed, test)

    print sample('LT', seed, test)
