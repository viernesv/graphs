import heapq
from collections import deque


class DirectedGraph:
    """
    Class to implement directed weighted graph
    - duplicate edges not allowed
    - loops not allowed
    - only positive edge weights
    - vertex names are integers
    """

    def __init__(self, start_edges=None):
        """
        Store graph info as adjacency matrix
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.v_count = 0
        self.adj_matrix = []

        # populate graph with initial vertices and edges (if provided)
        # before using, implement add_vertex() and add_edge() methods
        if start_edges is not None:
            v_count = 0
            for u, v, _ in start_edges:
                v_count = max(v_count, u, v)
            for _ in range(v_count + 1):
                self.add_vertex()
            for u, v, weight in start_edges:
                self.add_edge(u, v, weight)

    def __str__(self):
        """
        Return content of the graph in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if self.v_count == 0:
            return 'EMPTY GRAPH\n'
        out = '   |'
        out += ' '.join(['{:2}'.format(i) for i in range(self.v_count)]) + '\n'
        out += '-' * (self.v_count * 3 + 3) + '\n'
        for i in range(self.v_count):
            row = self.adj_matrix[i]
            out += '{:2} |'.format(i)
            out += ' '.join(['{:2}'.format(w) for w in row]) + '\n'
        out = f"GRAPH ({self.v_count} vertices):\n{out}"
        return out

    # ------------------------------------------------------------------ #

    def add_vertex(self) -> int:
        """
        Add new vertex to the graph
        """
        self.adj_matrix.append([0 for x in self.adj_matrix])
        for vertex in self.adj_matrix:
            vertex.append(0)
        self.v_count += 1
        return self.v_count


    def add_edge(self, src: int, dst: int, weight=1) -> None:
        """
        Add edge to the graph
        """
        if src not in range(len(self.adj_matrix)):
            return
        if dst not in range(len(self.adj_matrix)):
            return
        if weight < 0:
            return
        if src == dst:
            return
        else:
            self.adj_matrix[src][dst] = weight


    def remove_edge(self, src: int, dst: int) -> None:
        """
        Remove edge from the graph
        """
        if src not in range(len(self.adj_matrix)):
            return
        if dst not in range(len(self.adj_matrix)):
            return
        if src == dst:
            return
        else:
            self.adj_matrix[src][dst] = 0


    def get_vertices(self) -> []:
        """
        Return list of vertices in the graph
        """
        vertices = list()
        for v in range(len(self.adj_matrix)):
            vertices.append(v)
        return vertices


    def get_edges(self) -> []:
        """
        Return list of edges in the graph
        """
        vertices = self.get_vertices()
        edges = list()
        for i in vertices:
            for j in vertices:
                if self.adj_matrix[i][j] != 0:
                    edges.append(((i, j, self.adj_matrix[i][j])))
        return edges


    def is_valid_path(self, path: []) -> bool:
        """
        Return true if provided path is valid, False otherwise
        """
        if len(path) == 0:
            return True
        else:
            i = 0
            while i < (len(path) - 1):
                if self.adj_matrix[path[i]][path[i+1]] == 0:
                    return False
                i += 1
            return True


    def dfs(self, v_start, v_end=None) -> []:
        """
        Return list of vertices visited during DFS search
        Vertices are picked in ascending order
        """
        reachable = list()
        stack = list()

        if v_start not in self.get_vertices():
            return reachable
        else:
            stack.append(v_start)

            # implementation of DFS (provided by module exploration)
            while len(stack) != 0 and v_end not in reachable:
                vertex = stack.pop()
                if vertex not in reachable:
                    reachable.append(vertex)
                    successors = list()
                    for j in range(len(self.adj_matrix[vertex])):
                        if self.adj_matrix[vertex][j] != 0:
                            successors.append(j)
                    successors.sort(reverse=True)
                    for s in successors:
                        stack.append(s)
            return reachable


    def bfs(self, v_start, v_end=None) -> []:
        """
        Return list of vertices visited during BFS search
        Vertices are picked in ascending order
        """
        reachable = list()
        queue = list()

        if v_start not in self.get_vertices():
            return reachable
        else:
            queue.append(v_start)

            # implementation of BFS (provided by module exploration)
            while len(queue) != 0 and v_end not in reachable:
                vertex = queue.pop(0)
                if vertex not in reachable:
                    reachable.append(vertex)
                    successors = list()
                    for j in range(len(self.adj_matrix[vertex])):
                        if self.adj_matrix[vertex][j] != 0:
                            successors.append(j)
                    successors.sort()
                    for s in successors:
                        queue.append(s)
            return reachable


    def has_cycle(self):
        """
        Return True if graph contains a cycle, False otherwise
        """

        unvisited = list()                          # list of unvisited vertices
        stack = list()                              # list of successors of a vertex that are being processed/explored
        visited = list()                            # list of visited vertices whose children is being processed

        for vertex in self.get_vertices():
            unvisited.append(vertex)

        while len(unvisited) >= 0:
            stack.append(unvisited.pop(0))          # initialize DFS with the first vertex of the graph

            # modified implementation of DFS
            while len(stack) != 0:
                vertex = stack[len(stack) - 1]      # vertex currently processing the last element of the stack
                successors = list()
                for j in range(len(self.adj_matrix[vertex])):
                    if self.adj_matrix[vertex][j] != 0 and self.adj_matrix[vertex][j] not in visited:
                        successors.append(j)

                if len(successors) == 0:
                    stack.remove(vertex)
                    visited.append(vertex)
                else:
                    for s in successors:
                        print("vertex: ", vertex, "     s:", successors, "     unvisited: ", unvisited, "         stack: ", stack, "visited: ", visited)
                        if s not in stack and s not in unvisited:
                            visited.append(s)
                            stack.pop()
                        elif s not in stack and s not in visited:
                            unvisited.remove(s)
                            stack.append(s)
                        elif s in stack:
                            return True

            # after stepping through every vertex of the graph and not detecting any cycle, return False
            return False


    def dijkstra(self, src: int) -> []:
        """
        Returns the length of the shortest path for a given vertex
        """
        # initialize hashtable and priority queue
        visited = dict()
        queue = list()

        # initialize priority queue with src vertex
        heapq.heappush(queue, (0, src))

        # implementation of Dijkstra's algorithm (provided by module exploration)
        while len(queue) != 0:
            tuple = heapq.heappop(queue)
            vertex = tuple[1]
            distance = tuple[0]

            if vertex not in visited.keys():
                visited[vertex] = distance
                for j in range(len(self.adj_matrix[vertex])):
                    if self.adj_matrix[vertex][j] != 0:
                        successor = j
                        sub_distance = self.adj_matrix[vertex][successor]
                        heapq.heappush(queue, ((distance + sub_distance), successor))

        # initializes solution array with float('inf') for each element
        solution = [float("inf") for vertex in self.get_vertices()]

        # replaces each element of solution that has been visited with the min distance from src
        for key in visited.keys():
            solution[key] = visited[key]

        return solution