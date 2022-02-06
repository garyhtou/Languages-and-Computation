"""
Gary Tou
CPSC 3400, HW 3 - Python Garbage Collector
1/19/2022
https://seattleu.instructure.com/courses/1602042/assignments/6989793
"""

import sys


class Graph:
    """
    An adjacency list data structure that represents a graph
    """

    def __init__(self, num_block) -> None:
        """
        Create a graph

        Args:
            num_block (int): Number of heap blocks
        """

        # Initialize the graph for the heap blocks
        self.adjacency = {}
        for i in range(num_block):
            self.adjacency[f'{i}'] = []

    def vertices(self):
        """
        Get a list of vertices in the graph

        Returns:
            list of strings: vertices in the graph
        """
        return list(self.adjacency.keys())

    def pointers(self):
        """
        Get a list of pointer vertices in the graph

        Returns:
            list of strings: Pointer vertices in the graph
        """

        # Pointers can't be digits
        return [k for k in self.adjacency.keys() if not k.isdigit()]

    def heads(self, vertex):
        """
        Get a list of heads from a vertex (edges that have the vertex as a tail)

        Args:
            vertex (string): Vertex (tail) to get heads from

        Returns:
            list of strings: Heads from the vertex
        """
        return self.adjacency[vertex]

    def add_edge(self, vertex, reference):
        """
        Add an edge to the graph. It will create the vertex if it doesn't already exist

        Args:
            vertex ([type]): [description]
            reference ([type]): [description]
        """
        # Dyanmically add a vertex if it doesn't exist (used for pointer vars)
        if vertex not in self.adjacency:
            self.adjacency[vertex] = []

        if reference not in self.adjacency:
            self.adjacency[reference] = []

        self.adjacency[vertex].append(reference)


def sweep_mark(filename):
    """
    Calculates the 'marked' and 'swept' nodes in the input file.
    Assumptions:
    - The first line of the input file is the number of heap blocks
    - There is at least one heap block
    - The rest of the lines are the edges of the graph, separated by a comma
      with no spaces
    - Variable names are unique.
    - Variable names consists of letters, digits, and underscores but cannot
      begin with a digit.
    - Heap blocks are numbered from 0 to numBlocks - 1 (this is their name)

    Args:
        filename (string): Input file

    Returns:
        dict: {'marked': list of int, 'swept': list of int}: The marked and swept nodes

    >>> # This doctest requires the instructor-provided sample input file
    ... try:
    ...     parse("sample1.txt")
    ... except FileNotFoundError:
    ...     ("This doctest failed because the instructor-provided "
    ...      "'sample1.txt' input file was not present.")
    Marked nodes: 0 1 2 6 7
    Swept nodes: 3 4 5 8 9
    """

    def follow(vertex):
        """
        Helper function for traversing the graph

        Args:
            vertex (string): The vertex to follow (start from)
        """
        if vertex not in marked:
            marked.append(vertex)

        heads = graph.heads(vertex)
        for v in heads:
            follow(v)

    # Variable to hold the graph
    graph = None

    try:
        # Create and fill graph with input data
        with open(filename) as file:
            graphData = parse(file)
            graph = Graph(graphData["numBlocks"])

            for edge in graphData["edges"]:
                graph.add_edge(edge[0], edge[1])
    except FileNotFoundError:
        print("File not found")
        sys.exit(1)

    # Now that the graph has been created, we can traverse it starting from the
    # pointers to compute the reachable vertices (nodes)
    marked = []
    for v in graph.pointers():
        follow(v)

    # Compute the unreachable vertices (inverse of reachable/marked vertices)
    swept = []
    for v in graph.vertices():
        if v not in marked:
            swept.append(v)

    # Filter out pointers and sort
    marked = sorted([int(v) for v in marked if v.isdigit()])
    swept = sorted([int(v) for v in swept if v.isdigit()])

    return {"marked": marked, "swept": swept}


def parse(file):
    """
    Parse the input file into easy to work with data structures

    Args:
        file (TextIoWrapper): Input file

    Returns:
        dict: {'numBlocks': int, edges: list of tuples (string, string)}: Parsed data

    >>> # This doctest requires the instructor-provided sample input file
    ... try:
    ...     with open(filename) as file:
    ...         parse(file)
    ... except FileNotFoundError:
    ...     ("This doctest failed because the instructor-provided "
    ...      "'sample1.txt' input file was not present.")
    {'numBlocks': 10, 'edges': [('p', '0'), ('0', '1'), ('1', '7'), ('r', '2'), ('2', '0'), ('4', '1'), ('4', '5'), ('5', '4'), ('5', '9'), ('s', '6'), ('8', '4'), ('9', '8')]}
    """
    graphData = {"numBlocks": None, "edges": []}

    try:
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
    except:
        print("Input file is improperly formatted")
        sys.exit(1)


def format_output(data):
    return ' '.join([str(v) for v in data])


def main(filepath):
    output = sweep_mark(filepath)
    print("Marked:", format_output(output["marked"]))
    print("Swept:", format_output(output["swept"]))


if __name__ == '__main__':
    # Get the name of the input file from the command line (using sys.argv)
    try:
        filepath = sys.argv[1]
        main(filepath)
    except IndexError:
        # Exit if no input file is provided
        print("Usage: hw3 <filepath>")
        sys.exit(1)
