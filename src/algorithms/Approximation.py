from __future__ import print_function
from __future__ import division


class Approximation:
    def __init__(self, graph, solution_file, trace_file):
        self.graph = graph
        self.solution_file_name = solution_file
        self.trace_file_name = trace_file
        self.vertex_cover = set()

    def run(self):
        edges_covered = set()

        for num, edge in enumerate(self.graph.edges()):
            u = edge[0]
            v = edge[1]
            if (u, v) not in edges_covered and (v, u) not in edges_covered:
                # Add the endpoints of the current edge
                self.vertex_cover.add(u)
                self.vertex_cover.add(v)
                # Union operation over already covered edges and the edges being covered by u and v
                edges_covered = edges_covered.union(set(self.graph.edges([u, v])))

        # Write the sol file. No trace file is written
        trace_file = open(self.trace_file_name, 'w')
        solution_file = open(self.solution_file_name, 'w')
        solution_file.write('%d\n' % len(self.vertex_cover))
        best_solution_vertices = sorted(list(self.vertex_cover))
        for idx, vertex in enumerate(best_solution_vertices):
            if idx != len(best_solution_vertices) - 1:
                solution_file.write('%d,' % vertex)
            else:
                solution_file.write('%d' % vertex)
