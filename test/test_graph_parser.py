import pytest
from dijkstra import DijkstraSPF
from haversine import haversine, Unit

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
    assert dijkstra_ways_init_simple_node.get_distance(TEST_END_POINT_LONG_ID) == 68.21850243944048


def test_get_right_path(dijkstra_ways_init_simple_node):
    assert dijkstra_ways_init_simple_node.get_path(TEST_END_POINT_LONG_ID) == TEST_PATH_POSSIBLE_RESULT_1


def test_get_right_weight(dijkstra_ways_init_simple_node):
    init_node_info = parser.nodeId_to_nodeInfo_dict[TEST_INIT_POINT_ID]
    end_node_info = parser.nodeId_to_nodeInfo_dict[TEST_END_POINT_SHORT_ID]
    coordinates_0 = (float(init_node_info.lat), float(init_node_info.lon))
    coordinates_1 = (float(end_node_info.lat), float(end_node_info.lon))
    distance_ratio = 0.1 * haversine(coordinates_0, coordinates_1, unit=Unit.METERS)
    assert dijkstra_ways_init_simple_node.get_distance(TEST_END_POINT_SHORT_ID) == highway_types['residential'] + distance_ratio


def test_populate_note_to_info_dict(simplified_graph):
    assert len(simplified_graph.nodeId_to_nodeInfo_dict[TEST_INIT_POINT_ID].ways) == 1
    assert len(simplified_graph.nodeId_to_nodeInfo_dict[TEST_END_POINT_SHORT_ID].ways) == 2
