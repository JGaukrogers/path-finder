import pytest
from dijkstra import DijkstraSPF

from src.constants import PRIORITY_QUIETNESS
from src.display_map import MapDisplayer
from src.graph_parser import GraphParser
from test.test_constants import TEST_INIT_POINT_ID, TEST_END_POINT_SHORT_ID, TEST_END_POINT_LONG_ID, \
    MOCK_GRAPH_FILE, MOCK_MAP_FILE

test_graph_parser = GraphParser(MOCK_GRAPH_FILE, MOCK_MAP_FILE, PRIORITY_QUIETNESS)
test_weighed_graph = test_graph_parser.parse_simplified_map_to_graph()

INIT_POINT = test_graph_parser.nodeId_to_nodes_dict[str(TEST_INIT_POINT_ID)]
END_POINT_SHORT = test_graph_parser.nodeId_to_nodes_dict[str(TEST_END_POINT_SHORT_ID)]
END_POINT_LONG = test_graph_parser.nodeId_to_nodes_dict[str(TEST_END_POINT_LONG_ID)]

test_dijkstra = DijkstraSPF(test_weighed_graph, INIT_POINT)


@pytest.fixture()
def map_displayer():
    return MapDisplayer(test_graph_parser, test_dijkstra)


def test_create_graph_one_edge(map_displayer):
    map_displayer.get_quietest_way(str(TEST_INIT_POINT_ID), str(TEST_END_POINT_SHORT_ID), 'index_short.html')


def test_create_graph_four_edges(map_displayer):
    map_displayer.get_quietest_way(str(TEST_INIT_POINT_ID), str(TEST_END_POINT_LONG_ID), 'index_long.html')
