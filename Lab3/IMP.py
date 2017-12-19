# encoding: utf-8
import Queue
import time
import graph
import random
import ISE
import numpy as np
import options

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

    def set_influence(self, inf):
        self.influence = inf

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
            assert degree[it] > 0
            # print 'in degree:', it, degree[it]
            degree_discount.put(Node_degree(it, degree[it]))
        else:
            degree[it] = 0

    top_rand = k ** 2
    if top_rand > len(degree):
        top_rand = len(degree)

    for i in range(k):
        temp = []
        for j in range(top_rand):
            if not degree_discount.empty():
                temp.append(degree_discount.get_nowait())

        # index = get_exp_rand(0, len(temp), 0.5)  # 按照指数函数分布取值
        index = get_rand_node(temp)  # 以weight作为权重取值

        # 没用过的数放回
        for j in range(len(temp)):
            if j != index:
                degree_discount.put(temp[j])

        it = temp[index].node

        # it = degree_discount.get().node
        # 选择或许存在的强力影响的父节点
        big_parent = find_big_parent(network, it)
        if len(big_parent) != 0:
            degree_discount.put(temp[index])
            counter = 0
            loop = set()
            while len(big_parent) != 0:
                counter += 1
                # print "round:",counter
                index = random.randint(0, len(big_parent) - 1)
                before = (big_parent, index)
                # 判断是否有环
                if big_parent[index] not in loop:
                    loop.add(big_parent[index])
                else:
                    big_parent = list(loop)
                    index = random.randint(0, len(big_parent) - 1)
                    before = (big_parent, index)
                    break
                big_parent = find_big_parent(network, big_parent[index])

            big_parent, index = before
            it = big_parent[index]
            del_node(degree_discount, it)
            seed.append(it)
        else:
            seed.append(it)

        for nei in network.get_neighbor(it):
            if nei not in seed:
                # adjacent[nei] += 1
                adjacent[nei] += network.get_weight(it, nei)
                priority = degree[nei] - 2 * adjacent[nei] - (degree[nei] - adjacent[nei]) * adjacent[nei] * p
                if priority >= 0:
                    degree_discount.put(Node_degree(nei, priority))
    seed.sort()
    return seed


def del_node(dd, n):
    buf = []
    while not dd.empty():
        temp = dd.get()
        if temp.node == n:
            break
        else:
            buf.append(temp)

    for it in buf:
        dd.put(it)


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
    """
    generate random numbers by weight
    :param optional: degree discount list
    :return: node number
    """
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
    rmdup = dict()
    for it in seeds:
        key = tuple(it.seed)
        if key in rmdup:
            if rmdup[key] > it.influence:
                rmdup[key] = it.influence
        else:
            rmdup[key] = it.influence
    # print len(seeds), len(rmdup)

    out = []
    for it in rmdup:
        s = Seed(list(it))
        s.set_influence(rmdup[it])
        out.append(s)
    return out


def print_seed(seed):
    for i in seed:
        print i


def solver(network, size, model, termination, utime, rand):
    random.seed(rand)
    data = graph.read_network(network)
    d1 = graph.list2dict(data[2])
    d2 = graph.inv_list2dict(data[2])
    grap = graph.Graph(d1, d2)

    seed_size = size
    seeds = []
    fine_seed = []

    start = time.time()
    if termination == 0:
        for i in range(1000):
            s = Seed(degreeDiscountIC(grap, seed_size, 0.01))
            s.evaluate(model, grap)
            seeds.append(s)
            # print i, s

        seeds = remove_duplicate(seeds)
        seeds.sort(reverse=True)
        fine_seed = seeds[0:10]
        run_time = (time.time() - start)
        # print "TIME1: {}s".format(run_time)
    elif termination == 1:
        run_time = (time.time() - start)
        # print "TIME1: {}s".format(run_time)
        while run_time + 1 < utime:
            s = Seed(degreeDiscountIC(grap, seed_size, 0.01))
            s.evaluate(model, grap)
            seeds.append(s)
            run_time = (time.time() - start)

        seeds = remove_duplicate(seeds)
        seeds.sort(reverse=True)
        fine_seed = seeds[0:10]
        run_time = (time.time() - start)
        # print "TIME2: {}s".format(run_time)

    for i in range(0, len(fine_seed)):
        fine_seed[i].evaluate(model, grap, ISE.MEDIUM)
    seeds.sort(reverse=True)

    print_seed(seeds[0].seed)  # 打印结果
    run_time = (time.time() - start)
    # print "TIME4: {}s".format(run_time)
    return seeds[0]  # 返回Seed 对象


if __name__ == "__main__":
    # network = "network.txt"
    # network = "NetHEPT.txt"
    # size = 4
    # model = "IC"
    # termination = 0
    # utime = 5
    # rand = None
    network, size, model, termination, utime, rand = options.imp_parse_command_line()
    # print solver(network, size, model, termination, utime, rand)
    solver(network, size, model, termination, utime, rand)
