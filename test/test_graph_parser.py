import pytest
from pathlib import Path
from dijkstra import DijkstraSPF

from src import graph_parser
from src.constants import PRIORITY_QUIETNESS
from src.graph_parser import GraphParser
from src.graph_elements import highway_types
from test.test_constants import TEST_INIT_POINT_ID, TEST_END_POINT_SHORT_ID, TEST_END_POINT_LONG_ID

resources_dir = Path("..") / 'resources'
graph_file_path = str(resources_dir / 'ophois-graph.txt')
map_file_path = str(resources_dir / 'my_town.osm')

parser = GraphParser(graph_file_path, map_file_path, PRIORITY_QUIETNESS)
graph = parser.parse_simplified_map_to_graph()

TEST_INIT_POINT = parser.nodeId_to_nodes_dict[str(TEST_INIT_POINT_ID)]
TEST_END_POINT_SHORT = parser.nodeId_to_nodes_dict[str(TEST_END_POINT_SHORT_ID)]
TEST_END_POINT_LONG = parser.nodeId_to_nodes_dict[str(TEST_END_POINT_LONG_ID)]

TEST_PATH_POSSIBLE_RESULT_1 = [
    TEST_INIT_POINT,
    TEST_END_POINT_SHORT,
    parser.nodeId_to_nodes_dict['2215046974'],
    TEST_END_POINT_LONG,
]

COMPOSED_NODE = '9311284676-9311288421'
NODE_TO_COMPOSED_NODE = '9311288435'


@pytest.fixture()
def dijkstra_ways_init_simple_node():
    dijkstra = DijkstraSPF(graph, TEST_INIT_POINT)
    return dijkstra


@pytest.fixture()
def dijkstra_ways_init_composed_node():
    dijkstra = DijkstraSPF(graph, COMPOSED_NODE)
    return dijkstra


@pytest.fixture()
def simplified_graph():
    parser.parse_simplified_map_to_graph()
    return parser


def test_shortest_distance_is_correct(dijkstra_ways_init_simple_node):
    assert 9 == dijkstra_ways_init_simple_node.get_distance(TEST_END_POINT_LONG)


def test_get_right_path(dijkstra_ways_init_simple_node):
    assert dijkstra_ways_init_simple_node.get_path(TEST_END_POINT_LONG) == TEST_PATH_POSSIBLE_RESULT_1


def test_get_right_weight(dijkstra_ways_init_simple_node):
    assert dijkstra_ways_init_simple_node.get_distance(TEST_END_POINT_SHORT) == highway_types['residential']


# Test for grouped nodes
@pytest.mark.skip('FIX: why does it return inf?')
def test_composed_node_has_right_number_of_ways(simplified_graph):
    node0, node1 = COMPOSED_NODE.split(graph_parser.NODE_SEPARATOR)
    assert len(simplified_graph.nodeId_to_nodeInfo_dict[node0].ways) == 2
    assert len(simplified_graph.nodeId_to_nodeInfo_dict[node1].ways) == 2


def test_composed_node_connects_one_street(dijkstra_ways_init_composed_node):
    assert dijkstra_ways_init_composed_node.get_distance(NODE_TO_COMPOSED_NODE) == highway_types['track']
