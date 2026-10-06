# Verification record

Verified locally on 6 October 2026 with Python 3.10.4, Flask 3.1.2 and headless Microsoft Edge through agent-browser.

## Automated Python checks

`python -m unittest discover -s tests -v`: **25 tests passed** after the final functional changes. Coverage includes four graph modes, mutation validation, finite positive weights, cyclic and disconnected traversal, BFS queue order, DFS backtracking, stable campus positions, adjacency representations, escaped labels, page rendering, and the actual form URLs generated for both traversal buttons.

`git diff --check`: passed.

## Browser checks

- Desktop viewport: 1440 × 1100.
- Phone viewport: 390 × 844.
- Tablet viewport: 768 × 1024.
- All five pages rendered; phone and tablet checks found no page-wide horizontal overflow.
- Adding a location and weighted connection updated the SVG and both adjacency representations.
- Graph configuration showed both directed arcs when converting an undirected graph; loading the directed sample showed its 14 original one-way connections and meter weights.
- Clicking a map location selected the starting vertex.
- The rendered BFS/DFS buttons submitted successfully and returned Python-generated results.
- Next step, play, pause, restart, complete/replay state, node colors, queue snapshots and recursion-stack snapshots worked.
- Unreachable vertices were reported.
- The mobile menu expanded and navigated; the campus map scrolled within its container.
- Clear produced useful empty states, disabled traversal on an empty graph, and Reset restored the original sample.
- Browser JavaScript errors: none detected. Browser console messages: none detected in the completed run.

Desktop and mobile screenshots and the local browser QA helper are in the ignored `artifacts/` folder. That helper is a development aid, not a runtime dependency of the Flask application.

## Scope

This verifies local functionality and Edge rendering at the listed sizes. A hosted Render deployment, Linux Gunicorn process, and other browser engines were not exercised. Deployment configuration and instructions are included; no service was published. The graph remains intentionally shared and in-memory.
