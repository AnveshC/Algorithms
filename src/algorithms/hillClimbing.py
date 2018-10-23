#!/usr/bin/python
# CSE 6140 Fall 2017 Project: LS1

from __future__ import print_function
from __future__ import division
import os.path
import random as rd
from timeit import default_timer as timer


# hillclimb main script
def hillClimbing(graph, cutoff_time, randSeed, outPutName, node_num):

    # populate original vertex cover and initialize dictionary for vertex node
    vc = set([num for num in range(1, node_num + 1)])
    nodeDict = {}

    # populate nodeDict where vertex degree is key
    for node in graph.node():
        if graph.degree(node) not in nodeDict:
            nodeDict[graph.degree(node)] = list()
        nodeDict[graph.degree(node)].append(node)

    # out put file
    # outPutName = file.split('.')[0] + '_' + 'LS1HC' + '_' + str(cutoff_time) + '_' + str(randSeed)
    trace = open('{}.trace'.format(outPutName), 'w')
    sol = open('{}.sol'.format(outPutName), 'w')

    # main loop and loop variables
    sizeOld = len(vc)
    rd.seed(randSeed)
    start = timer()
    for key in nodeDict.keys(): # loop key in asc order
        while nodeDict[key]: # loop vertex
            # select random vertex node of same degree
            rand = rd.random()*len(nodeDict[key])
            node = nodeDict[key][int(rand)]
            nodeDict[key].remove(node)
            # check VC
            vc.remove(node)
            if isVC(graph, vc) is -1:
                vc.add(node)
            # trace improved sol
            current = timer()
            sizeNew = len(vc)
            if sizeNew < sizeOld:
                line = str(current - start) + ', ' + str(sizeNew) + '\n'
                trace.write(line)
            sizeOld = sizeNew
            # cutoff_time 
            if current - start > cutoff_time:
                print ('timeout')
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

# check if a vertex cover is a solution
def isVC(graph, vc):
    for edge in graph.edges():
        if edge[0] not in vc and edge[1] not in vc: 
                return -1
    return 1
