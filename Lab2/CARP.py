# encoding: utf-8
import re
import dijkstra as dij
import copy
import sys
import random
import time


# TODO 下降速率画图
# TODO 中间某步重新生成路径（path scanning）
# TODO 统计那种变异方法最有效
# TODO 随机使用rule


# TODO 减少edge的后两个参数，改成查表
# TODO Augment-merge，split 算法
# TODO Order Crossover genetic algorithm 改进变异算法
# TODO 改变边的存储方式，其实每条边不需要深度复制，只是每条边的顺序 和 方向需要深度复制
# TODO 改成边的字典引用貌似可行

# TODO 并行化
def read_data(filename):
    """
    读取文件
    0-7行，数据定义
    8行开始，数据本体
    :param filename: 文件名
    :return: 数据列表
    """
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


def print_head(sample):
    print "NAME : {}".format(sample[0])  # Line 0
    print "VERTICES : {}".format(sample[1])  # Line 1
    print "DEPOT : {}".format(sample[2])  # Line 2
    print "REQUIRED EDGES : {}".format(sample[3])  # Line 3
    print "NON-REQUIRED EDGES : {}".format(sample[4])  # Line 4
    print "VEHICLES : {}".format(sample[5])  # Line 5
    print "CAPACITY : {}".format(sample[6])  # Line 6
    print "TOTAL COST OF REQUIRED EDGES : {}".format(sample[7])  # Line 7


def matrix_tran(data):
    """
    将源数据转换为邻接矩阵，每条边正反都存
    :param data: 源数据
    :return: 邻接矩阵
    """
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


def free_edge_set(data):
    """
    取出所有有需求的边，每条边只存一次
    :param data: 源数据
    :return: 邻接矩阵
    """
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


def path_scanning(graph, map_dij, capacity, rule_num):
    """
    :param graph: 邻接表，每条边只存一次
    :param map_dij: Dijkstra对象
    :param capacity: 容量
    :param rule_num: 使用的规则，如果在[1, 5] 范围内就一直使用此规则，不然随机使用规则。
    :return: 路径列表
    """
    out_of_index = rule_num < 0 or rule_num > 5
    # k = 0
    free = copy.deepcopy(graph)
    rt = []
    l = []  # load list
    c = []  # cost list
    while True:
        # k = k + 1
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
                if out_of_index:
                    rule_num = random.randint(1, 5)
                if load + idemand <= capacity:
                    # 正面
                    if map_dij.get_dist(i, istart) < dist:
                        dist = map_dij.get_dist(i, istart)
                        edge = it
                    elif dist == map_dij.get_dist(i, istart) and better(it, edge, remain, map_dij, capacity, rule_num,
                                                                        False):
                        edge = it
                    # 反面
                    if map_dij.get_dist(i, iend) < dist:
                        dist = map_dij.get_dist(i, iend)
                        edge = [iend, istart, icost, idemand]
                    elif dist == map_dij.get_dist(i, iend) and better(it, edge, remain, map_dij, capacity, rule_num,
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

    def print_route(self, vdij):
        self.calc_cost(vdij)
        for i in range(0, len(self.path)):
            line = str(i + 1) + ": "
            for j in range(0, len(self.path[i])):
                line += "({}, {})".format(self.path[i][j][0], self.path[i][j][1])

                if j < len(self.path[i]) - 1:
                    line += ", "
            print line
        print "Total COST: {}, Total DEMAND: {}".format(self.total_cost, self.total_demand)

    def check(self):
        # if len(self.cost) > self.vehicles:
        #     self.obey_rule = False
        #     print "more cars"
        #     return self.obey_rule

        for d in self.demand:
            if d > self.capacity:
                self.obey_rule = False
                # print "more demand"
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
                [istart, iend] = self.path[i][j]
                Tcost = Tcost + map_dij.get_cost(istart, iend) + map_dij.get_dist(prev, istart)
                Tdemand = Tdemand + map_dij.get_demand(istart, iend)
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
        it1 = self.path[x1][y1]

        x2 = random.randint(0, len(self.path) - 1)
        y2 = random.randint(0, len(self.path[x2]) - 1)
        it2 = self.path[x2][y2]

        new_route1 = copy.deepcopy(self.path)
        new_route2 = copy.deepcopy(self.path)
        new_route3 = copy.deepcopy(self.path)
        new_route4 = copy.deepcopy(self.path)

        for i in range(0, len(new_route1)):
            if x1 == i:
                new_route1[x1][y1] = it2
                new_route2[x1][y1] = invedge(it2)
                new_route3[x1][y1] = invedge(it2)
                new_route4[x1][y1] = it2
            if x2 == i:
                new_route1[x2][y2] = it1
                new_route2[x2][y2] = invedge(it1)
                new_route3[x2][y2] = it1
                new_route4[x2][y2] = invedge(it1)
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
        while route_index1 == route_index2:
            route_index1 = random.randint(0, len(self.path) - 1)
            route_index2 = random.randint(0, len(self.path) - 1)

        sub1 = random.randint(0, len(self.path[route_index1]) - 1)
        sub2 = random.randint(0, len(self.path[route_index2]) - 1)

        for i in range(0, len(self.path)):
            if i != route_index1 and i != route_index2:
                new_route1.append(copy.deepcopy(self.path[i]))
                new_route2.append(copy.deepcopy(self.path[i]))

        tmp1 = copy.deepcopy(self.path[route_index1][0:sub1])
        tmp2 = copy.deepcopy(self.path[route_index2][sub2:])
        new_route1.append(tmp1 + tmp2)

        tmp1 = copy.deepcopy(self.path[route_index2][0:sub2])
        tmp2 = copy.deepcopy(self.path[route_index1][sub1:])
        new_route1.append(tmp1 + tmp2)

        tmp1 = copy.deepcopy(self.path[route_index1][0:sub1])
        tmp2 = reverse_edges(self.path[route_index2][0:sub2])
        new_route2.append(tmp1 + tmp2)

        tmp1 = reverse_edges(self.path[route_index1][sub1:])
        tmp2 = copy.deepcopy(self.path[route_index2][sub2:])
        new_route2.append(tmp1 + tmp2)

        return new_route1, new_route2

    def fix(self, map_dij, capacity, rule_num):
        fixed = []
        free = []
        l = []  # load list
        test = 0
        # assert len(self.path) >= 7
        for i in range(0, len(self.path)):
            Tdemand = 0
            tmp_fix = []
            tmp_load = 0
            for j in range(0, len(self.path[i])):
                [istart, iend] = self.path[i][j]
                temp = Tdemand + map_dij.get_demand(istart, iend)
                if temp <= capacity:
                    Tdemand = temp
                    tmp_load = temp
                    tmp_fix.append([istart, iend])
                else:
                    Tdemand = temp
                    icost = map_dij.get_cost(istart, iend)
                    idemand = map_dij.get_demand(istart, iend)
                    free.append([istart, iend, icost, idemand])
            l.append(tmp_load)
            test += Tdemand
            fixed.append(tmp_fix)

        while [] in fixed:
            fixed.remove([])

        k = -1
        out_of_index = rule_num < 0 or rule_num > 5
        while True:
            k = k + 1
            if k < len(fixed):
                r = fixed[k]
                i = r[-1][1]
                load = l[k]
            else:
                r = []
                i = 1
                load = 0
            remain = capacity - load

            while True:
                dist = sys.maxint
                edge = None
                for it in free:
                    # it格式 [a,b,c,d] a起点 0，b终点 1，c COST 2，d DEMAND 3
                    [istart, iend, icost, idemand] = it
                    if out_of_index:
                        rule_num = random.randint(1, 5)
                    if load + idemand <= capacity:
                        # 正面
                        if map_dij.get_dist(i, istart) < dist:
                            dist = map_dij.get_dist(i, istart)
                            edge = it
                        elif dist == map_dij.get_dist(i, istart) and better(it, edge, remain, map_dij, capacity,
                                                                            rule_num,
                                                                            False):
                            edge = it
                        # 反面
                        if map_dij.get_dist(i, iend) < dist:
                            dist = map_dij.get_dist(i, iend)
                            edge = [iend, istart, icost, idemand]
                        elif dist == map_dij.get_dist(i, iend) and better(it, edge, remain, map_dij, capacity, rule_num,
                                                                          True):
                            edge = [iend, istart, icost, idemand]
                    else:
                        continue
                # end for
                if edge is not None:
                    [istart, iend, icost, idemand] = edge
                    r.append([istart, iend])
                    remove_free(free, edge)
                    load = load + idemand
                    remain = capacity - load
                    i = iend

                if len(free) == 0 or dist == sys.maxint:
                    break
                    # end in loop

            if k < len(l):
                l[k] = load
            else:
                l.append(load)
                fixed.append(r)
            if len(free) == 0:
                break
                # end out loop
        return fixed


def invedge(edge):
    [istart, iend] = edge
    return [iend, istart]


def reverse_edges(edges):
    tmp = copy.deepcopy(edges)
    tmp = tmp[::-1]
    for i in range(0, len(tmp)):
        tmp[i] = invedge(tmp[i])
    return tmp


def simplify_edge(route):
    rt = []
    for i in range(0, len(route)):
        line = []
        for j in range(0, len(route[i])):
            line.append([route[i][j][0], route[i][j][1]])
        rt.append(line)
    return rt


class Population:
    # TODO 减少deepcopy引用
    def __init__(self, select_size, generate_size, dist_map):
        """
        初始化
        :param select_size: 筛选总群大小
        :param generate_size: 变异大小
        :param dist_map: dijkstra对象
        """
        self.select_size = select_size
        self.generate_size = generate_size
        self.routing_list = []
        self.dist_map = dist_map

    def initial(self, initial_size, edge_set, vertex_dij, vehicles, capacity):
        print "\nInitial Route:"
        for i in range(1, initial_size + 1):
            print "Rule{}".format(i)
            (rt, load, cost) = path_scanning(edge_set, vertex_dij, capacity, i)
            s_rt = simplify_edge(rt)

            temp = Routing(s_rt, vehicles, capacity)
            temp.calc_cost(vertex_dij)
            temp.print_route(vertex_dij)
            self.add_route(temp)
            print ""

    def add_route(self, route):
        if route.check():
            self.routing_list.append(route)

    def generate(self, rule_num, vehicles, capacity):
        """
        产生新总群
        :param rule_num: 变异规则
        :param vehicles: 车辆数
        :param capacity: 车辆容量
        :return: None，增加备选列表
        """
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
                else:
                    rule = random.randint(1, 5)
                    rt = temp.fix(self.dist_map, capacity, rule)
                    fixed = Routing(rt, vehicles, capacity)
                    # print rt
                    fixed.calc_cost(self.dist_map)
                    if fixed.check():  # 检测是否符合规则
                        link.append(fixed)
                        counter = counter - 1
                        # 这里修不好就不要了
        self.routing_list.extend(link)

    def select(self):
        self.routing_list.sort()
        self.routing_list = self.routing_list[0:self.select_size]

    def top_best(self, num):
        self.routing_list.sort()
        if num < len(self.routing_list):
            count = num
        else:
            count = len(self.routing_list)
        for i in range(0, count):
            print "Top:{}\n".format(i + 1) + str(self.routing_list[i])

    def print_result(self):
        self.select()
        best = self.routing_list[0]
        path = best.path
        str_path = "s "
        for i in range(0, len(path)):
            str_path += "0,"
            for j in range(0, len(path[i])):
                str_path += "({},{}),".format(path[i][j][0], path[i][j][1])
            if i == len(path) - 1:
                str_path += "0"
            else:
                str_path += "0,"
        print str_path
        print "q {}".format(best.total_cost)


def search_CARP(file_name, limited_time, ram_seed):
    """
    :param file_name: 文件名
    :param limited_time: 限制时间
    :param ram_seed: 随机种子
    :return: None，标准打印
    """
    start = time.time()
    sample = read_data(file_name)
    vehicles = sample[5]
    capacity = sample[6]
    random.seed(ram_seed)

    print sample
    print_head(sample)

    free = free_edge_set(sample)
    # print free

    vertex = matrix_tran(sample)
    vertex_dij = dij.Dijkstra(vertex)
    # vertex_dij.print_graph()

    group = Population(200, 600, vertex_dij)
    group.initial(1000, free, vertex_dij, vehicles, capacity)
    group.select()
    group.top_best(3)
    run_time = (time.time() - start)
    count = 1

    while run_time <= limited_time:
        print "\nLOOP: {}".format(count)
        rule_num = random.randint(1, 5)
        group.generate(rule_num, vehicles, capacity)
        group.select()
        group.top_best(5)
        run_time = (time.time() - start)
        print "LOOP: {} TIME: {}s".format(count, run_time)
        count += 1

    run_time = (time.time() - start)
    print "\nTIME: {}s".format(run_time)
    group.print_result()


if __name__ == '__main__':
    search_CARP("CARP_samples\\egl-s1-A.dat", 120, None)

    # sem = [[[116,117],[117,2],[117,119],[124,126],[126,130],[118,114],[114,113],[113,112],[116,1]],[[112,107],[108,109],[108,107],[107,110],[110,111],[110,112]],[[107,106],[106,105],[105,104],[104,102],[66,62],[62,63],[63,64],[64,65],[56,55],[55,54],[55,140],[140,49],[49,48],[67,68]],[[95,96],[96,97],[97,98],[66,67],[67,69],[69,71],[71,72],[72,73],[73,44],[44,45],[45,34],[34,139]],[[43,44],[139,33],[33,11],[11,8],[6,5],[6,8],[8,9],[13,12]],[[87,86],[86,85],[85,84],[84,82],[82,80],[80,79],[79,78],[78,77],[77,46],[46,43],[43,37],[37,36],[36,38],[38,39],[39,40]],[[11,27],[27,28],[28,29],[28,30],[30,32],[27,25],[25,24],[24,20],[20,22],[13,14],[12,11]]]
    # sem =[[[1,116],[116,117],[117,119],[117,2],[118,114],[114,113],[113,112],[112,110],[110,111],[110,107],[107,108],[105,104]],[[87,86],[86,85],[85,84],[84,82],[82,80],[80,79],[79,78],[78,77],[77,46],[46,43],[43,37],[37,36],[36,38],[38,39],[39,40]],[[108,109],[66,62],[62,63],[63,64],[64,65],[56,55],[55,54],[55,140],[49,48]],[[124,126],[126,130],[43,44],[34,139],[139,33],[33,11],[11,12],[12,13],[20,22]],[[95,96],[96,97],[97,98],[140,49],[11,8],[6,5],[8,9],[13,14],[8,6],[24,25],[27,28]],[[11,27],[27,25],[24,20],[28,29],[28,30],[30,32]],[[112,107],[107,106],[106,105],[104,102],[66,67],[67,68],[67,69],[69,71],[45,34]],[[112,107],[107,106],[106,105],[104,102],[66,67],[67,68],[67,69],[69,71],[71,72],[72,73],[73,44],[44,45],[71,72],[72,73],[73,44],[44,45],[45,34]]]
    # sem =[[[1,116],[116,117],[117,119],[117,2],[118,114],[114,113],[113,112],[112,110],[110,111],[110,107],[107,108],[105,104]],[[87,86],[86,85],[85,84],[84,82],[82,80],[80,79],[79,78],[78,77],[77,46],[46,43],[43,37],[37,36],[36,38],[38,39],[39,40]],[[108,109],[66,62],[62,63],[63,64],[64,65],[56,55],[55,54],[55,140],[49,48]],[[124,126],[126,130],[43,44],[34,139],[139,33],[33,11],[11,12],[12,13],[20,22]],[[95,96],[96,97],[97,98],[140,49],[11,8],[6,5],[8,9],[13,14],[8,6],[24,25],[27,28]],[[11,27],[27,25],[24,20],[28,29],[28,30],[30,32]],[[112,107],[107,106],[106,105],[104,102],[66,67],[67,68],[67,69],[69,71],[45,34]],[[71,72],[72,73],[73,44],[44,45],[71,72],[72,73],[73,44],[44,45],[45,34]]]
    # te = Routing(sem, vehicles,capacity)
    # te.print_route(vertex_dij)
