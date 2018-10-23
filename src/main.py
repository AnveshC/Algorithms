#!/usr/bin/python
# CSE 6140 Fall 2017 Project: Main Script

from __future__ import print_function
from __future__ import division
import sys
import os.path
import networkx as nx
from algorithms.BranchBound import BranchBound
from algorithms.Approximation import Approximation
from algorithms.hillClimbing import hillClimbing
from algorithms.greedy import greedy
from os import getcwd
from os.path import basename
num_args = len(sys.argv)

# INPUT ARGUMENT CHECKS
# Check if minimum number of arguments have been supplied
if num_args < 7:
    print('Error: not enough input arguments')
    exit(1)

# Check if proper algorithm argument has been supplied
alg_type = sys.argv[4]
if alg_type not in ['BnB', 'Approx', 'LS1', 'LS2']:
    print('Error: incorrect algorithm type')
    exit(1)

# Check if the seed value has been given for local search and approximation
if alg_type != 'BnB' and num_args < 8:
    print('Error: random seed not supplied')
    exit(1)
else:
    random_seed = sys.argv[8]

cutoff_time = float(sys.argv[6])
# Check if minimum cutoff time has been supplied
if cutoff_time < 600:
    print('Error: cutoff time is too short')
    if alg_type == 'BnB':
        print('Setting cutoff time to 1200 for BnB')
        cutoff_time = 1200
    else:
        print('Setting cutoff time to 600')
        cutoff_time = 600

input_file_name = sys.argv[2]
# Check if the input file exists
if os.path.isfile(input_file_name) is False:
    print('Error: cannot find input file')
    exit(1)

# READ THE INPUT GRAPH FILE
# Create a graph object and read the graph file
graph = nx.Graph()
with open(input_file_name, 'r') as f:
    graph_info = list(map(lambda e: int(e), next(f).split()))
    for i, line in enumerate(f):
        vertices_of_i = list(map(lambda e: int(e), line.split()))
        if len(vertices_of_i) > 0:
            graph.add_node(i + 1)
        for vertex in vertices_of_i:
            graph.add_edge(i+1, vertex)

# print('Added {0} nodes and {1} edges'.format(graph.number_of_nodes(), graph.number_of_edges()))
# CALL APPROPRIATE ALGORITHM
file_base = basename(input_file_name)
current_dir = basename(getcwd())
output_prefix = './output/'
if current_dir == 'src':
    output_prefix = '../output/'
input_file_end = file_base.rfind('.')
instance_name = file_base[0: input_file_end]
if alg_type == 'BnB':
    solution_file = output_prefix + instance_name + '_BnB_' + str(int(cutoff_time)) + '.sol'
    trace_file = output_prefix + instance_name + '_BnB_' + str(int(cutoff_time)) + '.trace'
    solver = BranchBound(graph, cutoff_time, solution_file, trace_file)
    solver.run()
elif alg_type == 'Approx':
    solution_file = output_prefix + instance_name + '_Approx_' + str(int(cutoff_time)) + '.sol'
    trace_file = output_prefix + instance_name + '_Approx_' + str(int(cutoff_time)) + '.trace'
    solver = Approximation(graph, solution_file, trace_file)
    solver.run()
elif alg_type == 'LS1':
    outPutName = output_prefix + instance_name + '_LS1HC_' + str(int(cutoff_time)) + str(random_seed)
    hillClimbing(graph, cutoff_time, random_seed, outPutName, graph_info[0])
else:
    outPutName = output_prefix + instance_name + '_LS2G_' + str(int(cutoff_time)) + str(random_seed)
    greedy(graph, cutoff_time, random_seed, outPutName)
