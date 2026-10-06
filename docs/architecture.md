# Architecture

```text
Browser form (HTML)
        ↓ POST
Flask route (routes/graph_routes.py)
        ↓ method/function call
Python DSA layer (/dsa)
        ↓ graph / representation / traversal snapshots
Jinja template → HTML + safely serialized JSON
        ↓
CSS presentation + JavaScript SVG drawing/playback
```

## Responsibilities

- `app.py` creates Flask, loads the sample, registers the blueprint, and configures error pages. It contains no graph algorithm.
- `routes/graph_routes.py` reads forms, delegates operations to `/dsa`, flashes validation errors, and renders or redirects.
- `/dsa` owns vertices, edges, neighbor relationships, graph modes, adjacency representations, BFS, DFS, and sample loading. It has no Flask dependency and can run independently.
- `/templates` contains five pages with Jinja inheritance and shared navigation, notifications, icons and map shell.
- `/static/css` owns the light Bento Grid design and responsive layouts.
- `/static/js/graph.js` creates SVG elements from Python data and colors them using Python step snapshots. Path clipping, label wrapping and reciprocal arrow offsets are drawing geometry, not traversal algorithms.
- `/static/js/ui.js` handles the mobile menu, dismissible notifications and destructive-action confirmations.

## State

Each Flask application holds one `Graph` in `app.extensions`. A reentrant lock protects page snapshots and mutations during threaded requests. It is released during request teardown, including errors. Graph state is shared among all visitors to that process. It is intentionally not stored in a cookie, database, or file. The only session use is Flask flash messages, signed with a generated process secret.

Gunicorn uses one worker and four threads. Multiple workers or instances would create independent graphs and are unsupported. Restarting the process restores the sample and changes the temporary session secret.

## Request flow

Graph edits use ordinary POST forms followed by redirects, so refreshing the result does not repeat the edit. Traversal POSTs render a result page directly; they do not mutate the graph. Page requests always read the current graph. An already-open page is a snapshot; refresh it after changes in another tab. No fetch API, external network service, or frontend framework is required.

## Rendering and validation

Server-side validation is authoritative. Jinja autoescaping protects labels in HTML; `tojson` safely embeds data in script elements. The renderer uses DOM `textContent` rather than injecting user HTML. Empty graphs and invalid form values receive visible messages. The Flask debugger is off. The app is a small shared academic demo, not an authenticated multi-user navigation service.
