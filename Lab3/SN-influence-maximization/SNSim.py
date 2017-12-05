# -*- coding: utf-8 -*-

import networkx as nx
import random
import numpy
import math
import time
import sys

# Simulates the Independent Cascade propagation model 
# on graph G starting with the seed nodes in "a".
# Returns the number of nodes reached by the propagation
# -> Time complexity: a very worst case of O(V^3) (lower with lower "p")
# -> Memory complexity: O(V)
def IC_model(G, a, p):              # a: the set of initial active nodes
                                    # p: the system-wide probability of influence on an edge, in [0,1]
    A = set(a)                      # A: the set of active nodes, initially a
    B = set(a)                      # B: the set of nodes activated in the last completed iteration
    converged = False

    while not converged:
        nextB = set()
        for n in B:
            for m in set(G.neighbors(n)) - A:
                prob = random.random()	# in the range [0.0, 1.0)
                if prob <= p:
                    nextB.add(m)
        B = set(nextB)
        if not B:
            converged = True
        A |= B

    return len(A)

# Simulates the Weighted Cascade propagation model 
# on graph G starting with the seed nodes in "a".
# Returns the number of nodes reached by the propagation
# -> Time complexity: a very worst case of O(V^3)
# -> Memory complexity: O(V)
def WC_model(G, a):                 # a: the set of initial active nodes
                                    # each edge from node u to v is assigned probability 1/in-degree(v) of activating v
    A = set(a)                      # A: the set of active nodes, initially a
    B = set(a)                      # B: the set of nodes activated in the last completed iteration
    converged = False
 
    if nx.is_directed(G):
        my_degree_function = G.in_degree
    else:
        my_degree_function = G.degree

    while not converged:
        nextB = set()
        for n in B:
            for m in set(G.neighbors(n)) - A:
                prob = random.random()	# in the range [0.0, 1.0)
                p = 1.0/my_degree_function(m)
                if prob <= p:
                    nextB.add(m)
        B = set(nextB)
        if not B:
            converged = True
        A |= B

    return len(A)

# Evaluates a given seed set A,
# simulated "no_simulations" times
# Returns a tuple: the mean, stdev, and 95% confidence interval
def evaluate(G, A, p, no_simulations, model):
    results = []

    if model == 'WC':
        for i in range(no_simulations):
            results.append(WC_model(G, A))
    elif model == 'IC':
        for i in range(no_simulations):
            results.append(IC_model(G, A, p))

    return numpy.mean(results), numpy.std(results), 1.96 * numpy.std(results) / math.sqrt(no_simulations)

# Evaluates "no_samples" random seed sets A of size "k",
# each simulated "no_simulations" times.
# Returns a list of "no_samples" tuples (mean, stdev, and 95% confidence interval)
def RND_evaluate(G, k, p, no_samples, no_simulations, model):
    results = []

    for i in range(no_samples):
        A = random.sample(G.nodes(), k)
        results.append(evaluate(G, A, p, no_simulations, model))

    return results

# Reads in a seed set A from stdin: 
# a number of whitespace-separated node ids on one line
def input_A():
    try:
        A = list(map(int, sys.stdin.readline().strip().split()))
    except:
        pass

    return A or []

if __name__ == "__main__":                  # in test rather than import mode
    
    p = 0.01                                # "p" only matters for IC_model
    k = 10
    model = 'IC'
    no_simulations = 100
    no_samples = 1

    # file = 'soc-Epinions1.txt'
    # file = 'wiki-Vote.txt'
    # file = 'amazon0302.txt'
    # file = 'web-Google.txt'
    # G = nx.read_edgelist(file, comments='#', delimiter='\t', create_using=nx.DiGraph(), nodetype=int, data=False)
    file = 'facebook_combined.txt'
    G = nx.read_edgelist(file, comments='#', delimiter=' ', create_using=nx.Graph(), nodetype=int, data=False)
 
    tstart = time.process_time()
    # print(RND_evaluate(G, k, p, no_samples, no_simulations, model))
    print(evaluate(G, input_A(), p, no_simulations, model))
    print("Elapsed time: ", time.process_time() - tstart)
