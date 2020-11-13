class Vertex:

    def __init__(self, supply1=0, supply2=0):
        self.supply1 = supply1
        self.supply2 = supply2

    def __repr__(self):
        return f'<supply1={self.supply1}, supply2={self.supply2}>'


class DirectedEdge:

    def __init__(self, capacity, capacity1=0, capacity2=0, cost=0):
        self.capacity = capacity
        self.capacity1 = capacity1
        self.capacity2 = capacity2
        self.cost = cost
        self.flow1 = 0
        self.flow2 = 0

    def __repr__(self):
        return (
            '<'
            f'cost {self.cost}; '
            f'flow1 ({self.flow1} / {self.capacity1}); '
            f'flow2 ({self.flow2} / {self.capacity2})'
            '>'
        )


class EdgeView:
    def __init__(self, G):
        self.G = G

    def __len__(self):
        return sum(len(self.G[v]) for v in self.G)

    def __iter__(self):
        for v in self.G:
            for w in self.G[v]:
                yield (v, w)

    def __contains__(self, e):
        return self.get(e) is not None

    def __getitem__(self, e):
        v, w = e
        if v not in self.G:
            return None
        return self.G[v].get(w, None)


class Graph:
    def __init__(self):
        self._adj = {}
        self._pred = {}
        self._vertices = {}

    def add_edge(self, v, w, capacity, capacity1=0, capacity2=0, cost=0):
        if v not in self._adj:
            self.add_vertex(v)
        if w not in self._adj:
            self.add_vertex(w)

        edge = DirectedEdge(capacity, capacity1, capacity2, cost)
        self._adj[v][w] = edge
        self._pred[w][v] = edge

    def add_vertex(self, name, supply1=0, supply2=0):
        self._adj[name] = {}
        self._pred[name] = {}
        self._vertices[name] = Vertex(supply1, supply2)

    @property
    def vertices(self):
        return self._vertices

    @property
    def edges(self):
        return EdgeView(self)

    @property
    def adj(self):
        return self._adj

    @property
    def in_edges(self):
        return self._pred

    @property
    def out_edges(self):
        return self._adj

    def __len__(self):
        return len(self.vertices)

    def __iter__(self):
        return iter(self.vertices)

    def __contain__(self, v):
        return v in self.vertices

    def __getitem__(self, v):
        return self.adj[v]
