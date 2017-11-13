# encoding: utf-8
import heapq
import sys
import CARP
import numpy as np


# 优化性能，运行时计算 or 提前算好查表
# 如果 REQUIRED EDGES 为 vertex的 1.2 倍或者以上时候，就是点较少的时候，采用提前查表，否则采用运行时计算
# 最后决定的生成方法，改成第一次使用的时候调用，然后储存结果，不一次性全部生成结果。
class Dijkstra(object):
    def __init__(self, vertexs):
        self.vertexs = vertexs  # 邻接矩阵
        self.dist = {}  # 相聚起始点的距离
        self.unVisited = []  # 准备访问点
        self.d = np.full((len(vertexs) + 1, len(vertexs) + 1), sys.maxint)  # 两点之间的距离

    def init_unvisited(self, start):
        self.dist.clear()
        self.unVisited = []  # 清空历史数据
        for v in self.vertexs:
            temp = Node(v)
            if temp.nodeID == start:
                temp.set_dist(0)
                self.dist[start] = 0  # 设置起始点
            heapq.heappush(self.unVisited, temp)

    def search(self, start, end):
        self.init_unvisited(start)
        while len(self.unVisited) > 0:  # 如果准备访问列表不为空
            top = heapq.heappop(self.unVisited)  # 弹出最小距离点
            if top.nodeID == end:
                return top
            neighbors = self.get_neighbors(top.nodeID)  # 获取该点邻接点
            for neighbor in neighbors:
                alt = top.dist + neighbors[neighbor][0]
                if neighbor in self.dist:
                    if alt < self.dist[neighbor]:
                        self.dist[neighbor] = alt
                        self.update_node(top, neighbor, alt)
                else:
                    self.dist[neighbor] = alt
                    self.update_node(top, neighbor, alt)
        return None

    def update_node(self, current, nextID, dist):
        index = 0
        for i in range(0, len(self.unVisited)):
            if self.unVisited[i].nodeID == nextID:
                self.unVisited[i].set_prev(current)
                self.unVisited[i].set_dist(dist)
                index = i
                break
        heapq._siftdown(self.unVisited, 0, index)

    def go_all(self):
        # print "maxINT:" + str(sys.maxint)
        for i in range(1, len(self.d)):
            for j in range(i, len(self.d[i])):
                temp = self.search(i, j)
                if temp is not None:
                    # print temp.dist
                    self.d[i][j] = temp.dist
                    self.d[j][i] = temp.dist

    def get_dist(self, i, j):
        if self.d[i][j] != sys.maxint:
            return self.d[i][j]
        else:
            temp = self.search(i, j)
            if temp is not None:
                self.d[i][j] = temp.dist
                self.d[j][i] = temp.dist
                return temp.dist
            else:
                return sys.maxint

    def get_neighbors(self, nodeID):
        # 返回邻接字典
        return self.vertexs[nodeID]

    def print_graph(self):
        for it in self.vertexs:
            print it, self.vertexs.get(it)


class Node(object):
    def __init__(self, nodeID):
        self.nodeID = nodeID  # ID
        self.prev = None  # 前一个节点
        self.dist = sys.maxint  # 距离起始点的距离

    def __cmp__(self, other):
        if self.dist < other.dist:
            return -1
        elif self.dist > other.dist:
            return 1
        else:
            return 0

    def set_prev(self, prev):
        self.prev = prev

    def set_dist(self, dist):
        self.dist = dist

    def str_with_indent(self, indent):
        s1 = "<ID: {}>\n".format(self.nodeID)
        if self.prev is not None:
            s2 = "\t<prev: {}>\n".format(self.prev.str_with_indent(indent + 1))
        else:
            s2 = "<prev: None>\n"
        s3 = "<distance: {}>".format(self.dist)
        for i in range(0, indent):
            s2 = "\t" + s2
            s3 = "\t" + s3
        return s1 + s2 + s3

    def __str__(self):
        return self.str_with_indent(0)

    def __repr__(self):
        return str(self)


if __name__ == '__main__':
    sample = CARP.read_data("CARP_samples\\egl-s1-A.dat")
    print sample

    vmap = CARP.matrix_tran(sample)

    test1 = Dijkstra(vmap)
    test1.print_graph()
    # print test1.search(0, 5)
    test1.go_all()
    print test1.d
    print len(test1.d)
