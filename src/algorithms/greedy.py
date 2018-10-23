from __future__ import print_function
from __future__ import division
from operator import itemgetter
import os.path
import random as rd
from timeit import default_timer as timer


def greedy(graph, cutoff, randSeed, outPutName):
    vc = set(graph.nodes())
    M = set()
    trace = open('{}.trace'.format(outPutName), 'w')
    sol = open('{}.sol'.format(outPutName), 'w')

    sizeOld = len(vc)
    rd.seed(randSeed)
    start = timer()
    coveredEdges = graph.edges()
    subgraph = graph.copy()
#	sorted(graph.degree_iter(),key=itemgetter(1))

    while coveredEdges: # checking if the list is not empty
        # Sort the edges based on degree, and choose the node with minimum degree
        node_degrees = list(subgraph.degree())#list(graph.degree())
        current_vertex = min(node_degrees, key=itemgetter(1))[0]
        # print (current_vertex)
        #subgraph = graph.copy()
        vertex_neighbors = list(subgraph.neighbors(current_vertex))
        # print (vertex_neighbors)
        subgraph.remove_nodes_from(vertex_neighbors)
        subgraph.remove_node(current_vertex)
        #print (len(subgraph.node()))
        vc.remove(current_vertex)
        vc.difference(set(vertex_neighbors))

        coveredEdges = subgraph.edges()
        current = timer()
        sizeNew = len(vc)
        if sizeNew < sizeOld:
            line = str(current - start) + ', ' + str(sizeNew) + '\n'
            trace.write(line)
            sizeOld = sizeNew
        # cutoff
        if current - start > cutoff:
            # print ('timeout')
            break
    end = timer()
    # write sol and trace
    sol.write(str(sizeOld) + '\n')
    for num in vc:
        sol.write(str(num) + ',')
    sol.seek(-1, os.SEEK_END)
    sol.truncate()
    trace.close()
    sol.close()

    # return
    return (end - start), len(vc)


# cutoff = 600
# randSeed = [2, 101, 193, 251, 337, 439, 521, 601, 701, 941]
# avgT = 0
# avgSize = 0
# for i in range(10):
#     t, s = greedy(cutoff, randSeed[i])
#     avgT += t
#     avgSize += s

# print (file)
# print (avgT/10)
# print (int(avgSize/10))























