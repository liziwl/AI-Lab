# encoding: utf-8
import heapq
import sys
import CARP
import numpy as np


class Dijkstra(object):
    def __init__(self, vertexs):
        self.vertexs = vertexs  # 邻接矩阵
        self.dist = {}  # 相聚起始点的距离
        self.unVisited = []  # 准备访问点
        self.d = np.full((len(vertexs) + 1, len(vertexs) + 1), sys.maxint)  # 两点之间的距离

    def initUnVisited(self, start):
        self.dist.clear()
        self.unVisited = []  # 清空历史数据
        for v in self.vertexs:
            temp = Node(v)
            if temp.nodeID == start:
                temp.setDist(0)
                self.dist[start] = 0  # 设置起始点
            heapq.heappush(self.unVisited, temp)

    def search(self, start, end):
        self.initUnVisited(start)
        while len(self.unVisited) > 0:  # 如果准备访问列表不为空
            top = heapq.heappop(self.unVisited)  # 弹出最小距离点
            if top.nodeID == end:
                return top
            neighbors = self.getNeighbors(top.nodeID)  # 获取该点邻接点
            for neighbor in neighbors:
                alt = top.dist + neighbors[neighbor][0]
                if neighbor in self.dist:
                    if alt < self.dist[neighbor]:
                        self.dist[neighbor] = alt
                        self.updateNode(top, neighbor, alt)
                else:
                    self.dist[neighbor] = alt
                    self.updateNode(top, neighbor, alt)
        return None

    def updateNode(self, current, nextID, dist):
        index = 0
        for i in range(0, len(self.unVisited)):
            if self.unVisited[i].nodeID == nextID:
                self.unVisited[i].setPrev(current)
                self.unVisited[i].setDist(dist)
                index = i
                break
        heapq._siftdown(self.unVisited, 0, index)

    def go_all(self):
        # print "maxINT:" + str(sys.maxint)
        for i in range(1, len(self.d)):
            for j in range(1, len(self.d[i])):
                temp = self.search(i, j)
                if temp is not None:
                    # print temp.dist
                    self.d[i][j] = temp.dist

    def getNeighbors(self, nodeID):
        # 返回邻接字典
        return self.vertexs[nodeID]

    def printGraph(self):
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

    def setPrev(self, prev):
        self.prev = prev

    def setDist(self, dist):
        self.dist = dist

    def str_withIndent(self, indent):
        s1 = "<ID: {}>\n".format(self.nodeID)
        if self.prev is not None:
            s2 = "\t<prev: {}>\n".format(self.prev.str_withIndent(indent + 1))
        else:
            s2 = "<prev: None>\n"
        s3 = "<distance: {}>".format(self.dist)
        for i in range(0, indent):
            s2 = "\t" + s2
            s3 = "\t" + s3
        return s1 + s2 + s3

    def __str__(self):
        return self.str_withIndent(0)

    def __repr__(self):
        return str(self)


if __name__ == '__main__':
    sample = CARP.readData("CARP_samples\\gdb1.dat")
    print sample

    vmap = CARP.matrixTran(sample)

    test1 = Dijkstra(vmap)
    test1.printGraph()
    # print test1.search(0, 5)
    test1.go_all()
    print test1.d
    print  len(test1.d)
