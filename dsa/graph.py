"""A small adjacency-list graph, implemented without graph libraries."""

from math import isfinite


class Graph:
    MAX_VERTICES = 24

    def __init__(self, directed=False, weighted=False):
        self.directed = directed
        self.weighted = weighted
        # Dictionaries preserve insertion order, making demonstrations repeatable.
        self.adjacency = {}

    @property
    def vertices(self):
        return list(self.adjacency)

    def has_vertex(self, name):
        return name in self.adjacency

    def add_vertex(self, name):
        name = " ".join(name.split())
        if not name:
            raise ValueError("Please enter a location name.")
        if len(name) > 40:
            raise ValueError("Keep location names to 40 characters or fewer.")
        if any(name.casefold() == existing.casefold() for existing in self.adjacency):
            raise ValueError("That location already exists.")
        if len(self.adjacency) >= self.MAX_VERTICES:
            raise ValueError("This demonstration supports up to 24 locations.")
        self.adjacency[name] = {}
        return name

    def require_vertex(self, name):
        if not self.has_vertex(name):
            raise ValueError("Please select a location that exists in the graph.")

    def add_edge(self, source, target, weight=1):
        self.require_vertex(source)
        self.require_vertex(target)
        if source == target:
            raise ValueError("Choose two different locations to connect.")
        if target in self.adjacency[source]:
            raise ValueError("These locations already have that connection.")
        if self.weighted:
            try:
                weight = float(weight)
            except (TypeError, ValueError):
                raise ValueError("Enter a numeric distance in meters.") from None
            if not isfinite(weight) or not 0 < weight <= 100000:
                raise ValueError("Distance must be greater than 0 and at most 100,000 meters.")
            weight = round(weight, 2)
            if weight == 0:
                raise ValueError("The smallest distance is 0.01 meters.")
            if weight.is_integer():
                weight = int(weight)
        else:
            weight = 1
        self.adjacency[source][target] = weight
        if not self.directed:
            self.adjacency[target][source] = weight

    def remove_vertex(self, name):
        self.require_vertex(name)
        del self.adjacency[name]
        for neighbors in self.adjacency.values():
            neighbors.pop(name, None)

    def remove_edge(self, source, target):
        self.require_vertex(source)
        self.require_vertex(target)
        if target not in self.adjacency[source]:
            raise ValueError("That connection does not exist.")
        del self.adjacency[source][target]
        if not self.directed:
            del self.adjacency[target][source]

    def neighbors(self, name):
        self.require_vertex(name)
        return list(self.adjacency[name])

    def edges(self):
        result, seen = [], set()
        for source, neighbors in self.adjacency.items():
            for target, weight in neighbors.items():
                if self.directed or (target, source) not in seen:
                    result.append({"source": source, "target": target, "weight": weight})
                seen.add((source, target))
        return result

    def get_adjacency_list(self):
        return {
            vertex: [{"name": name, "weight": weight} for name, weight in neighbors.items()]
            for vertex, neighbors in self.adjacency.items()
        }

    def get_adjacency_matrix(self):
        vertices = self.vertices
        return {"vertices": vertices, "rows": [
            [self.adjacency[source].get(target, 0) for target in vertices]
            for source in vertices
        ]}

    def reconfigure(self, directed, weighted):
        """Keep existing arcs. Merge reciprocal arcs using the smaller weight.

        An undirected edge becomes two directed arcs. When adding weights to an
        unweighted graph, every existing connection starts at 1 meter.
        """
        updated = Graph(directed, weighted)
        for vertex in self.vertices:
            updated.add_vertex(vertex)
        for source, neighbors in self.adjacency.items():
            for target, weight in neighbors.items():
                value = weight if weighted else 1
                if target in updated.adjacency[source]:
                    value = min(value, updated.adjacency[source][target])
                updated.adjacency[source][target] = value
                if not directed:
                    updated.adjacency[target][source] = value
        return updated
