from __future__ import print_function
from __future__ import division
import time
from operator import itemgetter


class BranchBound:
    def __init__(self, graph, cutoff_time, solution_file, trace_file):
        self.graph = graph
        self.cutoff_time = cutoff_time
        self.lower_bound = self.graph.number_of_nodes() - 1
        self.best_length = self.lower_bound
        self.best_solution_vertices = set()
        self.solution_found = False
        self.solution_file_name = solution_file
        self.trace_file_name = trace_file

    @staticmethod
    def run_approx(graph):
        vertex_cover = set()
        edges_covered = set()

        for num, edge in enumerate(graph.edges()):
            u = edge[0]
            v = edge[1]
            if (u, v) not in edges_covered and (v, u) not in edges_covered:
                # Add the endpoints of the current edge
                vertex_cover.add(u)
                vertex_cover.add(v)
                # Union operation over already covered edges and the edges being covered by u and v
                edges_covered = edges_covered.union(set(graph.edges([u, v])))

        # return len(vertex_cover)
        return len(vertex_cover)

    def run(self):
        # Start Timer
        start_time = time.time()
        trace_set = list()

        # Note the initial best solution, which is just the total number of edges - 1
        current_time = time.time() - start_time
        trace_set.append([current_time, self.best_length])

        # Run approx solution to get initial set of vertices
        while time.time() < start_time + self.cutoff_time and not self.solution_found:
            # Sort the edges based on degree, and extract the node with max degree
            node_degrees = list(self.graph.degree())
            current_vertex = max(node_degrees, key=itemgetter(1))[0]

            # Create two sub graphs, one with the current node delete, and the other with its neighbors deleted
            subgraph_add_vertex = self.graph.copy()
            subgraph_add_neighbors = self.graph.copy()
            subgraph_add_vertex.remove_node(current_vertex)
            vertex_neighbors = list(subgraph_add_neighbors.neighbors(current_vertex))
            subgraph_add_neighbors.remove_nodes_from(vertex_neighbors)
            subgraph_add_neighbors.remove_node(current_vertex)

            # Get approximation on the lower bound for the two sub graphs
            approx_vertex = self.run_approx(subgraph_add_vertex) / 2
            approx_neighbors = self.run_approx(subgraph_add_neighbors) / 2

            # Check which solution has better promise, and add corresponding vertices to the best solution set
            if approx_vertex + 1 <= approx_neighbors + len(vertex_neighbors):
                self.best_solution_vertices.add(current_vertex)
                self.graph.remove_node(current_vertex)
                temp = len(self.best_solution_vertices) + approx_vertex

            else:
                for vertex in vertex_neighbors:
                    self.best_solution_vertices.add(vertex)
                    # temp_solution_vertices.discard(vertex)
                self.graph.remove_nodes_from(vertex_neighbors)
                self.graph.remove_node(current_vertex)
                temp = len(self.best_solution_vertices) + approx_neighbors

            # If there is a change on the lower bound, note it for trace
            if temp != self.lower_bound:
                self.lower_bound = temp
                current_time = time.time() - start_time
                trace_set.append([current_time, self.lower_bound])

            # Check if we can stop looking
            if self.graph.number_of_edges() == 0:
                print('Found solution!')
                self.solution_found = True
        # Informative message to note that the solution was not found within the cutoff time
        if not self.solution_found:
            print('Incomplete solution!')

        # Write the trace and sol files
        trace_file = open(self.trace_file_name, 'w')
        solution_file = open(self.solution_file_name, 'w')
        solution_file.write('%d\n' % len(self.best_solution_vertices))
        self.best_solution_vertices = sorted(list(self.best_solution_vertices))
        for idx, vertex in enumerate(self.best_solution_vertices):
            if idx != len(self.best_solution_vertices)-1:
                solution_file.write('%d,' % vertex)
            else:
                solution_file.write('%d' % vertex)

        for idx, vertex in enumerate(trace_set):
            if idx != len(trace_set) - 1:
                trace_file.write('%.2f, %d\n' % (vertex[0], vertex[1]))
            else:
                trace_file.write('%.2f, %d' % (vertex[0], vertex[1]))
