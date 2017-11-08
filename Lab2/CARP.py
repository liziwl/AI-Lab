# encoding: utf-8
import re
import dijkstra as dij
import copy
import sys


def readData(filename):
    # 0-7行，数据定义
    # 8行开始，数据本体
    f = open(filename, 'r')
    Pattern = ["NAME : (.*)",
               "VERTICES : ([0-9]*)",
               "DEPOT : ([0-9]*)",
               "REQUIRED EDGES : ([0-9]*)",
               "NON-REQUIRED EDGES : ([0-9]*)",
               "VEHICLES : ([0-9]*)",
               "CAPACITY : ([0-9]*)",
               "TOTAL COST OF REQUIRED EDGES : ([0-9]*)"]
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
        if it[3] != 0:
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


def better(u, u2, remain, rule):
    function = {
        1: rule1,
        # 2: rule2,
        # 3: rule3,
        # 4: rule4,
        # 5: rule5
    }
    func = function[rule]
    func(u, u2, remain)


def rule1(u, u2, remain):
    rate1 = u[2] / (remain - u[3])
    rate2 = u2[2] / (remain - u2[3])
    if rate1 > rate2:
        return rate1
    else:
        return rate2


def rule2(u, u2, remain):
    rate1 = u[2] / (remain - u[3])
    rate2 = u2[2] / (remain - u2[3])
    if rate1 < rate2:
        return rate1
    else:
        return rate2


def removeFree(free,edge):
    index = -1
    [start, end, cost, demand]=edge
    for i in range(0,len(free)):
        [istart, iend, icost, idemand] = free[i]
        if (istart==start and iend ==end) or (istart==end and iend ==start):
            index = i
            break
    del free[index]

def path_scanning(graph, distance,capacity):
    '''
    :param graph: 邻接矩阵
    :param distance: Dijkstra对象中的每2个点之间的距离
    :param capacity: 容量
    :return:
    '''
    k = 0
    free = copy.deepcopy(graph)
    while True:
        k = k + 1
        r = [] # route list
        l = [] # load list
        c = [] # cost list
        load = 0
        cost = 0
        remain = capacity
        i = 1
        while True:
            dist = sys.maxint
            edge = None
            for it in free | load + it[3] < capacity:
                # it格式 [a,b,c,d] a起点 0，b终点 1，c COST 2，d DEMAND 3
                [istart,iend,icost,idemand] =it
                # 正面
                if distance[i][istart] <dist:
                    dist = distance[i][istart]
                    edge = it
                elif dist == distance[i][istart] and better(it,edge,remain,1):
                    edge =it
                # 反面
                if distance[i][iend] <dist:
                    dist = distance[i][iend]
                    edge = [iend,istart,icost,idemand]
                elif dist == distance[i][iend] and better(it,edge,remain,1):
                    edge = [iend, istart, icost, idemand]
            r.append(edge)
            removeFree(free,edge)
            free.remove(it)
            load = load + idemand
            cost = cost + dist + icost
            i = iend
            if len(free) == 0 or dist == sys.maxint:
                break
            cost = cost + dist[i][i]
        if len(free) == 0:
            break


class task:
    def __init__(self, id, start, end, cost, demand):
        self.id = id
        self.start = start
        self.end = end
        self.cost = cost
        self.demand = demand


if __name__ == '__main__':
    # print readData("CARP_samples\\egl-e1-A.dat")
    # print readData("CARP_samples\\egl-s1-A.dat")
    # print readData("CARP_samples\\gdb1.dat")
    # print readData("CARP_samples\\gdb10.dat")
    # print readData("CARP_samples\\val1A.dat")
    # print readData("CARP_samples\\val4A.dat")
    # print readData("CARP_samples\\val7A.dat")

    sample = readData("CARP_samples\\gdb1.dat")
    print sample

    graph = free_Set(sample)
    # printGraph(graph)
    # vmap = matrixTran(sample)

    # test1 = dij.Dijkstra(vmap)
    # test1.printGraph()
