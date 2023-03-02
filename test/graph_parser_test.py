import unittest
from os import getcwd
from dijkstra import DijkstraSPF

from src.graph_parser import GraphParser

resources_dir = getcwd() + '/../resources'
graph_file_path = resources_dir + '/ophois-graph.txt'

MOCK_INIT_POINT = '6845757797'
MOCK_END_POINT = '1238436031'


class MyTestCase(unittest.TestCase):
    def test_something(self):
        parser = GraphParser(graph_file_path)
        graph = parser.parse_simplified_map_to_graph()
        dijkstra = DijkstraSPF(graph, MOCK_INIT_POINT)

        print(dijkstra.get_distance(MOCK_END_POINT))

        self.assertEqual(dijkstra.get_distance(MOCK_END_POINT), 5)


if __name__ == '__main__':
    unittest.main()
