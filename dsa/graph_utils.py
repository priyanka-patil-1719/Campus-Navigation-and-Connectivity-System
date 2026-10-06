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
    """Keep campus landmarks fixed and extend the map for custom locations."""
    sample = json.loads(SAMPLE_PATH.read_text(encoding="utf-8"))
    positions = {node["name"]: node for node in sample["nodes"]}
    nodes = []
    custom_index = 0
    custom_top = 620 if any(name in positions for name in graph.vertices) else 85
    for index, name in enumerate(graph.vertices):
        if name in positions:
            node = dict(positions[name])
        else:
            node = {"name": name, "x": 115 + (custom_index % 4) * 220,
                    "y": custom_top + (custom_index // 4) * 140, "icon": "building"}
            custom_index += 1
        node["number"] = index + 1
        nodes.append(node)
    height = max(540, max((node["y"] for node in nodes), default=0) + 85)
    return {"nodes": nodes, "edges": graph.edges(), "directed": graph.directed,
            "weighted": graph.weighted, "width": 900, "height": height}
