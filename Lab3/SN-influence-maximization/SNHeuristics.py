# -*- coding: utf-8 -*-

import networkx as nx
import heapq as hq
import SNSim
import time
import json

# [Kempe et al.] "The high-degree heuristic chooses nodes v in order of decreasing degrees. 
# Considering high-degree nodes as influential has long been a standard approach 
# for social and other networks [3, 83], and is known in the sociology literature 
# as 'degree centrality'."
# -> Calculates the k nodes of highest degree
# -> Time complexity: O(V log (k))
# -> Memory complexity: Theta(k)
def high_degree_nodes(k, G):

    if nx.is_directed(G):
        my_degree_function = G.out_degree
    else:
        my_degree_function = G.degree

    # the top k nodes to be returned; initialization with first k elements
    H = [(my_degree_function(i), i) for i in G.nodes()[0:k]] 
    hq.heapify(H)

    # iterate through the remaining nodes; add to heap if larger than heap root
    for i in G.nodes()[k:]: 
        if my_degree_function(i) > H[0][0]:
            hq.heappushpop(H, (my_degree_function(i), i))
 
    return H

# Generator variant of high_degree_nodes(k, G)
# More time-efficient for range calls if k log k > log V
# Generates _all_ sets of i nodes of highest degree, with 1 <= i <= k
# -> Time complexity: O(V log (V))
# -> Memory complexity: Theta(V)
def high_degree_nodes_gen(k, G):

    if nx.is_directed(G):
        my_degree_function = G.out_degree
    else:
        my_degree_function = G.degree

    V = [(my_degree_function(i), i) for i in G.nodes()]
    V.sort(reverse=True)
    N = [t[1] for t in V]

    for i in range(1, min(k, len(N)) + 1):
        yield N[:i]

def dump_degree_list(G):
    H = []

    for i in G.nodes():
        H.append((i, G.out_degree(i)))

    return H

# The SingleDiscount algorithm by [Chen et al., KDD'09] for any cascade model.
# -> Calculates the k nodes of highest degree, making discounts if direct neighbours are already chosen
# -> Time complexity: O(V k^2)
# -> Memory complexity: Theta(k)
def single_discount_high_degree_nodes(k, G):

    if nx.is_directed(G):
        my_degree_function = G.out_degree
    else:
        my_degree_function = G.degree

    D = []

    for i in range(k):
        # find the node of max out_degree, discounting any out-edge
        # to a node already in D
        maxoutdeg_i = -1
        v_i = -1
        for v in list(set(G.nodes()) - set(D)):
    	    outdeg = my_degree_function(v)
    	    for u in D:
                if G.has_edge(v, u):
                    outdeg -= 1
    	    if outdeg > maxoutdeg_i:
                maxoutdeg_i = outdeg
                v_i = v

        D.append(v_i)

    return D

# Generator variant of single_discount_high_degree_nodes(k, G)
# More time-efficient for repeated calls by Theta(V) 
# Generates _all_ sets of i nodes of discounted highest degree, with 1 <= i <= k
# -> Time complexity: O(V k^2)
# -> Memory complexity: Theta(k)
def single_discount_high_degree_nodes_gen(k, G):

    if nx.is_directed(G):
        my_degree_function = G.out_degree
    else:
        my_degree_function = G.degree

    D = []

    for i in range(k):
        # find the node of max out_degree, discounting any out-edge
        # to a node already in D
        maxoutdeg_i = -1
        v_i = -1
        for v in list(set(G.nodes()) - set(D)):
            outdeg = my_degree_function(v)
            for u in D:
                if G.has_edge(v, u):
                    outdeg -= 1
            if outdeg > maxoutdeg_i:
                maxoutdeg_i = outdeg
                v_i = v

        D.append(v_i)
        yield D

# The approximate greedy algorithm by [Kempe et al.] for any cascade model.
# -> Calculates the k nodes of supposedly max influence, and that influence
# -> Single-thread
# -> Time complexity: O(V k Time(SNSim.evaluate))
# -> Memory complexity: Theta(k + Memory(SNSim.evaluate))
def general_greedy(k, G, p, no_simulations, model):
    S = []

    for i in range(k):
        maxinfl_i = (-1, -1)
        v_i = -1
        for v in list(set(G.nodes()) - set(S)):
            eval_tuple = SNSim.evaluate(G, S+[v], p, no_simulations, model)
            if eval_tuple[0] > maxinfl_i[0]:
                maxinfl_i = (eval_tuple[0], eval_tuple[2])
                v_i = v

        print(i, v_i, maxinfl_i)
        S.append(v_i)

    return S, maxinfl_i

from multiprocessing import Pool

gl_G = 0                    # some globals needed to make pool.map(evaluate_mt, L) possible
gl_p = 0
gl_no_simulations = 0
gl_model = 0
gl_S = []
gl_k = 0

def evaluate_mt(v):
    eval_tuple = SNSim.evaluate(gl_G, gl_S+[v], gl_p, gl_no_simulations, gl_model)
    return (eval_tuple[0], eval_tuple[2], v)

# The approximate greedy algorithm by Kempe, et al. for any cascade model.
# -> Calculates the k nodes of supposedly max influence, and that influence
# -> Multi-thread
# -> Time complexity: O(V k Time(SNSim.evaluate))
# -> Memory complexity: Theta(k + Memory(SNSim.evaluate))
def general_greedy_mt(k, G, p, no_simulations, model, no_cores):
    global gl_G, gl_k, gl_p, gl_no_simulations, gl_model, gl_S
    gl_G = G
    gl_k = k
    gl_p = p
    gl_no_simulations = no_simulations
    gl_model = model

    maxinfl_i = -1
    maxci_i = -1
    v_i = -1

    for i in range(len(gl_S)+1, k+1):
        L = list(set(G.nodes()) - set(gl_S))
        pool = Pool(no_cores)
        res = pool.map(evaluate_mt, L)
        (maxinfl_i, maxci_i, v_i) = max(res)
        gl_S.append(v_i)
        print(i, maxinfl_i, maxci_i, gl_S, sep=' ')                     # k, mean, CI95, the seed set
        pool.close()
        pool.join()

    return gl_S, maxinfl_i, maxci_i

if __name__ == "__main__":
    # file = 'soc-Epinions1.txt'
    file = 'wiki-Vote.txt'
    # file = 'amazon0302.txt'
    # file = 'web-Google.txt'
    G = nx.read_edgelist(file, comments='#', delimiter='\t', create_using=nx.DiGraph(), nodetype=int, data=False)

    # file = 'facebook_combined.txt'
    # G = nx.read_edgelist(file, comments='#', delimiter=' ', create_using=nx.Graph(), nodetype=int, data=False)

    # a dictionary by key k, to be jsoned
    data_dump = {}

    # generator calls
    # for A in high_degree_nodes_gen(4, G):                             # heuristic 1: HIGHDEG
    for A in single_discount_high_degree_nodes_gen(400, G):             # heuristic 2: SDISC

    # non-generator calls
    # for k in range(1, 401):
        # A = list(map(lambda x: x[1], high_degree_nodes(k, G)))        # heuristic 1: HIGHDEG
        # A = single_discount_high_degree_nodes(k, G)                   # heuristic 2: SDISC

        res = SNSim.evaluate(G, A, 0.01, 100, 'IC')
        print(len(A), res[0], res[2], A, sep=' ')                       # k, mean, CI95, the seed set
        data_dump[len(A)] = (res[0], res[2], A)

    with open('data.json', 'w') as F:
        json.dump(data_dump, F)

    # general_greedy_mt(5, G, 0.01, 100, 'IC', 4)                       # heuristic 3: GENGREEDY
