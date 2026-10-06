"""Thin routes: validate forms, call the DSA layer, render templates."""

from flask import Blueprint, current_app, flash, g, redirect, render_template, request, url_for

from dsa import Graph, bfs, dfs
from dsa.graph_utils import load_sample, visualization_data

pages = Blueprint("pages", __name__)


@pages.before_request
def acquire_graph():
    # A single shared classroom graph. Protect it during threaded local requests.
    current_app.extensions["graph_lock"].acquire()
    g.graph_locked = True


@pages.teardown_request
def release_graph(error=None):
    if g.pop("graph_locked", False):
        current_app.extensions["graph_lock"].release()


def graph():
    return current_app.extensions["campus_graph"]


def show(template, **context):
    campus = graph()
    return render_template(template, graph=campus, vertices=campus.vertices,
                           edges=campus.edges(), graph_data=visualization_data(campus),
                           **context)


@pages.get("/")
def index():
    return show("index.html", active="dashboard", title="Campus overview")


@pages.get("/graph")
def explorer():
    return show("graph.html", active="graph", title="Graph explorer")


@pages.post("/graph/<action>")
def change_graph(action):
    campus = graph()
    try:
        if action == "add-node":
            name = campus.add_vertex(request.form.get("name", ""))
            message = f"{name} added to the campus."
        elif action == "add-edge":
            campus.add_edge(request.form.get("source", ""), request.form.get("target", ""),
                            request.form.get("weight", ""))
            message = "Connection added. Your campus graph is updated."
        elif action == "remove-node":
            campus.remove_vertex(request.form.get("name", ""))
            message = "Location and its connections removed."
        elif action == "remove-edge":
            campus.remove_edge(request.form.get("source", ""), request.form.get("target", ""))
            message = "Connection removed."
        elif action == "configure":
            direction = request.form.get("direction")
            weight_mode = request.form.get("weight_mode")
            if direction not in ("directed", "undirected") or weight_mode not in ("weighted", "unweighted"):
                raise ValueError("Choose a valid graph type and weight mode.")
            current_app.extensions["campus_graph"] = campus.reconfigure(
                direction == "directed", weight_mode == "weighted")
            message = "Graph settings applied."
        elif action == "sample":
            current_app.extensions["campus_graph"] = load_sample(campus.directed, campus.weighted)
            message = "Sample campus loaded with your current graph settings."
        elif action == "reset":
            current_app.extensions["campus_graph"] = load_sample()
            message = "Campus reset to the original undirected, unweighted sample."
        elif action == "clear":
            current_app.extensions["campus_graph"] = Graph(campus.directed, campus.weighted)
            message = "Graph cleared. Add a location to begin."
        else:
            from flask import abort
            abort(404)
        flash(message, "success")
    except ValueError as error:
        flash(str(error), "error")
    return redirect(url_for("pages.explorer"))


@pages.route("/traversal", methods=["GET"])
@pages.route("/traversal/<algorithm>", methods=["POST"], endpoint="run_traversal")
def traversal(algorithm=None):
    result = None
    start = request.form.get("start", "")
    if request.method == "POST":
        try:
            if not graph().vertices:
                raise ValueError("Add a location before running a traversal.")
            if algorithm not in ("bfs", "dfs"):
                raise ValueError("Choose BFS or DFS.")
            result = {"bfs": bfs, "dfs": dfs}[algorithm](graph(), start)
        except ValueError as error:
            flash(str(error), "error")
    return show("traversal.html", active="traversal", title="Traversal studio",
                result=result, selected_start=start)


@pages.get("/representation")
def representation():
    return show("representation.html", active="representation", title="Graph representations",
                adjacency=graph().get_adjacency_list(), matrix=graph().get_adjacency_matrix())


@pages.get("/about")
def about():
    return show("about.html", active="about", title="The concepts behind the campus")
