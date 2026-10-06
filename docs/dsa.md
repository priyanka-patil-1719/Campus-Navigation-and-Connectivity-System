# DSA implementation guide

All data structures and algorithms live here. Open these files during evaluation.

## `dsa/__init__.py`

Exports `Graph`, `bfs`, and `dfs` for readable imports. It contains no additional algorithm.

## `dsa/graph.py`

`Graph.adjacency` is a manually managed dictionary of neighbor dictionaries:

```python
{
    "Main Gate": {"Library": 150, "Parking": 80},
    "Library": {"Main Gate": 150},
    "Parking": {"Main Gate": 80},
}
```

The outer keys are vertices. Inner keys are neighbors; values are weights. In unweighted mode the values are always 1. Python dictionary insertion order determines traversal tie-breaking.

| Method | Purpose |
| --- | --- |
| `vertices` | Return the ordered location names. |
| `has_vertex`, `require_vertex` | Check existence or raise a readable validation error. |
| `add_vertex` | Normalize and validate a name, then insert an empty neighbor dictionary. |
| `add_edge` | Validate endpoints/weight; store one directed arc or both undirected directions. |
| `remove_vertex` | Remove the vertex and every incoming edge. |
| `remove_edge` | Remove one directed arc or both undirected directions. |
| `neighbors` | Return neighbors in insertion order. |
| `edges` | Export paths, counting each undirected edge only once. |
| `reconfigure` | Return a new graph with the chosen direction and weight modes. |
| `get_adjacency_list` | Export each vertex with its neighbor names and weights. |
| `get_adjacency_matrix` | Export an ordered vertex key and a V × V matrix. |

The matrix looks up each `(source, target)` pair. A missing edge is 0. An unweighted edge is 1; a weighted edge contains its positive distance. Directed matrices can be asymmetric. Undirected matrices are symmetric. Self-loops are excluded, so the diagonal remains zero.

Reconfiguration preserves connectivity: undirected → directed retains both arcs; directed → undirected merges reciprocal arcs and takes their minimum weight. Switching weights off replaces values with 1. Switching them on again cannot recover discarded distances; existing values remain 1 m. Loading the weighted sample restores its fictional distances.

## `dsa/bfs.py`

Breadth First Search uses a FIFO `collections.deque`.

1. Mark the start discovered and enqueue it.
2. Remove the front vertex and append it to the visit order.
3. For each undiscovered neighbor, mark it immediately and enqueue it.
4. Record a teaching snapshot and continue until the queue is empty.

Marking on enqueue prevents multiple copies of a vertex in the queue when the graph has cycles. The first visit reaches each vertex at its fewest-edge level from the start. Edge weights do not affect BFS.

Each snapshot includes the current vertex, processed visit order, pending queue **after scanning the current neighbors**, discovery-tree edges and level.

## `dsa/dfs.py`

Depth First Search uses a recursive `visit` function and a visited set.

1. Mark the current vertex visited and append it to the visit order.
2. Push it onto the teaching call stack and record a snapshot.
3. Recursively visit each unvisited neighbor in order.
4. Pop the current call when its branch finishes, backtracking to its caller.

The visited set prevents infinite recursion on cyclic graphs. The graph is limited to 24 vertices, well below typical Python recursion limits. A snapshot represents **entry into a vertex**, not every return from a recursive call. The last snapshot therefore still displays the calls active at the last visit; actual recursive calls subsequently return. Depth is the current call-stack length minus one.

## Traversal result contract

Both algorithms return:

```python
{
    "algorithm": "BFS",  # or DFS
    "start": "Main Gate",
    "order": [...],
    "visited": [...],
    "unreachable": [...],
    "steps": [
        {"current": "Main Gate", "visited": [...], "frontier": [...],
         "tree_edges": [["Main Gate", "Library"]], "depth": 0}
    ],
}
```

An invalid starting vertex raises `ValueError`. A one-vertex graph visits that vertex once. A disconnected graph visits only vertices reachable from the start, respecting edge direction. The graph itself is never modified by a traversal.

## `dsa/graph_utils.py`

`load_sample()` constructs a real `Graph` using `data/sample_graph.json`. It calls the same vertex/edge methods as user edits. In directed mode, sample connections follow the direction written in JSON.

`visualization_data()` exports nodes, edges and mode flags. Sample locations keep their fixed fictional drawing positions and campus icons. Custom locations extend the map below them in predictable four-column rows; on an entirely custom campus, those rows start at the top. The map height grows as needed. The renderer bends paths around buildings that would otherwise lie on a straight connection. The coordinates describe a diagram, not geography. No layout physics or graph package is used.

## Complexity

| Operation | Time | Space |
| --- | --- | --- |
| Adjacency list export | O(V + E) | O(V + E) |
| Adjacency matrix export | O(V²) | O(V²) |
| Core BFS / DFS | O(V + E) | O(V) auxiliary |
| Add edge | O(1) expected | O(1) |
| Add vertex with case-insensitive duplicate scan | O(V) | O(1) |
| Remove vertex | O(V) expected dictionary operations | O(1) auxiliary |
| Reconfigure modes | O(V² + E), including name validation | O(V + E) |

`E` counts logical edges; undirected storage contains two entries per edge. This changes a constant factor only. **Teaching snapshots add overhead:** copying visit lists, queues/stacks and tree edges at each visit takes O(V²) time and storage in the worst case, on top of core O(V + E) traversal. Tree edges are at most V − 1. The UI's complexity labels describe the core traversal, not trace recording or animation. The 24-vertex cap keeps this educational tradeoff small.
