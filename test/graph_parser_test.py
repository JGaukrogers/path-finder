import unittest
from os import getcwd
from dijkstra import DijkstraSPF

from src.graph_parser import GraphParser

resources_dir = getcwd() + '/../resources'
graph_file_path = resources_dir + '/ophois-graph.txt'

TEST_INIT_POINT = '6845757797'
TEST_END_POINT = '1238436031'
TEST_PATH_POSSIBLE_RESULT_1 = ['6845757797', '6845757796', '10275176304', '10275291415', '10275290094', '1238436031']
TEST_PATH_POSSIBLE_RESULT_2 = ['6845757797', '6845757796', '10275176304', '10275295121', '10275290094', '1238436031']


class MyTestCase(unittest.TestCase):
    def test_shortest_distance_is_correct(self):
        parser = GraphParser(graph_file_path)
        graph = parser.parse_simplified_map_to_graph()
        dijkstra = DijkstraSPF(graph, TEST_INIT_POINT)

        self.assertEqual(5, dijkstra.get_distance(TEST_END_POINT))

    # TODO: find an example where the result is always the same
    # def test_get_right_path(self):
    #     parser = GraphParser(graph_file_path)
    #     graph = parser.parse_simplified_map_to_graph()
    #     dijkstra = DijkstraSPF(graph, TEST_INIT_POINT)
    #
    #     print(dijkstra.get_path(TEST_END_POINT))
    #
    #     self.assertListEqual(dijkstra.get_path(TEST_END_POINT), TEST_PATH_POSSIBLE_RESULT_1)


if __name__ == '__main__':
    unittest.main()
