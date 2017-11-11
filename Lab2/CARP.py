# encoding: utf-8
import re
import dijkstra as dij
import copy
import sys
import random


def readData(filename):
    # 0-7行，数据定义
    # 8行开始，数据本体
    f = open(filename, 'r')
    Pattern = ["NAME : (.*)",  # Line 0
               "VERTICES : ([0-9]*)",  # Line 1
               "DEPOT : ([0-9]*)",  # Line 2
               "REQUIRED EDGES : ([0-9]*)",  # Line 3
               "NON-REQUIRED EDGES : ([0-9]*)",  # Line 4
               "VEHICLES : ([0-9]*)",  # Line 5
               "CAPACITY : ([0-9]*)",  # Line 6
               "TOTAL COST OF REQUIRED EDGES : ([0-9]*)"]  # Line 7
    data = f.readlines()
    count = 0
    fData = []
    for it in data:
        if count == 0:
            fData.append(re.findall(Pattern[count], it)[0])
            count += 1
        elif count <= 7:
            fData.append(int(re.findall(Pattern[count], it)[0]))
            count += 1
        elif count == 8:
            count += 1
        elif 'END' in it:
            break
        else:
            temp = it.split()
            for i in range(0, len(temp)):
                temp[i] = int(temp[i])
            fData.append(temp)
    return fData


def matrixTran(data):
    # 转换为邻接矩阵，每条边正反都存
    vmap = {}

    for it in range(8, len(data)):
        # print data[it]
        if data[it][0] in vmap:
            temp = vmap[data[it][0]]
            temp[data[it][1]] = (data[it][2], data[it][3])
        else:
            temp = {}
            temp[data[it][1]] = (data[it][2], data[it][3])
            vmap[data[it][0]] = temp

        if data[it][1] in vmap:
            temp = vmap[data[it][1]]
            temp[data[it][0]] = (data[it][2], data[it][3])
        else:
            temp = {}
            temp[data[it][0]] = (data[it][2], data[it][3])
            vmap[data[it][1]] = temp
    return vmap


def free_Set(data):
    # 转换为邻接矩阵，每条边只存一次
    free = []
    for it in range(8, len(data)):
        # print data[it]
        if data[it][3] != 0:
            free.append(data[it])
    return free


def better(u, uPrev, remain, map_dij, capacity, rule, isinv):
    '''
    :param u: 当前边
    :param uPrev: 历史最优边
    :param remain: 车辆剩余容量
    :param map_dij: Dijkstra对象
    :param capacity: 车辆容量
    :param rule: 使用规则
    :param isinv: 是否将当前边反向比较
    :return: bool型，是否更好
    '''
    function = {
        1: rule1,
        2: rule2,
        3: rule3,
        4: rule4,
        5: rule5
    }
    func = function[rule]
    return func(u, uPrev, remain, map_dij, capacity, isinv)


def rule1(u, uPrev, remain, map_dij, capacity, isinv):
    if uPrev is None:
        return True

    try:
        rate1 = u[2] / (remain - u[3])
    except:
        rate1 = sys.maxint
    try:
        rate2 = uPrev[2] / (remain - uPrev[3])
    except:
        rate2 = sys.maxint

    if rate1 > rate2:
        return True
    else:
        return False


def rule2(u, uPrev, remain, map_dij, capacity, isinv):
    if uPrev is None:
        return True

    try:
        rate1 = u[2] / (remain - u[3])
    except:
        rate1 = sys.maxint
    try:
        rate2 = uPrev[2] / (remain - uPrev[3])
    except:
        rate2 = sys.maxint

    if rate1 < rate2:
        return True
    else:
        return False


def rule3(u, uPrev, remain, map_dij, capacity, isinv):
    if uPrev is None:
        return True
    if isinv:
        if map_dij.get_dist(u[0], 1) > map_dij.get_dist(uPrev[1], 1):
            return True
        else:
            return False
    else:
        if map_dij.get_dist(u[1], 1) > map_dij.get_dist(uPrev[1], 1):
            return True
        else:
            return False


def rule4(u, uPrev, remain, map_dij, capacity, isinv):
    if uPrev is None:
        return True
    if isinv:
        if map_dij.get_dist(u[0], 1) < map_dij.get_dist(uPrev[1], 1):
            return True
        else:
            return False
    else:
        if map_dij.get_dist(u[1], 1) < map_dij.get_dist(uPrev[1], 1):
            return True
        else:
            return False


def rule5(u, uPrev, remain, map_dij, capacity, isinv):
    if uPrev is None:
        return True
    if remain > capacity / 2:
        return rule3(u, uPrev, remain, map_dij, capacity, isinv)
    else:
        return rule4(u, uPrev, remain, map_dij, capacity, isinv)


def removeFree(free, edge):
    '''
    :param free: 路径列表
    :param edge: 需要移除的边
    :return:
    '''
    index = -1
    [start, end, cost, demand] = edge
    for i in range(0, len(free)):
        [istart, iend, icost, idemand] = free[i]
        if (istart == start and iend == end) or (istart == end and iend == start):
            index = i
            break
    del free[index]


def path_scanning(graph, map_dij, capacity, ruleNum):
    '''
    :param graph: 邻接表，每条边只存一次
    :param map_dij: Dijkstra对象
    :param capacity: 容量
    :param ruleNum: 使用的规则
    :return: 路径列表
    '''
    k = 0
    free = copy.deepcopy(graph)
    rt = []
    l = []  # load list
    c = []  # cost list
    while True:
        k = k + 1
        r = []  # route list
        load = 0
        cost = 0
        remain = capacity
        i = 1
        while True:
            dist = sys.maxint
            edge = None
            for it in free:
                # it格式 [a,b,c,d] a起点 0，b终点 1，c COST 2，d DEMAND 3
                [istart, iend, icost, idemand] = it
                if load + idemand <= capacity:
                    # 正面
                    if map_dij.get_dist(i, istart) < dist:
                        dist = map_dij.get_dist(i, istart)
                        edge = it
                    elif dist == map_dij.get_dist(i, istart) and better(it, edge, remain, map_dij, capacity, ruleNum,
                                                                        False):
                        edge = it
                    # 反面
                    if map_dij.get_dist(i, iend) < dist:
                        dist = map_dij.get_dist(i, iend)
                        edge = [iend, istart, icost, idemand]
                    elif dist == map_dij.get_dist(i, iend) and better(it, edge, remain, map_dij, capacity, ruleNum,
                                                                      True):
                        edge = [iend, istart, icost, idemand]
                else:
                    continue
            # end for
            if edge is not None:
                [istart, iend, icost, idemand] = edge
                r.append(edge)
                # print r
                removeFree(free, edge)
                load = load + idemand
                remain = capacity - load
                cost = cost + dist + icost
                i = iend

            if len(free) == 0 or dist == sys.maxint:
                break
                # end in loop
        cost = cost + map_dij.get_dist(i, 1)
        l.append(load)
        c.append(cost)
        rt.append(r)
        if len(free) == 0:
            break
            # end out loop
    return rt, l, c


def calc_cost(path, map_dij):
    total_cost = 0
    total_demand = 0
    for i in range(0, len(path)):
        cost = 0
        demand = 0
        prev = 1
        for j in range(0, len(path[i])):
            [istart, iend, icost, idemand] = path[i][j]
            cost = cost + icost + map_dij.get_dist(prev, istart)
            prev = iend
            demand += idemand
        cost = cost + map_dij.get_dist(prev, 1)
        print "{}: COST: {}, DEMAND: {}".format(i + 1, cost, demand)
        total_cost += cost
        total_demand += demand
    print "Total COST: {}, Total DEMAND: {}".format(total_cost, total_demand)


def printHead(sample):
    print "NAME : {}".format(sample[0])  # Line 0
    print "VERTICES : {}".format(sample[1])  # Line 1
    print "DEPOT : {}".format(sample[2])  # Line 2
    print "REQUIRED EDGES : {}".format(sample[3])  # Line 3
    print "NON-REQUIRED EDGES : {}".format(sample[4])  # Line 4
    print "VEHICLES : {}".format(sample[5])  # Line 5
    print "CAPACITY : {}".format(sample[6])  # Line 6
    print "TOTAL COST OF REQUIRED EDGES : {}".format(sample[7])  # Line 7


def printRoute(route, vdij):
    total_cost = 0
    total_demand = 0
    for i in range(0, len(route)):
        cost = 0
        demand = 0
        print str(i + 1) + ": ",
        for j in range(0, len(route[i])):
            cost += route[i][j][2]
            demand += route[i][j][3]
            print "({}, {})".format(route[i][j][0], route[i][j][1]),
            # print route[i][j]

            if j < len(route[i]) - 1:
                print ",",
            else:
                print ""
                # print "\nCOST: {}, DEMAND: {}".format(cost, demand)
                total_cost += cost
                total_demand += demand
    # print "Total COST: {}, Total DEMAND: {}".format(total_cost, total_demand)
    calc_cost(route, vdij)


def printGraph(graph):
    for it in graph:
        print it, graph.get(it)


class routing(object):
    def __init__(self, path):
        self.path = path
        self.total_cost = sys.maxint
        self.total_demand = sys.maxint
        self.cost = []
        self.demand = []

    def calc_cost(self, map_dij):
        self.cost = []
        self.demand = []
        self.total_cost = 0
        self.total_demand = 0
        for i in range(0, len(self.path)):
            Tcost = 0
            Tdemand = 0
            prev = 1
            for j in range(0, len(self.path[i])):
                [istart, iend, icost, idemand] = self.path[i][j]
                Tcost = Tcost + icost + map_dij.get_dist(prev, istart)
                prev = iend
                # demand += idemand
            Tcost = Tcost + map_dij.get_dist(prev, 1)
            self.cost.append(Tcost)
            self.demand.append(Tdemand)
            self.total_cost += Tcost
            self.total_demand += Tdemand

    def mutation_single(self):
        muta = []
        route_index = random.randint(0, len(self.path) - 1)
        for i in range(0, len(self.path)):
            new_route = copy.deepcopy(self.path[i])
            if i == route_index:
                # print "route:{}".format(route_index)
                edge_index = random.randint(0, len(new_route) - 1)
                # print "len:{}, index:{}".format(len(new_route), edge_index)
                edge = new_route[edge_index]
                new_route.remove(edge)
                inset = random.randint(0, len(new_route))
                new_route.insert(inset, edge)
            muta.append(new_route)
        return muta

    def mutation_double(self):
        muta1 = []
        muta2 = []
        route_index = random.randint(0, len(self.path) - 1)
        for i in range(0, len(self.path)):
            new_route1 = copy.deepcopy(self.path[i])
            new_route2 = copy.deepcopy(self.path[i])
            if i == route_index:
                # print "route:{}".format(route_index)
                edge_index = random.randint(0, len(new_route1) - 1)
                # print "len:{}, index:{}".format(len(new_route), edge_index)

                edge = new_route1[edge_index]
                [istart, iend, icost, idemand] = edge
                inv_edge = [iend, istart, icost, idemand]

                new_route1.remove(edge)
                new_route2.remove(edge)
                inset = random.randint(0, len(new_route1))
                new_route1.insert(inset, edge)
                new_route2.insert(inset, inv_edge)
            muta1.append(new_route1)
            muta2.append(new_route2)
        return muta1, muta2


if __name__ == '__main__':
    # sample = readData("CARP_samples\\egl-e1-A.dat")
    # sample = readData("CARP_samples\\egl-s1-A.dat")
    sample = readData("CARP_samples\\gdb1.dat")
    # sample = readData("CARP_samples\\gdb10.dat")
    # sample = readData("CARP_samples\\val1A.dat")
    # sample = readData("CARP_samples\\val4A.dat")
    # sample = readData("CARP_samples\\val7A.dat")

    print sample
    printHead(sample)

    free = free_Set(sample)
    print free

    vertex = matrixTran(sample)
    vdij = dij.Dijkstra(vertex)
    # # vdij.go_all()
    # # print test1.d
    # for i in range(1, 6):
    #     print "\nRule{}".format(i)
    #     (rt, load, cost) = path_scanning(free, vdij, sample[6], i)
    #     printRoute(rt, vdij)
    #     # print rt
    #     # print "Route COST: {}".format(sum(cost))

    (rt, load, cost) = path_scanning(free, vdij, sample[6], 1)
    a = routing(rt)
    a.calc_cost(vdij)
    print a.total_cost

    b = routing(a.mutation_single())
    b.calc_cost(vdij)
    print b.total_cost
