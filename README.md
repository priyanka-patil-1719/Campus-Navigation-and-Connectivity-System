# Campus Navigation and Connectivity System

A self-contained college mini-project that turns a fictional campus into an editable graph. Explore its connections, inspect adjacency representations, and demonstrate Breadth First Search and Depth First Search step by step.

## Project overview

CampusNav combines a light campus-map interface with a compact Bento Grid layout. Blue controls guide navigation, green shows visited locations, and orange marks the current traversal vertex. The sample campus contains **10 locations and 14 connections**. These are graph data, not geographic coordinates or real campus distances.

## Features

- Overview with live vertex and edge counts and a campus diagram.
- Graph Explorer: add/remove locations and connections, change graph modes, clear, reset, or load the sample.
- All four combinations of directed/undirected and weighted/unweighted graphs.
- SVG paths, directional arrowheads, reciprocal arrow offsets, and weighted distance labels.
- Python-generated BFS/DFS results with play/pause, next step, replay, restart, and speed controls.
- Queue snapshots for BFS and recursion-stack snapshots for DFS, plus unreachable locations.
- Dynamic adjacency list and matrix, including weights and directed asymmetry.
- Responsive navigation, scrollable maps/tables, keyboard-selectable start locations, reduced-motion support, and accessible form labels.
- Friendly validation and useful empty states. All assets are local; no CDN or image service.

## DSA concepts used

Graph, vertices, edges, directed graph, undirected graph, weighted graph, adjacency list, adjacency matrix, BFS, DFS, reachability, FIFO queue, recursion, and backtracking.

## Technology stack

Python 3.10+, Flask, Jinja2, HTML5, CSS3, and vanilla JavaScript for SVG drawing and playback. Python's `collections.deque` provides the BFS queue. Gunicorn is the Linux deployment server. There is no database, frontend build step, Node.js dependency, graph library, external API, or authentication system.

## Project structure

```text
app.py                    Flask application factory and local entry point
gunicorn.conf.py          Single-process deployment configuration
requirements.txt          Flask and Linux Gunicorn dependencies
dsa/
  __init__.py             Public DSA imports
  graph.py                Manual graph, mutation, modes, list and matrix
  bfs.py                  Queue-based BFS and teaching steps
  dfs.py                  Recursive DFS and teaching steps
  graph_utils.py          Sample loading and deterministic drawing data
routes/
  graph_routes.py         Thin page and form handlers
data/sample_graph.json    Fictional campus locations, positions and paths
templates/                Five Jinja pages, shared layout and components
static/css/               Design, graph styling and responsive rules
static/js/                SVG renderer, Python-result player, small UI actions
docs/                     Setup, architecture, routes, DSA and demo guide
tests/                    Standard-library DSA and Flask integration tests
```

## How to run

Open a terminal in this project folder:

```powershell
python -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
python app.py
```

If PowerShell blocks activation, use the environment's interpreter directly:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe app.py
```

On macOS/Linux, activate with `source .venv/bin/activate`. No environment variables are needed for local use.

## Open in browser

<http://127.0.0.1:5000>

The sample loads automatically. JavaScript is used for the SVG and animation; forms, representations and the complete server-rendered traversal order still work without it.

## DSA folder

**Every graph operation and traversal implementation is in `/dsa`.** Flask calls this layer. Templates present its data. JavaScript draws the supplied nodes/edges and plays the supplied traversal snapshots; it never computes BFS, DFS, or adjacency representations. Read [the DSA guide](docs/dsa.md) for a file-by-file explanation.

## Graph behavior

- Names are trimmed, limited to 40 characters, and unique ignoring case. Maximum 24 locations keeps the demonstration manageable.
- Self-loops and duplicate edges are rejected. Opposite directed edges are distinct connections.
- Distances must be finite and positive (0.01–100,000 m, rounded to two decimals). Zero in the matrix always means no edge.
- Switching undirected → directed creates both directions for each existing path.
- Switching directed → undirected merges reciprocal paths using the smaller distance.
- Turning weights off discards distances; turning them back on initializes existing paths to 1 m.
- **Load sample** replaces the campus while keeping the selected modes; weighted samples receive the JSON distances. In directed samples, each JSON path is one-way as written.
- **Reset graph** restores the original undirected, unweighted sample. **Clear graph** removes all locations and edges but keeps the modes.
- BFS/DFS follow neighbor insertion order and visit only reachable locations. Weights do not influence their visit order. Neither algorithm here is a weighted shortest-route solver.

## Teacher demonstration

1. Open Overview and identify the vertex/edge counts.
2. Open Graph Explorer and explain a location as a vertex and a path as an edge.
3. Change to directed and weighted modes. Apply settings, then load the sample to see one-way paths and fictional distances.
4. Add `Seminar Hall` and connect `Library → Seminar Hall` with distance `100`.
5. Inspect the adjacency list and matrix. Point out directed asymmetry.
6. Run BFS from Main Gate. Pause and use Next step to explain the queue and levels.
7. Run DFS from Main Gate and compare its recursion stack and visit order.
8. Add an isolated vertex to demonstrate reachability.
9. Open `dsa/graph.py`, `dsa/bfs.py`, and `dsa/dfs.py` to explain the actual implementation.

See [the 5–10 minute presentation guide](docs/project-explanation.md).

## Tests

```powershell
python -m unittest discover -s tests -v
```

Tests cover graph modes, matrix/list values, cycles, deterministic traversal, backtracking, isolated/empty graphs, validation, safe rendering, and the full Flask editing flow.

## Deployment

Create a **Python web service** from this repository on Render. Use the project folder as the root directory if it is nested in a larger repository.

- Build command: `pip install -r requirements.txt`
- Start command: `gunicorn app:app`
- Instance type: Free, if available for your account.

`gunicorn.conf.py` binds to Render's `PORT` and uses **one worker**. Keep one instance and one worker because the graph lives in process memory. Gunicorn is skipped during Windows installation; run `python app.py` locally on Windows. These steps follow [Render's Flask deployment guide](https://render.com/docs/deploy-flask) and [Flask's Gunicorn guide](https://flask.palletsprojects.com/en/stable/deploying/gunicorn/).

## Intentional limitations

The app is a shared classroom demonstration: every visitor to one running process edits the **same graph**. A restart, redeploy, or hosting instance recycle restores the sample; edits are not persisted. Use one worker/instance and reset before presenting. There are no user accounts or private workspaces. The map is a deterministic schematic, and dense custom graphs can contain crossing paths. See [Render's free-service limitations](https://render.com/docs/free) for hosting behavior.

This project is prepared for deployment; creating these files does not deploy a live service.

## Documentation

[Setup](docs/setup.md) · [Architecture](docs/architecture.md) · [DSA implementation](docs/dsa.md) · [Routes](docs/routes.md) · [Project explanation](docs/project-explanation.md)
