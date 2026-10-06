"""Breadth-first search: mark on enqueue, then explore with a FIFO queue."""

from collections import deque


def bfs(graph, start):
    graph.require_vertex(start)
    queue = deque([start])
    discovered = {start}
    order, steps, tree_edges = [], [], []
    depths = {start: 0}

    while queue:
        current = queue.popleft()
        order.append(current)
        for neighbor in graph.neighbors(current):
            if neighbor not in discovered:
                discovered.add(neighbor)
                depths[neighbor] = depths[current] + 1
                queue.append(neighbor)
                tree_edges.append([current, neighbor])
        steps.append({
            "current": current, "visited": order.copy(),
            "frontier": list(queue), "tree_edges": tree_edges.copy(),
            "depth": depths[current],
        })

    return {"algorithm": "BFS", "start": start, "order": order,
            "steps": steps, "visited": order.copy(),
            "unreachable": [v for v in graph.vertices if v not in discovered]}
