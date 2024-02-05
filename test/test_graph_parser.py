import pytest
from dijkstra import DijkstraSPF

from src.constants import PRIORITY_QUIETNESS
from src.graph_elements import highway_types
from src.graph_parser import GraphParser
from test.test_constants import TEST_INIT_POINT_ID, TEST_END_POINT_SHORT_ID, TEST_END_POINT_LONG_ID, \
    MOCK_GRAPH_CONTENT, MOCK_MAP_CONTENT

parser = GraphParser(MOCK_GRAPH_CONTENT, MOCK_MAP_CONTENT, PRIORITY_QUIETNESS)
graph = parser.parse_map_to_graph()

TEST_PATH_POSSIBLE_RESULT_1 = [
    TEST_INIT_POINT_ID,
    TEST_END_POINT_SHORT_ID,
    '6888567898',
    '2215046974',
    '430856696',
    TEST_END_POINT_LONG_ID,
]


@pytest.fixture()
def dijkstra_ways_init_simple_node():
    dijkstra = DijkstraSPF(graph, TEST_INIT_POINT_ID)
    return dijkstra


@pytest.fixture()
def simplified_graph():
    parser.parse_map_to_graph()
    return parser


def test_shortest_distance_is_correct(dijkstra_ways_init_simple_node):
    assert dijkstra_ways_init_simple_node.get_distance(TEST_END_POINT_LONG_ID) == 21


def test_get_right_path(dijkstra_ways_init_simple_node):
    assert dijkstra_ways_init_simple_node.get_path(TEST_END_POINT_LONG_ID) == TEST_PATH_POSSIBLE_RESULT_1


def test_get_right_weight(dijkstra_ways_init_simple_node):
    assert dijkstra_ways_init_simple_node.get_distance(TEST_END_POINT_SHORT_ID) == highway_types['residential']
