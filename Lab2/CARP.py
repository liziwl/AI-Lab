# encoding: utf-8
import re
import dijkstra as dij
import copy
import sys
import random
import time


def read_data(filename):
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


def matrix_tran(data):
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


def free_set(data):
    # 转换为邻接矩阵，每条边只存一次
    free = []
    for it in range(8, len(data)):
        # print data[it]
        if data[it][3] != 0:
            free.append(data[it])
    return free


def better(u, uPrev, remain, map_dij, capacity, rule, isinv):
    """
    :param u: 当前边
    :param uPrev: 历史最优边
    :param remain: 车辆剩余容量
    :param map_dij: Dijkstra对象
    :param capacity: 车辆容量
    :param rule: 使用规则
    :param isinv: 是否将当前边反向比较
    :return: bool型，是否更好
    """
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


def remove_free(free, edge):
    """
    :param free: 路径列表
    :param edge: 需要移除的边
    :return:
    """
    index = -1
    [start, end, cost, demand] = edge
    for i in range(0, len(free)):
        [istart, iend, icost, idemand] = free[i]
        if (istart == start and iend == end) or (istart == end and iend == start):
            index = i
            break
    del free[index]


def path_scanning(graph, map_dij, capacity, ruleNum):
    """
    :param graph: 邻接表，每条边只存一次
    :param map_dij: Dijkstra对象
    :param capacity: 容量
    :param ruleNum: 使用的规则
    :return: 路径列表
    """
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
                remove_free(free, edge)
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


def print_head(sample):
    print "NAME : {}".format(sample[0])  # Line 0
    print "VERTICES : {}".format(sample[1])  # Line 1
    print "DEPOT : {}".format(sample[2])  # Line 2
    print "REQUIRED EDGES : {}".format(sample[3])  # Line 3
    print "NON-REQUIRED EDGES : {}".format(sample[4])  # Line 4
    print "VEHICLES : {}".format(sample[5])  # Line 5
    print "CAPACITY : {}".format(sample[6])  # Line 6
    print "TOTAL COST OF REQUIRED EDGES : {}".format(sample[7])  # Line 7


def print_route(route, vdij):
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


def print_graph(graph):
    for it in graph:
        print it, graph.get(it)


class Routing(object):
    def __init__(self, path, vehicles, capacity):
        self.path = path
        self.total_cost = sys.maxint
        self.total_demand = sys.maxint
        self.cost = []
        self.demand = []
        self.obey_rule = False
        self.capacity = capacity
        self.vehicles = vehicles

    def __str__(self):
        return str(self.path) + "\n" + "Total COST: {}, Total DEMAND: {}".format(self.total_cost, self.total_demand)

    def __cmp__(self, other):
        if self.total_cost < other.total_cost:
            return -1
        elif self.total_cost > other.total_cost:
            return 1
        else:
            return 0

    def check(self):
        if len(cost) > self.vehicles:
            self.obey_rule = False
            return self.obey_rule

        for d in self.demand:
            if d > self.capacity:
                self.obey_rule = False
                return self.obey_rule

        self.obey_rule = True
        return self.obey_rule

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
                # print self.path[i][j]
                # print self.path
                [istart, iend, icost, idemand] = self.path[i][j]
                Tcost = Tcost + icost + map_dij.get_dist(prev, istart)
                Tdemand = Tdemand + idemand
                prev = iend
            Tcost = Tcost + map_dij.get_dist(prev, 1)
            self.cost.append(Tcost)
            self.demand.append(Tdemand)
            self.total_cost += Tcost
            self.total_demand += Tdemand

    def mutation(self, rule_num):
        """
        :param rule_num: 使用的变异规则
        :return: 变异后的路线元组
        """
        function = {
            1: self.mutation_single,
            2: self.mutation_double,
            3: self.mutation_swap,
            4: self.mutation_2opt,
            5: self.mutation_2opt_inter
        }
        func = function[rule_num]
        return func()

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
        return (muta,)

    def mutation_double(self):
        muta1 = []
        muta2 = []
        route_index = random.randint(0, len(self.path) - 1)
        for i in range(0, len(self.path)):
            copy_edge = copy.deepcopy(self.path[i])
            new_route1 = copy_edge
            new_route2 = copy_edge
            if i == route_index:
                edge_index = random.randint(0, len(copy_edge) - 1)

                edge = copy_edge[edge_index]
                inv_edge = invedge(edge)

                copy_edge.remove(edge)
                inset = random.randint(0, len(copy_edge))
                dup_edge = copy.deepcopy(copy_edge)
                new_route2 = dup_edge

                copy_edge.insert(inset, edge)
                dup_edge.insert(inset, inv_edge)

            muta1.append(new_route1)
            muta2.append(new_route2)
        return muta1, muta2

    def mutation_swap(self):
        x1 = random.randint(0, len(self.path) - 1)
        y1 = random.randint(0, len(self.path[x1]) - 1)
        it1 = self.path[x1][y1]  # 交换边1

        x2 = random.randint(0, len(self.path) - 1)
        y2 = random.randint(0, len(self.path[x2]) - 1)
        it2 = self.path[x2][y2]  # 交换边2

        origin_copy = copy.deepcopy(self.path)
        new_route1 = []
        new_route2 = []
        new_route3 = []
        new_route4 = []

        for i in range(0, len(self.path)):
            if i != x1 and i != x2:
                new_route1.append(origin_copy[i])
                new_route2.append(origin_copy[i])
                new_route3.append(origin_copy[i])
                new_route4.append(origin_copy[i])
            else:
                if x1 == i:
                    ori_tmp = origin_copy[i]
                    rout = copy.deepcopy(ori_tmp)
                    rout[y1] = it2
                    inv_rout = copy.deepcopy(ori_tmp)
                    inv_rout[y1] = invedge(it2)

                    new_route1.append(rout)
                    new_route2.append(inv_rout)
                    new_route3.append(inv_rout)
                    new_route4.append(rout)
                if x2 == i:
                    ori_tmp = origin_copy[i]
                    rout = copy.deepcopy(ori_tmp)
                    rout[y2] = it1
                    inv_rout = copy.deepcopy(ori_tmp)
                    inv_rout[y2] = invedge(it1)

                    new_route1.append(rout)
                    new_route2.append(inv_rout)
                    new_route3.append(rout)
                    new_route4.append(inv_rout)
        return new_route1, new_route2, new_route3, new_route4

    def mutation_2opt(self):
        new_route1 = copy.deepcopy(self.path)
        route_index = random.randint(0, len(self.path) - 1)
        sub1 = random.randint(0, len(self.path[route_index]) - 1)
        sub2 = random.randint(0, len(self.path[route_index]) - 1)
        if sub1 > sub2:
            sub1, sub2 = sub2, sub1

        temp = copy.deepcopy(new_route1[route_index])
        for i in range(sub1, sub2 + 1)[::-1]:
            new_route1[route_index][sub2 + sub1 - i] = invedge(temp[i])
        return (new_route1,)

    def mutation_2opt_inter(self):
        new_route1 = []
        new_route2 = []

        route_index1 = random.randint(0, len(self.path) - 1)
        route_index2 = random.randint(0, len(self.path) - 1)

        sub1 = random.randint(0, len(self.path[route_index1]) - 1)
        sub2 = random.randint(0, len(self.path[route_index2]) - 1)

        for i in range(0, len(self.path)):
            if i != route_index1 and i != route_index2:
                new_route1.append(copy.deepcopy(self.path[i]))
                new_route2.append(copy.deepcopy(self.path[i]))

        sub1_start = copy.deepcopy(self.path[route_index1][0:sub1])
        sub2_end = copy.deepcopy(self.path[route_index2][sub2:])
        new_route1.append(sub1_start + sub2_end)

        tmp = copy.deepcopy(self.path[route_index2][0:sub2])
        new_route1.append(tmp + copy.deepcopy(self.path[route_index1][sub1:]))

        new_route2.append(sub1_start + reverse_edges(self.path[route_index2][0:sub2]))

        tmp = reverse_edges(self.path[route_index1][sub1:])
        new_route2.append(tmp + sub2_end)
        return new_route1, new_route2


def invedge(edge):
    [istart, iend, icost, idemand] = edge
    return [iend, istart, icost, idemand]


def reverse_edges(edges):
    tmp = copy.deepcopy(edges)
    tmp = tmp[::-1]
    for i in range(0, len(tmp)):
        tmp[i] = invedge(tmp[i])
    return tmp


class Population:
    # TODO 减少deepcopy引用
    def __init__(self, select_size, generate_size, dist_map):
        self.select_size = select_size
        self.generate_size = generate_size
        self.routing_list = []
        self.dist_map = dist_map

    def add_route(self, route):
        if route.check():
            self.routing_list.append(route)

    def generate(self, rule_num, vehicles, capacity):
        link = []
        counter = self.generate_size
        while counter > 0:
            index = random.randint(0, len(self.routing_list) - 1)
            muta = self.routing_list[index].mutation(rule_num)
            for rout in muta:
                temp = Routing(rout, vehicles, capacity)
                temp.calc_cost(self.dist_map)
                if temp.check():  # 检测是否符合规则
                    link.append(temp)
                    counter = counter - 1
        self.routing_list.extend(link)

    def select(self):
        self.routing_list.sort()
        self.routing_list = self.routing_list[0:self.select_size]

    def top_best(self, num):
        self.routing_list.sort()
        if num < len(self.routing_list):
            count = num + 1
        else:
            count = len(self.routing_list)
        for i in range(0, count):
            print "Top:{}\n".format(i + 1) + str(self.routing_list[i])


if __name__ == '__main__':
    start = time.time()

    # sample = read_data("CARP_samples\\egl-e1-A.dat")
    # sample = read_data("CARP_samples\\egl-s1-A.dat")
    # sample = read_data("CARP_samples\\gdb1.dat")
    sample = read_data("CARP_samples\\gdb10.dat")
    # sample = read_data("CARP_samples\\val1A.dat")
    # sample = read_data("CARP_samples\\val4A.dat")
    # sample = read_data("CARP_samples\\val7A.dat")

    print sample
    print_head(sample)

    free = free_set(sample)
    print free

    vertex = matrix_tran(sample)
    vdij = dij.Dijkstra(vertex)
    # vdij.go_all()

    group = Population(100, 400, vdij)

    for i in range(1, 6):
        print "Rule{}".format(i)
        (rt, load, cost) = path_scanning(free, vdij, sample[6], i)
        print_route(rt, vdij)

        a = Routing(rt, sample[5], sample[6])
        a.calc_cost(vdij)
        group.add_route(a)
        print ""

    group.select()
    group.top_best(3)

    for i in range(0, 1000):
        print "\nLOOP: {}".format(i + 1)
        rule_num = random.randint(1, 5)
        # rule_num = 3
        group.generate(rule_num, sample[5], sample[6])
        group.select()
        group.top_best(5)
        run_time = (time.time() - start)
        print "LOOP: {} TIME: {}s".format(i + 1, run_time)

    run_time = (time.time() - start)
    print "\nTIME: {}s".format(run_time)
