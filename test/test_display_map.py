from pathlib import Path

from dijkstra import DijkstraSPF

from src.constants import PRIORITY_QUIETNESS
from src.display_map import MapDisplayer
from src.graph_parser import GraphParser

resources_dir = Path(".") / 'resources'
MOCK_GRAPH_FILE = str(resources_dir / 'ophois-graph.txt')
MOCK_MAP_FILE = str(resources_dir / 'my_town.osm')


TEST_INIT_POINT = '6845757797'
TEST_END_POINT_SHORT = '6845757796'
TEST_END_POINT_LONG = '1238435933'


def test_create_graph_one_edge():
    test_graph_parser = GraphParser(MOCK_GRAPH_FILE, MOCK_MAP_FILE, PRIORITY_QUIETNESS)
    test_weighed_graph = test_graph_parser.parse_simplified_map_to_graph()
    test_dijkstra = DijkstraSPF(test_weighed_graph, TEST_INIT_POINT)

    map_displayer = MapDisplayer(test_graph_parser, test_dijkstra)
    map_displayer.get_quietest_way(TEST_INIT_POINT, TEST_END_POINT_SHORT)


def test_create_graph_four_edges():
    test_graph_parser = GraphParser(MOCK_GRAPH_FILE, MOCK_MAP_FILE, PRIORITY_QUIETNESS)
    test_weighed_graph = test_graph_parser.parse_simplified_map_to_graph()
    test_dijkstra = DijkstraSPF(test_weighed_graph, TEST_INIT_POINT)

    map_displayer = MapDisplayer(test_graph_parser, test_dijkstra)
    map_displayer.get_quietest_way(TEST_INIT_POINT, TEST_END_POINT_LONG)
