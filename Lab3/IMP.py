# encoding: utf-8
import Queue
import time
import graph
import random
import ISE
import copy
import numpy as np

'''
# ISE 评估一个seed的影响
# return seed的影响总node数
# IMP 产生一个较好的seed
# IC [1]模型采用degree discount heuristic算法实现
# LT [2]模型采用
References:
[1] -- Wei Chen et al. Efficient influence maximization in Social Networks (algorithm 4)
[2] Chen et al. "Scalable Influence Maximization in Social Networks under Lienar Threshold Model"
'''


class Seed(object):
    def __init__(self, seed):
        self.seed = seed
        self.influence = 0

    def evaluate(self, model, network, speed=ISE.FAST):
        self.influence = ISE.sample(model, self.seed, network, speed)

    def __cmp__(self, other):
        if self.influence < other.influence:
            return -1
        elif self.influence > other.influence:
            return 1
        else:
            return 0

    def __str__(self):
        return str(self.seed) + "@" + str(self.influence)

    def __repr__(self):
        return str(self)


class Node_degree(object):
    def __init__(self, node, weight):
        self.node = node
        self.weight = weight

    def __cmp__(self, other):
        # 原来是从小到大排序
        # -1: if x < y
        # 0: if x == y
        # 1: if x > y
        # 重定义大小，这样就是大的权重在上
        if self.weight > other.weight:
            return -1
        elif self.weight < other.weight:
            return 1
        else:
            return 0

    def __str__(self):
        return str(self.node) + " & " + str(self.weight)

    def __repr__(self):
        return str(self)


def find_big_parent(network, node):
    out = []
    now = node
    parent = network.get_parent(now)
    for pa in parent:
        if network.get_weight(pa, now) == 1:
            out.append(pa)
    # print "parent len:", len(out)
    return out


def print_queue(pq):
    temp = []
    while not pq.empty():
        it = pq.get()
        print it
        temp.append(it)
    for it in temp:
        pq.put(it)


def degreeDiscountIC(network, k, p=.01):
    """
    :param network: graph
    :param k: number of nodes needed
    :param p: propagation probability
    :return: chosen k nodes
    """
    seed = []
    degree_discount = Queue.PriorityQueue()  # heap
    degree = {}
    adjacent = {}

    for it in network.nodes():
        adjacent[it] = 0
        if it in network.node_dict:
            degree[it] = sum(network.node_dict[it].values())
            # print 'in degree:', it, degree[it]
            degree_discount.put(Node_degree(it, degree[it]))
        else:
            degree[it] = 0

    top_rand = k ** 2
    if top_rand > len(degree):
        top_rand = degree

    # print_queue(degree_discount)

    for i in range(k):
        temp = []
        for j in range(top_rand):
            temp.append(degree_discount.get())

        # index = get_exp_rand(0, top_rand, 0.5) # 按照指数函数分布取值
        index = get_rand_node(temp)  # 以weight作为权重取值
        # index = random.randint(0,top_rand-1) # 平均随机数取值
        # print "index:", index

        # 没用过的数放回
        for j in range(top_rand):
            if j != index:
                degree_discount.put(temp[j])

        it = temp[index].node
        # it = degree_discount.get().node
        # print 'node:', it

        # 选择或许存在的强力影响的父节点
        big_parent = find_big_parent(network, it)
        if len(big_parent) != 0:
            degree_discount.put(temp[index])
            # index = random.randint(0, len(big_parent) - 1)
            counter = 0
            while len(big_parent) != 0:
                counter += 1
                # print "round:",counter
                index = random.randint(0, len(big_parent) - 1)
                before = (big_parent, index)
                big_parent = find_big_parent(network, big_parent[index])

            big_parent, index = before
            seed.append(big_parent[index])
            it = big_parent[index]
        else:
            seed.append(it)

        for nei in network.get_neighbor(it):
            if nei not in seed:
                # adjacent[nei] += 1
                adjacent[nei] += network.get_weight(it, nei)
                priority = degree[nei] - 2 * adjacent[nei] - (degree[nei] - adjacent[nei]) * adjacent[nei] * p
                degree_discount.put(Node_degree(nei, priority))
    seed.sort()
    return seed


def get_exp_rand(start, end, lambd):
    """
    generate a random int number in range [start, end) with Exponential distribution.
    :param start: range left end
    :param end: range right end (not include)
    :param lambd: lambda
    :return: a random int number
    """
    rand = int(random.expovariate(lambd))
    while rand < start or rand >= end:
        rand = int(random.expovariate(lambd))
    return rand


def get_rand_node(optional):
    nodes = []
    prob = []
    for i in range(0, len(optional)):
        nodes.append(optional[i].node)
        prob.append(optional[i].weight)

    sump = sum(prob)
    for i in range(0, len(prob)):
        prob[i] = prob[i] / sump

    n = np.random.choice(nodes, p=prob)

    return nodes.index(n)


def remove_duplicate(seeds):
    rmdup = set()
    for it in seeds:
        rmdup.add(tuple(it.seed))
    print len(seeds), len(rmdup)

    out = []
    for it in rmdup:
        out.append(Seed(list(it)))
    return out


if __name__ == "__main__":
    d = graph.read_network("network.txt")
    # d = graph.read_network("AI_IMP_testdata\\NetHEPT.txt")
    # d = graph.read_network("AI_IMP_testdata\\physical.txt")
    # d = graph.read_network("AI_IMP_testdata\\NetPHY.txt")
    # print d

    d1 = graph.list2dict(d[2])
    # graph.print_graph(d1)
    # print "-----------------------------"
    d2 = graph.inv_list2dict(d[2])
    # graph.print_graph(d2)
    test = graph.Graph(d1, d2)

    s = Seed(degreeDiscountIC(test, 4, 0.01))
    s.evaluate('IC', test)
    print s

    seeds = []
    for i in range(0, 500 + 1):
        s = Seed(degreeDiscountIC(test, 4, 0.01))
        seeds.append(s)

    # start = time.time()
    seeds = remove_duplicate(seeds)
    # run_time = (time.time() - start)
    # print "TIME: {}s".format(run_time)

    for s in seeds:
        s.evaluate('IC', test)

    seeds.sort(reverse=True)
    print seeds

    fine_seed = seeds[0:10]
    for i in range(0, len(fine_seed)):
        fine_seed[i].evaluate('LT', test, ISE.SLOW)

    fine_seed.sort(reverse=True)
    print len(fine_seed), fine_seed
