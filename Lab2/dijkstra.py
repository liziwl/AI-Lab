# encoding: utf-8
import heapq
import sys
import CARP


class Dijkstra(object):
    def __init__(self, vertexs):
        self.vertexs = vertexs  # 邻接矩阵
        self.dist = {}  # 相聚起始点的距离
        self.unVisited = []  # 准备访问点
        # self.visited = []  # 已经访问点

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

    def getNeighbors(self, nodeID):
        # 返回邻接字典
        return self.vertexs[nodeID]

    def printGraph(self):
        for it in self.vertexs:
            print it, self.vertexs.get(it)


class Node(object):
    def __init__(self, nodeID):
        self.nodeID = nodeID
        self.prev = None
        self.dist = sys.maxint

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

    def __str__(self):
        return "<ID: {}>\n<prev: {}>\n<distance: {}>".format(self.nodeID, self.prev, self.dist)

    def __repr__(self):
        return str(self)


if __name__ == '__main__':
    sample = CARP.readData("CARP_samples\\egl-e1-A.dat")
    print sample

    vmap = CARP.matrixTran(sample)

    test1 = Dijkstra(vmap)
    test1.printGraph()
    print test1.search(19, 54)
