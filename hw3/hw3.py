"""
Gary Tou
CPSC 3400, HW 3 - Python Garbage Collector
1/19/2022
https://seattleu.instructure.com/courses/1602042/assignments/6989793
"""

# Needs graph
# adjacency matrix/list

# TODO: docstrings

import sys


class Graph:

    def __init__(self, num_block) -> None:
        # Initialize the graph for the heap blocks
        self.adjacency = {}
        for i in range(num_block):
            self.adjacency[f'{i}'] = []

    def verticies(self):
        return self.adjacency.keys()

    def pointers(self):
        # Pointers can't be digits
        return [k for k in self.adjacency.keys() if not k.isdigit()]

    def heads(self, vertex):
        return self.adjacency[vertex]

    def add_edge(self, vertex, reference):
        # Dyanmically add a vertex if it doesn't exist (used for pointer vars)
        if vertex not in self.adjacency:
            self.adjacency[vertex] = []

        self.adjacency[vertex].append(reference)


def sweep_mark(filename):
    def follow(vertex):
        if vertex not in marked:
            marked.append(vertex)

        heads = graph.heads(vertex)

        for v in heads:
            follow(v)

    try:
        graph = None

        # Create and fill graph with input data
        with open(filename) as file:
            graphData = parse(file)
            graph = Graph(graphData["numBlocks"])

            for edge in graphData["edges"]:
                graph.add_edge(edge[0], edge[1])

        # Compute the reachable vertices from the pointers
        marked = []
        for v in graph.pointers():
            follow(v)

        # Computer the unreachable vertices
        swept = []
        for v in graph.verticies():
            if v not in marked:
                swept.append(v)

        # Filter out pointers and sort
        marked = sorted([int(v) for v in marked if v.isdigit()])
        swept = sorted([int(v) for v in swept if v.isdigit()])

        return {"marked": marked, "swept": swept}

    except FileNotFoundError:
        print("File not found")
        pass


def parse(file):
    graphData = {"numBlocks": None, "edges": []}

    while (line := file.readline().strip()):
        # Skips empty lines
        if len(line) == 0:
            continue

        # Set the num blocks variable (first line)
        if graphData["numBlocks"] == None:
            graphData["numBlocks"] = int(line)
            continue

        tail, head = line.split(',')
        graphData["edges"].append((tail, head))

    return graphData


def main(filepath):
    output = sweep_mark(filepath)
    # TODO: format print
    print("Marked:", output["marked"])
    print("Swept:", output["swept"])


if __name__ == '__main__':
    # Get the name of the input file from the command line (using sys.argv)
    try:
        filepath = sys.argv[1]
        main(filepath)
    except IndexError:
        # Exit if no input file is provided
        print("Usage: hw3 <filepath>")
        sys.exit(1)
