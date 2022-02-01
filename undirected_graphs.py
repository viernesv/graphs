class UndirectedGraph:
    """
    Class to implement undirected graph
    - duplicate edges not allowed
    - loops not allowed
    - no edge weights
    - vertex names are strings
    """

    def __init__(self, start_edges=None):
        """
        Store graph info as adjacency list
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.adj_list = dict()

        # populate graph with initial vertices and edges (if provided)
        # before using, implement add_vertex() and add_edge() methods
        if start_edges is not None:
            for u, v in start_edges:
                self.add_edge(u, v)

    def __str__(self):
        """
        Return content of the graph in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = [f'{v}: {self.adj_list[v]}' for v in self.adj_list]
        out = '\n  '.join(out)
        if len(out) < 70:
            out = out.replace('\n  ', ', ')
            return f'GRAPH: {{{out}}}'
        return f'GRAPH: {{\n  {out}}}'

    # ------------------------------------------------------------------ #

    def add_vertex(self, v: str) -> None:
        """
        Add new vertex to the graph
        """
        if v in self.adj_list.keys():
            return
        else:
            self.adj_list[v] = list()


    def add_edge(self, u: str, v: str) -> None:
        """
        Add edge to the graph
        """
        # returns if the vertices are equal
        if u == v:
            return
        else:
            # creates vertices only if they do not already exist in the graph
            if u not in self.adj_list.keys():
                self.add_vertex(u)
            if v not in self.adj_list.keys():
                self.add_vertex(v)

            # creates edge between vertices only if it does not already exist between them
            if v not in self.adj_list[u]:
                self.adj_list[u].append(v)
            if u not in self.adj_list[v]:
                self.adj_list[v].append(u)


    def remove_edge(self, v: str, u: str) -> None:
        """
        Remove edge from the graph
        """
        # returns if either vertex is not in the graph
        if u not in self.adj_list.keys() or v not in self.adj_list.keys():
            return

        # returns if the edge between the vertices does not exist
        if v not in self.adj_list[u] or u not in self.adj_list[v]:
            return

        else:
            self.adj_list[u].remove(v)
            self.adj_list[v].remove(u)


    def remove_vertex(self, v: str) -> None:
        """
        Remove vertex and all connected edges
        """
        # returns if the vertex is not in the graph
        if v not in self.adj_list.keys():
            return
        else:
            # remove all edges incident to the vertex
            for key in self.adj_list.keys():
                if v in self.adj_list[key]:
                    self.adj_list[key].remove(v)

            # remove the vertex from the graph
            del self.adj_list[v]


    def get_vertices(self) -> []:
        """
        Return list of vertices in the graph (any order)
        """
        keys = list()
        for v in self.adj_list.keys():
            keys.append(v)
        return keys


    def get_edges(self) -> []:
        """
        Return list of edges in the graph (any order)
        """
        all_edges = list()
        for vertex in self.adj_list.keys():
            for edge in self.adj_list[vertex]:

                # only appends the edge if it has not been previously appended
                if (vertex, edge) not in all_edges and (edge, vertex) not in all_edges:
                    all_edges.append((vertex, edge))

        return all_edges
        

    def is_valid_path(self, path: []) -> bool:
        """
        Return true if provided path is valid, False otherwise
        """
        if len(path) == 0:
            return True
        elif len(path) == 1:
            if path[0] in self.adj_list.keys():
                return True
            else:
                return False
        else:
            edges = self.get_edges()
            for i in range(len(path) - 1):
                if (path[i], path[i+1]) not in edges and (path[i+1], path[i]) not in edges:
                    return False
            return True


    def dfs(self, v_start, v_end=None) -> []:
        """
        Return list of vertices visited during DFS search
        Vertices are picked in alphabetical order
        """
        reachable = list()
        stack = list()

        if v_start not in self.adj_list.keys():
            return reachable
        else:
            stack.append(v_start)

            # implementation of DFS (provided by module exploration)
            while len(stack) != 0 and v_end not in reachable:
                vertex = stack.pop()
                if vertex not in reachable:
                    reachable.append(vertex)
                    self.adj_list[vertex].sort(reverse = True)      # sort in reverse lexicographical order
                    for successor in self.adj_list[vertex]:
                        stack.append(successor)
            return reachable


    def bfs(self, v_start, v_end=None) -> []:
        """
        Return list of vertices visited during BFS search
        Vertices are picked in alphabetical order
        """
        reachable = list()
        queue = list()

        if v_start not in self.adj_list.keys():
            return reachable
        else:
            queue.append(v_start)

            # implementation of BFS (provided by module exploration)
            while len(queue) != 0 and v_end not in reachable:
                vertex = queue.pop(0)
                if vertex not in reachable:
                    reachable.append(vertex)
                    self.adj_list[vertex].sort()        # sort in lexicographical order
                    for successor in self.adj_list[vertex]:
                        queue.append(successor)
            return reachable


    def count_connected_components(self):
        """
        Return number of connected components in the graph
        """
        vertices = self.get_vertices()      # list of all vertices in graph
        visited = self.bfs(vertices[0])     # initialize list of visited vertices
        count = 1                           # count number of connected components

        # loops through each unvisited vertex of the graph and performs DFS initialized with that vertex
        # counts how many DFSs occur, which represents the number of connected components in the graph
        for i in range(len(vertices)):
            if vertices[i] not in visited:
                count += 1
                for element in self.bfs(vertices[i]):
                    visited.append(element)
        return count


    def has_cycle(self):
        """
        Return True if graph contains a cycle, False otherwise
        """
        visited = list()
        stack = list()

        # steps through each vertex and performs a DFS to detect possible cycles originating at that vertex
        for i in range(len(self.get_vertices())):
            v_start = self.get_vertices()[i]    # initialize DFS with the first vertex of the graph
            stack.append(v_start)

            # modified implementation of DFS
            while len(stack) != 0:
                vertex = stack.pop()
                if vertex not in visited:
                    visited.append(vertex)

                    # for each successor of the vertex, checks if successor is in the stack; if it is not, append it.
                    # if the successor is already in the stack, it means a path has been found that leads back to it;
                    # hence, a cycle is detected
                    for successor in self.adj_list[vertex]:
                        if successor not in stack:
                            stack.append(successor)
                        elif successor in stack:
                            return True

        # after stepping through every vertex of the graph and not detecting any cycle, return False
        return False
       
