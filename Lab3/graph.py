# encoding: utf-8
import random


class Graph:
    def __init__(self, node_dict, node_inv):
        self.node_dict = node_dict
        self.node_inv = node_inv
        # 存入邻接矩阵

    def nodes(self):
        counter = set()
        for node in self.node_inv:
            counter.add(node)
        for node in self.node_dict:
            counter.add(node)
        node_list = list(counter)
        node_list.sort()
        return node_list

    def get_weight(self, i, j):
        return self.node_dict[i][j]

    def get_neighbor(self, i):
        if i in self.node_dict:
            return self.node_dict[i]
        else:
            return []

    def get_parent(self, i):
        if i in self.node_inv:
            return self.node_inv[i]
        else:
            return []

    def get_thresh(self):
        thresh = {}
        for node in self.node_inv:
            if node not in thresh:
                thresh[node] = random.random()

        for node in self.node_dict:
            if node not in thresh:
                thresh[node] = random.random()
        return thresh


def list2dict(node_list):
    """
    列表转化为邻接矩阵
    :param node_list: 元数据
    :return: 邻接矩阵
    """
    dic = {}
    for i in range(0, len(node_list)):
        from_node, to_node, weight = node_list[i]
        if from_node in dic:
            node_dic = dic[from_node]
            node_dic[to_node] = weight
        else:
            temp = {}
            temp[to_node] = weight
            dic[from_node] = temp
    return dic


def inv_list2dict(node_list):
    """
    列表转化为逆邻接矩阵
    :param node_list: 元数据
    :return: 逆邻接矩阵
    """
    dic = {}
    for i in range(0, len(node_list)):
        from_node, to_node, weight = node_list[i]
        if to_node in dic:
            node_dic = dic[to_node]
            node_dic[from_node] = weight
        else:
            temp = {}
            temp[from_node] = weight
            dic[to_node] = temp
    return dic


def print_graph(node_dict):
    for it in node_dict:
        print it, node_dict.get(it)


def read_network(file_name):
    fData = []
    count = 0
    node_num = 0
    data_num = 0
    f = open(file_name, 'r')
    data = f.readlines()
    for it in data:
        temp = it.split()
        if count == 0:
            node_num = int(temp[0])
            data_num = int(temp[1])
        else:
            idata = [int(temp[0]), int(temp[1]), float(temp[2])]
            fData.append(idata)
            # print idata
        count += 1
    # print node_num
    # print data_num
    # print fData
    return node_num, data_num, fData


def read_seed(file_name):
    seed = []
    f = open(file_name, 'r')
    data = f.readlines()
    for it in data:
        seed.append(int(it))
    # print seed
    seed.sort()
    return seed


if __name__ == "__main__":
    d = read_network("network.txt")
    print d

    d1 = list2dict(d[2])
    print_graph(d1)
    print "-----------------------------"
    d2 = inv_list2dict(d[2])
    print_graph(d2)

    test = Graph(d1, d2)
    print test.get_weight(14, 10)
    print "***********************************"
    print test.get_neighbor(14)

    print_graph(test.node_inv)
    print test.get_parent(1)
    print test.nodes()
