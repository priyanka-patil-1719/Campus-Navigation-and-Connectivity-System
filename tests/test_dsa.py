import unittest

from dsa import Graph, bfs, dfs
from dsa.graph_utils import load_sample, visualization_data


class GraphTests(unittest.TestCase):
    def make_graph(self, directed=False, weighted=False):
        graph = Graph(directed, weighted)
        for name in ("Gate", "Library", "Canteen", "Hostel", "Isolated"):
            graph.add_vertex(name)
        for source, target, weight in [("Gate", "Library", 150), ("Gate", "Canteen", 100),
                                       ("Library", "Hostel", 75), ("Canteen", "Hostel", 50)]:
            graph.add_edge(source, target, weight)
        return graph

    def test_all_four_graph_modes(self):
        for directed in (False, True):
            for weighted in (False, True):
                with self.subTest(directed=directed, weighted=weighted):
                    graph = self.make_graph(directed, weighted)
                    self.assertEqual(len(graph.edges()), 4)
                    matrix = graph.get_adjacency_matrix()["rows"]
                    self.assertEqual(matrix[0][1], 150 if weighted else 1)
                    self.assertEqual(matrix[1][0], 0 if directed else (150 if weighted else 1))
                    self.assertEqual(matrix[4], [0] * 5)
                    self.assertEqual(graph.get_adjacency_list()["Gate"][0],
                                     {"name": "Library", "weight": 150 if weighted else 1})

    def test_vertex_validation_and_normalization(self):
        graph = Graph()
        self.assertEqual(graph.add_vertex("  Main   Gate "), "Main Gate")
        for value in ("", "   ", "main gate", "a" * 41):
            with self.subTest(value=value), self.assertRaises(ValueError):
                graph.add_vertex(value)
        self.assertEqual(graph.vertices, ["Main Gate"])

    def test_vertex_limit(self):
        graph = Graph()
        for index in range(24):
            graph.add_vertex(str(index))
        with self.assertRaises(ValueError):
            graph.add_vertex("one too many")

    def test_invalid_edges_leave_graph_unchanged(self):
        graph = self.make_graph(weighted=True)
        before = graph.edges()
        for source, target, weight in [("Gate", "missing", 1), ("Gate", "Gate", 1),
                                      ("Gate", "Library", 1), ("Library", "Gate", 1)]:
            with self.assertRaises(ValueError):
                graph.add_edge(source, target, weight)
        for weight in ("", "abc", "nan", "inf", "-inf", -1, 0, 0.001, 100001, None):
            with self.subTest(weight=weight), self.assertRaises(ValueError):
                graph.add_edge("Gate", "Isolated", weight)
        self.assertEqual(graph.edges(), before)

    def test_fractional_weights_and_unweighted_input(self):
        graph = self.make_graph(weighted=True)
        graph.add_edge("Gate", "Isolated", "10.25")
        self.assertEqual(graph.get_adjacency_matrix()["rows"][0][4], 10.25)
        plain = self.make_graph()
        plain.add_edge("Gate", "Isolated", "ignored")
        self.assertEqual(plain.get_adjacency_matrix()["rows"][0][4], 1)

    def test_remove_location_removes_incoming_and_outgoing_edges(self):
        for directed in (False, True):
            graph = self.make_graph(directed)
            graph.remove_vertex("Library")
            self.assertFalse(graph.has_vertex("Library"))
            self.assertNotIn("Library", graph.neighbors("Gate"))
            self.assertEqual(len(graph.edges()), 2)

    def test_remove_edge_in_both_modes(self):
        for directed in (False, True):
            graph = self.make_graph(directed)
            graph.remove_edge("Gate", "Library")
            self.assertNotIn("Library", graph.neighbors("Gate"))
            self.assertNotIn("Gate", graph.neighbors("Library"))
            with self.assertRaises(ValueError):
                graph.remove_edge("Gate", "Library")

    def test_reconfiguration_preserves_arcs_and_merges_weights(self):
        graph = Graph(directed=True, weighted=True)
        graph.add_vertex("A")
        graph.add_vertex("B")
        graph.add_edge("A", "B", 8)
        graph.add_edge("B", "A", 3)
        undirected = graph.reconfigure(False, True)
        self.assertEqual(undirected.get_adjacency_matrix()["rows"], [[0, 3], [3, 0]])
        directed = undirected.reconfigure(True, True)
        self.assertEqual(len(directed.edges()), 2)
        plain = directed.reconfigure(True, False)
        self.assertEqual(plain.get_adjacency_matrix()["rows"], [[0, 1], [1, 0]])
        self.assertEqual(plain.reconfigure(False, True).edges()[0]["weight"], 1)
        self.assertEqual(graph.edges()[0]["weight"], 8)

    def test_bfs_order_queue_and_unreachable(self):
        result = bfs(self.make_graph(), "Gate")
        self.assertEqual(result["order"], ["Gate", "Library", "Canteen", "Hostel"])
        self.assertEqual(result["unreachable"], ["Isolated"])
        self.assertEqual(result["steps"][0]["frontier"], ["Library", "Canteen"])
        self.assertEqual(result["steps"][1]["frontier"], ["Canteen", "Hostel"])
        self.assertEqual(result["steps"][-1]["frontier"], [])
        self.assertEqual(result["steps"][-1]["depth"], 2)

    def test_dfs_order_stack_and_backtracking(self):
        result = dfs(self.make_graph(), "Gate")
        self.assertEqual(result["order"], ["Gate", "Library", "Hostel", "Canteen"])
        self.assertEqual(result["steps"][2]["frontier"], ["Gate", "Library", "Hostel"])
        self.assertEqual(result["unreachable"], ["Isolated"])
        directed = dfs(self.make_graph(directed=True), "Gate")
        self.assertEqual(directed["steps"][-1]["frontier"], ["Gate", "Canteen"])

    def test_traversals_obey_direction_and_ignore_weights(self):
        for algorithm in (bfs, dfs):
            graph = self.make_graph(directed=True, weighted=True)
            self.assertEqual(algorithm(graph, "Hostel")["order"], ["Hostel"])
            self.assertEqual(algorithm(graph, "Gate")["order"],
                             algorithm(graph.reconfigure(True, False), "Gate")["order"])

    def test_invalid_start_and_empty_graph(self):
        for algorithm in (bfs, dfs):
            with self.assertRaises(ValueError):
                algorithm(Graph(), "Gate")
            with self.assertRaises(ValueError):
                algorithm(self.make_graph(), "missing")

    def test_single_vertex(self):
        graph = Graph()
        graph.add_vertex("Gate")
        for algorithm in (bfs, dfs):
            result = algorithm(graph, "Gate")
            self.assertEqual(result["order"], ["Gate"])
            self.assertEqual(result["unreachable"], [])
        self.assertEqual(graph.get_adjacency_matrix()["rows"], [[0]])

    def test_representations_and_steps_do_not_mutate_graph(self):
        graph = self.make_graph()
        before = graph.edges()
        graph.get_adjacency_list()["Gate"].clear()
        graph.get_adjacency_matrix()["rows"][0][1] = 99
        bfs(graph, "Gate")
        dfs(graph, "Gate")
        self.assertEqual(graph.edges(), before)

    def test_sample_and_custom_layouts(self):
        for directed in (False, True):
            for weighted in (False, True):
                graph = load_sample(directed, weighted)
                self.assertEqual(len(graph.vertices), 10)
                self.assertEqual(len(graph.edges()), 14)
                self.assertEqual(len(bfs(graph, "Main Gate")["order"]), 10)
        graph.add_vertex("Seminar Hall")
        data = visualization_data(graph)
        self.assertEqual(len(data["nodes"]), 11)
        self.assertEqual(len({(n["x"], n["y"]) for n in data["nodes"]}), 11)
        self.assertTrue(all(0 < n["y"] < data["height"] for n in data["nodes"]))
        gate = next(node for node in data["nodes"] if node["name"] == "Main Gate")
        self.assertEqual((gate["x"], gate["y"], gate["icon"]), (100, 265, "gate"))
        self.assertGreater(data["nodes"][-1]["y"], 540)


if __name__ == "__main__":
    unittest.main()
