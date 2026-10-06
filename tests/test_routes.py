import unittest
from html.parser import HTMLParser

from app import create_app


class RouteTests(unittest.TestCase):
    def setUp(self):
        self.app = create_app({"TESTING": True, "SECRET_KEY": "test-only"})
        self.client = self.app.test_client()

    @property
    def graph(self):
        return self.app.extensions["campus_graph"]

    def post(self, action, **data):
        return self.client.post("/graph/" + action, data=data, follow_redirects=True)

    def test_all_pages_and_local_assets(self):
        for path in ("/", "/graph", "/traversal", "/representation", "/about",
                     "/static/css/style.css", "/static/css/graph.css", "/static/css/responsive.css",
                     "/static/js/graph.js", "/static/js/ui.js", "/static/favicon.svg"):
            with self.subTest(path=path):
                with self.client.get(path) as response:
                    self.assertEqual(response.status_code, 200)
        self.assertEqual(self.client.get("/missing").status_code, 404)
        self.assertEqual(self.client.post("/graph/missing").status_code, 404)

    def test_full_edit_representation_traversal_flow(self):
        self.post("add-node", name="Seminar Hall")
        response = self.post("add-edge", source="Library", target="Seminar Hall")
        self.assertIn(b"Connection added", response.data)
        self.assertIn(b"Seminar Hall", self.client.get("/representation").data)
        for algorithm in ("bfs", "dfs"):
            response = self.client.post("/traversal/" + algorithm, data={"start": "Main Gate"})
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'id="traversal-data"', response.data)
            self.assertIn(b'Seminar Hall', response.data)
        self.post("remove-edge", source="Library", target="Seminar Hall")
        self.assertEqual(self.graph.neighbors("Seminar Hall"), [])
        self.post("remove-node", name="Seminar Hall")
        self.assertFalse(self.graph.has_vertex("Seminar Hall"))

    def test_configuration_sample_clear_and_reset(self):
        for direction in ("directed", "undirected"):
            for mode in ("weighted", "unweighted"):
                response = self.post("configure", direction=direction, weight_mode=mode)
                self.assertEqual(response.status_code, 200)
                self.assertEqual(self.graph.directed, direction == "directed")
                self.assertEqual(self.graph.weighted, mode == "weighted")
        self.post("configure", direction="directed", weight_mode="weighted")
        self.post("clear")
        self.assertEqual(self.graph.vertices, [])
        self.assertTrue(self.graph.directed and self.graph.weighted)
        self.post("sample")
        self.assertEqual(self.graph.edges()[0]["weight"], 100)
        self.assertEqual(len(self.graph.edges()), 14)
        self.post("reset")
        self.assertFalse(self.graph.directed or self.graph.weighted)
        self.assertEqual(len(self.graph.vertices), 10)

    def test_empty_graph_pages_and_traversal(self):
        self.post("clear")
        for path in ("/", "/graph", "/representation", "/traversal"):
            self.assertEqual(self.client.get(path).status_code, 200)
        response = self.client.post("/traversal/bfs", data={"start": "Main Gate"})
        self.assertIn(b"Add a location before running a traversal", response.data)
        self.assertNotIn(b'id="traversal-data"', response.data)

    def test_rendered_traversal_buttons_submit_to_working_routes(self):
        class ButtonParser(HTMLParser):
            def __init__(self):
                super().__init__()
                self.actions = []

            def handle_starttag(self, tag, attrs):
                attributes = dict(attrs)
                if tag == "button" and "formaction" in attributes:
                    self.actions.append(attributes["formaction"])

        parser = ButtonParser()
        parser.feed(self.client.get("/traversal").get_data(as_text=True))
        self.assertEqual(parser.actions, ["/traversal/bfs", "/traversal/dfs"])
        for action in parser.actions:
            response = self.client.post(action, data={"start": "Main Gate"})
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'id="traversal-data"', response.data)

    def test_invalid_forms_show_errors(self):
        for name in ("", "   ", "Main Gate"):
            self.assertIn(b'role="alert"', self.post("add-node", name=name).data)
        self.assertEqual(len(self.graph.vertices), 10)
        self.assertIn(b'role="alert"', self.post("add-edge", source="Fake", target="Library").data)
        self.assertIn(b'role="alert"', self.post("configure", direction="bad", weight_mode="weighted").data)
        self.assertIn(b'role="alert"', self.client.post("/traversal/bfs", data={"start": "Fake"}).data)
        self.assertIn(b'role="alert"', self.client.post("/traversal/bad", data={"start": "Main Gate"}).data)

    def test_weight_validation_on_server(self):
        self.post("configure", direction="directed", weight_mode="weighted")
        self.post("add-node", name="Hall")
        for weight in ("nan", "", "abc", "0", "-2"):
            response = self.post("add-edge", source="Library", target="Hall", weight=weight)
            self.assertIn(b'role="alert"', response.data)
        self.post("add-edge", source="Library", target="Hall", weight="42.5")
        self.assertEqual(self.graph.adjacency["Library"]["Hall"], 42.5)

    def test_labels_are_escaped_in_html_and_json(self):
        value = '<script>alert(1)</script>'
        response = self.post("add-node", name=value)
        self.assertNotIn(value.encode(), response.data)
        self.assertIn(b'&lt;script&gt;', response.data)
        self.assertIn(b'\\u003cscript\\u003e', response.data)
        response = self.client.get("/representation")
        self.assertNotIn(value.encode(), response.data)

    def test_mutations_require_post(self):
        self.assertEqual(self.client.get("/graph/clear").status_code, 405)
        self.assertEqual(len(self.graph.vertices), 10)

    def test_apps_have_independent_state_for_tests(self):
        self.post("clear")
        second_app = create_app({"TESTING": True})
        self.assertEqual(len(second_app.extensions["campus_graph"].vertices), 10)


if __name__ == "__main__":
    unittest.main()
