# encoding: utf-8
import copy
import time
import graph
import random
import numpy as np

FAST = 1
MEDIUM = 2
SLOW = 3


def sample(model, seed, network, speed=FAST):
    if speed == FAST:
        return evaluate_specific(model, seed, network, 100)
    elif speed == MEDIUM:
        return evaluate_specific(model, seed, network, 1000)
    else:
        return evaluate_specific(model, seed, network, 10000)


def evaluate_specific(model, seed, network, times):
    start = time.time()
    if model == 'IC':
        sample_list = []
        for i in range(0, times):
            sample_list.append(ic(seed, network))
        run_time = (time.time() - start)
        print "TIME: {}s".format(run_time)
        return np.mean(sample_list)
    elif model == 'LT':
        sample_list = []
        for i in range(0, times):
            sample_list.append(lt(seed, network))
        run_time = (time.time() - start)
        print "TIME: {}s".format(run_time)
        return np.mean(sample_list)
    else:
        return -1


def ic(seed_list, network):
    activated = set(seed_list)
    activity = set(seed_list)
    count = len(activity)
    while len(activity) > 0:
        new_activity = set()
        for it in activity:
            neighbor = network.get_neighbor(it)
            for nei in neighbor:
                if nei not in activated:  # 除去已经激活的点
                    prob = random.random()
                    if prob <= network.get_weight(it, nei):
                        activated.add(nei)
                        new_activity.add(nei)
        count += len(new_activity)
        activity = new_activity
    assert len(activated) == count
    return count


def lt(seed_list, network):
    activated = set(seed_list)
    activity = set(seed_list)
    thresh = network.get_thresh()
    count = len(activity)
    while len(activity) > 0:
        new_activity = set()
        for it in activity:
            neighbor = network.get_neighbor(it)
            for nei in neighbor:
                if nei not in activated:  # 除去已经激活的点
                    parent = network.get_parent(nei)
                    w_total = 0
                    for p in parent:
                        if p in activated:
                            w_total += network.get_weight(p, nei)
                    if w_total >= thresh[nei]:
                        activated.add(nei)
                        new_activity.add(nei)
        count += len(new_activity)
        activity = new_activity
    assert len(activated) == count
    return count


if __name__ == "__main__":
    d = graph.read_network("network.txt")
    # print d

    seed = graph.read_seed("seeds.txt")
    print seed

    d1 = graph.list2dict(d[2])
    graph.print_graph(d1)
    # print "-----------------------------"
    d2 = graph.inv_list2dict(d[2])
    # graph.print_graph(d2)

    test = graph.Graph(d1, d2)
    seed = [53, 56, 58, 62]  # 27.3075/31.8265
    seed = [28, 53, 56, 58]  # 27.077/31.31
    seed = [48, 53, 56, 58]  # 26.9996/ 32.7784
    seed = [50, 53, 56, 58]  # 27.0631/31.2291
    print sample('IC', seed, test)
    print sample('IC', seed, test, MEDIUM)
    print sample('IC', seed, test, SLOW)

    print sample('LT', seed, test)
    print sample('LT', seed, test, MEDIUM)
    print sample('LT', seed, test, SLOW)
