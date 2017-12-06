# encoding: utf-8
import graph

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


if __name__ == "__main__":
    d = graph.read_network("network.txt")
    # print d

    d1 = graph.list2dict(d[2])
    graph.print_graph(d1)
    print "-----------------------------"
    d2 = graph.inv_list2dict(d[2])
    graph.print_graph(d2)
