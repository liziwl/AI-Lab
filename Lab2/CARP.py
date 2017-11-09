# encoding: utf-8
import re
import dijkstra as dij
import copy
import sys


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
    # 转换为邻接矩阵
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
    # 转换为邻接矩阵
    free = []
    for it in range(8, len(data)):
        # print data[it]
        if data[it][3] != 0:
            free.append(data[it])
    return free


# class route:
#     def __init__(self,graph):
#         self.route_list = []
#         self.graph = graph

def printGraph(graph):
    for it in graph:
        print it, graph.get(it)

        # def append(self, route_num, task):
        #     self.route_list[route_num].append(task)


def better(u, uPrev, remain, distance, capacity, rule, isinv):
    function = {
        1: rule1,
        2: rule2,
        3: rule3,
        4: rule4,
        5: rule5
    }
    func = function[rule]
    return func(u, uPrev, remain, distance, capacity, isinv)


def rule1(u, uPrev, remain, distance, capacity, isinv):
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


def rule2(u, uPrev, remain, distance, capacity, isinv):
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


def rule3(u, uPrev, remain, distance, capacity, isinv):
    if uPrev is None:
        return True
    if isinv:
        if distance[u[0]][1] > distance[uPrev[1]][1]:
            return True
        else:
            return False
    else:
        if distance[u[1]][1] > distance[uPrev[1]][1]:
            return True
        else:
            return False


def rule4(u, uPrev, remain, distance, capacity, isinv):
    if uPrev is None:
        return True
    if isinv:
        if distance[u[0]][1] < distance[uPrev[1]][1]:
            return True
        else:
            return False
    else:
        if distance[u[1]][1] < distance[uPrev[1]][1]:
            return True
        else:
            return False


def rule5(u, uPrev, remain, distance, capacity, isinv):
    if uPrev is None:
        return True
    if remain > capacity / 2:
        return rule3(u, uPrev, remain, distance, capacity, isinv)
    else:
        return rule4(u, uPrev, remain, distance, capacity, isinv)


def removeFree(free, edge):
    index = -1
    [start, end, cost, demand] = edge
    for i in range(0, len(free)):
        [istart, iend, icost, idemand] = free[i]
        if (istart == start and iend == end) or (istart == end and iend == start):
            index = i
            break
    del free[index]


def path_scanning(graph, distance, capacity, ruleNum):
    '''
    :param graph: 邻接表
    :param distance: Dijkstra对象中的每2个点之间的距离
    :param capacity: 容量
    :return:
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
                    if distance[i][istart] < dist:
                        dist = distance[i][istart]
                        edge = it
                    elif dist == distance[i][istart] and better(it, edge, remain, distance, capacity, ruleNum, False):
                        edge = it
                    # 反面
                    if distance[i][iend] < dist:
                        dist = distance[i][iend]
                        edge = [iend, istart, icost, idemand]
                    elif dist == distance[i][iend] and better(it, edge, remain, distance, capacity, ruleNum, True):
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
        cost = cost + distance[i][1]
        l.append(load)
        c.append(cost)
        rt.append(r)
        if len(free) == 0:
            break
            # end out loop
    return rt


def printHead(sample):
    print "NAME : {}".format(sample[0])  # Line 0
    print "VERTICES : {}".format(sample[1])  # Line 1
    print "DEPOT : {}".format(sample[2])  # Line 2
    print "REQUIRED EDGES : {}".format(sample[3])  # Line 3
    print "NON-REQUIRED EDGES : {}".format(sample[4])  # Line 4
    print "VEHICLES : {}".format(sample[5])  # Line 5
    print "CAPACITY : {}".format(sample[6])  # Line 6
    print "TOTAL COST OF REQUIRED EDGES : {}".format(sample[7])  # Line 7


def printRoute(route):
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
                print "\nCOST: {}, DEMAND: {}".format(cost, demand)


class task:
    def __init__(self, id, start, end, cost, demand):
        self.id = id
        self.start = start
        self.end = end
        self.cost = cost
        self.demand = demand


if __name__ == '__main__':
    sample = readData("CARP_samples\\egl-e1-A.dat")
    # sample = readData("CARP_samples\\egl-s1-A.dat")
    # sample = readData("CARP_samples\\gdb1.dat")
    # sample = readData("CARP_samples\\gdb10.dat")
    # sample = readData("CARP_samples\\val1A.dat")
    # sample = readData("CARP_samples\\val4A.dat")
    # sample = readData("CARP_samples\\val7A.dat")

    print sample
    printHead(sample)

    free = free_Set(sample)
    print free

    vmap = matrixTran(sample)
    test1 = dij.Dijkstra(vmap)
    test1.go_all()
    # print test1.d
    rt = path_scanning(free, test1.d, sample[6],5)
    # print rt
    printRoute(rt)
