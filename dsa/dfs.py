"""Depth-first search: recursively explore one branch before backtracking."""


def dfs(graph, start):
    graph.require_vertex(start)
    visited = set()
    order, steps, stack, tree_edges = [], [], [], []

    def visit(current):
        visited.add(current)
        order.append(current)
        stack.append(current)
        steps.append({
            "current": current, "visited": order.copy(),
            "frontier": stack.copy(), "tree_edges": tree_edges.copy(),
            "depth": len(stack) - 1,
        })
        for neighbor in graph.neighbors(current):
            if neighbor not in visited:
                tree_edges.append([current, neighbor])
                visit(neighbor)
        stack.pop()

    visit(start)
    return {"algorithm": "DFS", "start": start, "order": order,
            "steps": steps, "visited": order.copy(),
            "unreachable": [v for v in graph.vertices if v not in visited]}
