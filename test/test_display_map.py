import pytest
from dijkstra import DijkstraSPF

from src.constants import PRIORITY_QUIETNESS
from src.display_map import MapDisplayer
from src.graph_parser import GraphParser
from test.test_constants import TEST_INIT_POINT_ID, TEST_END_POINT_SHORT_ID, TEST_END_POINT_LONG_ID, \
    MOCK_MAP_CONTENT, MOCK_GRAPH_CONTENT

test_graph_parser = GraphParser(MOCK_GRAPH_CONTENT, MOCK_MAP_CONTENT, PRIORITY_QUIETNESS)
test_weighed_graph = test_graph_parser.parse_map_to_graph()


test_dijkstra = DijkstraSPF(test_weighed_graph, TEST_INIT_POINT_ID)


@pytest.fixture()
def map_displayer():
    return MapDisplayer(test_graph_parser, test_dijkstra)


def test_create_graph_one_edge(map_displayer):
    map_displayer.get_quietest_way(TEST_INIT_POINT_ID, TEST_END_POINT_SHORT_ID, 'index_short.html')


def test_create_graph_four_edges(map_displayer):
    map_displayer.get_quietest_way(TEST_INIT_POINT_ID, TEST_END_POINT_LONG_ID, 'index_long.html')
