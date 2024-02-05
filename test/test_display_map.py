import pytest
from dijkstra import DijkstraSPF

from src.constants import PRIORITY_QUIETNESS
from src.display_map import MapDisplayer
from src.graph_parser import GraphParser
from test.test_constants import TEST_INIT_POINT_ID, TEST_END_POINT_SHORT_ID, TEST_END_POINT_LONG_ID, \
    MOCK_MAP_CONTENT, MOCK_GRAPH_CONTENT, \
    INDEX_SHORT_HTML, INDEX_LONG_HTML

test_graph_parser = GraphParser(MOCK_GRAPH_CONTENT, MOCK_MAP_CONTENT, PRIORITY_QUIETNESS)
test_weighed_graph = test_graph_parser.parse_map_to_graph()


test_dijkstra = DijkstraSPF(test_weighed_graph, TEST_INIT_POINT_ID)


@pytest.fixture()
def map_displayer():
    return MapDisplayer(test_graph_parser, test_dijkstra)


def test_create_graph_one_edge(map_displayer):
    map_displayer.generate_map(TEST_INIT_POINT_ID, TEST_END_POINT_SHORT_ID, INDEX_SHORT_HTML)


def test_create_graph_four_edges(map_displayer):
    map_displayer.generate_map(TEST_INIT_POINT_ID, TEST_END_POINT_LONG_ID, INDEX_LONG_HTML)
