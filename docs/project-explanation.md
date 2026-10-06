# Explaining the project in 5–10 minutes

## Objective

“This project demonstrates graph data structures using a fictional campus. Locations are vertices, paths are edges, and BFS and DFS let us compare two ways of exploring connectivity.”

## 1. Introduce the campus (1 minute)

Open Overview. Identify Main Gate, Library, Canteen and the other buildings. Explain the live location and connection counts. The campus is a schematic: it does not use GPS or real map coordinates.

## 2. Build and configure the graph (2 minutes)

Open Graph Explorer. Show undirected paths, then select Directed and Weighted and click Apply settings. Explain that existing two-way paths become two arrows. Load sample campus to display the explicitly directed sample and its fictional meter distances.

Add `Seminar Hall`. Connect `Library → Seminar Hall` with weight `100`. Point out the extra vertex and edge. Try adding the same location again to demonstrate validation. The fixed custom layout keeps node placement repeatable.

## 3. Show graph representations (1 minute)

Open Representations. Find Library in the adjacency list and point to Seminar Hall. Find the corresponding row/column intersection in the matrix. Explain that zero means no edge, and that a directed matrix can be asymmetric. Switch to undirected to show symmetry if time permits.

## 4. Demonstrate BFS (1–2 minutes)

Open Traversal, choose Main Gate, and run BFS. Pause and use Next step. Describe the queue as first-in, first-out. Each snapshot shows the queue after the current vertex's neighbors are considered. Newly discovered vertices join the back; nearer levels are visited first. The orange vertex is current and green vertices have been visited.

## 5. Compare DFS (1–2 minutes)

Run DFS from the same start. Follow its recursion stack: each recursive call explores a branch before the algorithm backtracks. Snapshots occur on entry to a vertex. Compare the final order with BFS. Both are deterministic because neighbors are considered in insertion order.

Optionally add a disconnected vertex and run again to show that only reachable locations are visited. In a directed graph, reachability depends on arrow direction.

## 6. Open the code (1–2 minutes)

Open `dsa/graph.py` to show the adjacency dictionary, `add_edge`, and the matrix method. Open `dsa/bfs.py` and point to `deque`, `popleft`, and marking neighbors at enqueue time. Open `dsa/dfs.py` and show the recursive `visit` function and visited set.

Finally, show that Flask routes simply call these functions. JavaScript only draws and animates the results returned by Python.

## Likely viva questions

| Question | Answer |
| --- | --- |
| Why an adjacency list? | It naturally stores each location's neighbors and supports traversal in O(V + E). |
| Why also a matrix? | It demonstrates another representation and makes individual connection lookups and symmetry visible. |
| Why mark visited? | To avoid repeated work and infinite loops on cyclic graphs. |
| Queue versus stack? | BFS's queue explores levels; DFS's recursive call stack explores depth before returning. |
| Is BFS the shortest walking route? | BFS gives fewest-edge levels; it does not optimize weighted distances. DFS does not optimize distance either. |
| What if the graph is disconnected? | Only vertices reachable from the chosen start are visited; the others are listed. |
| Why can visit order differ? | Different start vertices or neighbor insertion orders can produce different valid traversal orders. |
| How is data saved? | It stays in process memory; all visitors share it and a restart restores the sample. |
| What is traversal complexity? | Core BFS/DFS is O(V + E) time and O(V) auxiliary space. This teaching version additionally copies step snapshots, which can use O(V²) time and space. |

Reset the graph before each demonstration so the opening state is predictable.
