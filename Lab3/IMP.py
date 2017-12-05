# encoding: utf-8
import graph

# ISE 评估一个seed的影响 用入度
# IMP 产生一个较好的seed

if __name__ == "__main__":
    d = graph.read_network("network.txt")
    # print d

    d1 = graph.list2dict(d[2])
    graph.print_graph(d1)
    print "-----------------------------"
    d2 = graph.inv_list2dict(d[2])
    graph.print_graph(d2)
