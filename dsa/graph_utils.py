"""Load the fictional campus and prepare graph data for presentation."""

import json
from pathlib import Path

from .graph import Graph

SAMPLE_PATH = Path(__file__).resolve().parent.parent / "data" / "sample_graph.json"


def load_sample(directed=False, weighted=False):
    data = json.loads(SAMPLE_PATH.read_text(encoding="utf-8"))
    graph = Graph(directed, weighted)
    for node in data["nodes"]:
        graph.add_vertex(node["name"])
    for edge in data["edges"]:
        graph.add_edge(*edge)
    return graph


def visualization_data(graph):
    """A fixed campus layout; custom campuses use a predictable four-column grid."""
    sample = json.loads(SAMPLE_PATH.read_text(encoding="utf-8"))
    positions = {node["name"]: node for node in sample["nodes"]}
    use_campus_layout = all(name in positions for name in graph.vertices)
    nodes = []
    for index, name in enumerate(graph.vertices):
        if use_campus_layout:
            node = dict(positions[name])
        else:
            node = {"name": name, "x": 115 + (index % 4) * 220,
                    "y": 85 + (index // 4) * 140, "icon": "building"}
        node["number"] = index + 1
        nodes.append(node)
    height = 540 if use_campus_layout else max(420, ((len(nodes) + 3) // 4) * 140 + 30)
    return {"nodes": nodes, "edges": graph.edges(), "directed": graph.directed,
            "weighted": graph.weighted, "width": 900, "height": height}
