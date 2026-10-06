# Routes

All graph forms use POST; no GET endpoint changes the graph. Successful graph edits and validation failures both redirect to the explorer with an appropriate flash message. Traversal routes render results directly.

| Method | Path | Fields / behavior |
| --- | --- | --- |
| GET | `/` | Overview, counts, campus drawing. |
| GET | `/graph` | Graph configuration, editor, drawing and inventory. |
| POST | `/graph/add-node` | `name`: normalized unique location name. |
| POST | `/graph/add-edge` | `source`, `target`, `weight` (required only when weighted). |
| POST | `/graph/remove-node` | `name`: remove location and incident edges. |
| POST | `/graph/remove-edge` | `source`, `target`: remove connection. |
| POST | `/graph/configure` | `direction`: `directed`/`undirected`; `weight_mode`: `weighted`/`unweighted`. |
| POST | `/graph/sample` | Replace campus with the sample, preserving modes. |
| POST | `/graph/reset` | Restore original undirected, unweighted sample. |
| POST | `/graph/clear` | Empty graph, preserving modes. |
| GET | `/traversal` | Starting-location selection and algorithm controls. |
| POST | `/traversal/bfs` | `start`: execute Python BFS. |
| POST | `/traversal/dfs` | `start`: execute Python DFS. |
| GET | `/representation` | Python-generated adjacency list and matrix. |
| GET | `/about` | Concise academic explanations and demo guide. |

The graph mutation dispatcher is one short route with explicit supported actions. Unrecognized actions return 404. DSA validation raises `ValueError`, which the route converts to a friendly notification. The template context receives a `Graph`, its vertices/edges and visualization data. Traversal results use Jinja `tojson` for safe playback data.
