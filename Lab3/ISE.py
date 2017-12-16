# encoding: utf-8
import copy
import time
import graph
import random
import numpy as np
import options

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
        # print "TIME: {}s".format(run_time)
        return np.mean(sample_list)
    elif model == 'LT':
        sample_list = []
        for i in range(0, times):
            sample_list.append(lt(seed, network))
        run_time = (time.time() - start)
        # print "TIME: {}s".format(run_time)
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
            # neighbor = network.get_neighbor(it)
            if it in network.node_dict:
                neighbor = network.node_dict[it]
            else:
                neighbor = []
            for nei in neighbor:
                if nei not in activated:  # 除去已经激活的点
                    prob = random.random()
                    # if prob <= network.get_weight(it, nei):
                    if prob <= neighbor[nei]:
                        activated.add(nei)
                        new_activity.add(nei)
        count += len(new_activity)
        activity = new_activity
    assert len(activated) == count
    return count


def lt(seed_list, network):
    activated = set(seed_list)
    activity = set(seed_list)
    thresh = {}
    count = len(activity)
    while len(activity) > 0:
        new_activity = set()
        for it in activity:
            # neighbor = network.get_neighbor(it)
            if it in network.node_dict:
                neighbor = network.node_dict[it]
            else:
                neighbor = []
            for nei in neighbor:
                if nei not in activated:  # 除去已经激活的点
                    # parent = network.get_parent(nei)
                    parent = network.node_inv[nei]
                    w_total = 0
                    for p in parent:
                        if p in activated:
                            w_total += parent[p]
                            # w_total += network.get_weight(p, nei)
                    if nei not in thresh:
                        thresh[nei] = random.random()
                    if w_total >= thresh[nei]:
                        activated.add(nei)
                        new_activity.add(nei)
        count += len(new_activity)
        activity = new_activity
    assert len(activated) == count
    return count


def solver(network, seed, model, termination, utime, rand):
    random.seed(rand)
    data = graph.read_network(network)
    d1 = graph.list2dict(data[2])
    d2 = graph.inv_list2dict(data[2])
    grap = graph.Graph(d1, d2)
    seed_data = graph.read_seed(seed)

    if termination == 0:
        return sample(model, seed_data, grap, SLOW)
    elif termination == 1:
        sample_data = []
        start = time.time()
        sample_data.append(sample(model, seed_data, grap, MEDIUM))
        run_time = (time.time() - start)
        base_time = run_time + 0.5

        while run_time < utime - base_time:
            sample_data.append(sample(model, seed_data, grap, MEDIUM))
            run_time = (time.time() - start)

        # print "TIME: {}s".format(run_time)
        return np.mean(sample_data)


if __name__ == "__main__":
    # seed = [53, 56, 58, 62]  # 27.3075/31.8265
    # seed = [28, 53, 56, 58]  # 27.077/31.31
    # seed = [48, 53, 56, 58]  # 26.9996/ 32.7784
    # seed = [50, 53, 56, 58]  # 27.0631/31.2291
    # network = "network.txt"
    # seed = "seeds10.txt"
    # model = "IC"
    # termination = 0
    # utime = 12
    # rand = None
    network, seed, model, termination, utime, rand = options.ise_parse_command_line()
    # start = time.time()
    print solver(network, seed, model, termination, utime, rand)
    # run_time = (time.time() - start)
    # print "TIME: {}s".format(run_time)
