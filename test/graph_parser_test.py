import pytest
from os import getcwd
from dijkstra import DijkstraSPF

from src import graph_parser
from src.graph_parser import GraphParser
from src.way import highway_types

resources_dir = getcwd() + '/../resources'
graph_file_path = resources_dir + '/ophois-graph.txt'
map_file_path = resources_dir + '/my_town.osm'

TEST_INIT_POINT = '6845757797'
TEST_END_POINT_SHORT = '6845757796'
TEST_END_POINT_LONG = '1238436031'
TEST_PATH_POSSIBLE_RESULT_1 = ['6845757797', '6845757796', '10275176304', '10275291415', '10275290094', '1238436031']
TEST_PATH_POSSIBLE_RESULT_2 = ['6845757797', '6845757796', '10275176304', '10275295121', '10275290094', '1238436031']

COMPOSED_NODE = '9311284676-9311288421'
NODE_TO_COMPOSED_NODE = '9311288435'


@pytest.fixture()
def dijkstra_ways_init_simple_node():
    parser = GraphParser(graph_file_path, map_file_path)
    graph = parser.parse_simplified_map_to_graph()
    dijkstra = DijkstraSPF(graph, TEST_INIT_POINT)
    return dijkstra

@pytest.fixture()
def dijkstra_ways_init_composed_node():
    parser = GraphParser(graph_file_path, map_file_path)
    graph = parser.parse_simplified_map_to_graph()
    dijkstra = DijkstraSPF(graph, TEST_INIT_POINT)
    return dijkstra

@pytest.fixture()
def simplified_graph():
    parser = GraphParser(graph_file_path, map_file_path)
    parser.parse_simplified_map_to_graph()
    return parser


def test_shortest_distance_is_correct(dijkstra_ways_init_simple_node):
    assert 9 == dijkstra_ways_init_simple_node.get_distance(TEST_END_POINT_LONG)


# TODO: find an example where the result is always the same
def test_get_right_path(dijkstra_ways_init_simple_node):
    assert dijkstra_ways_init_simple_node.get_path(TEST_END_POINT_LONG) in (TEST_PATH_POSSIBLE_RESULT_1, TEST_PATH_POSSIBLE_RESULT_2)


def test_get_right_weight(dijkstra_ways_init_simple_node):
    assert dijkstra_ways_init_simple_node.get_distance(TEST_END_POINT_SHORT) == highway_types['residential']


# Test for grouped nodes

def test_composed_node_has_right_number_of_ways(simplified_graph):
    node0, node1 = COMPOSED_NODE.split(graph_parser.NODE_SEPARATOR)
    assert len(simplified_graph.node_to_way_dict[node0]) == 2
    assert len(simplified_graph.node_to_way_dict[node1]) == 2


def test_composed_node_connects_one_street(dijkstra_ways_init_composed_node):
    assert dijkstra_ways_init_composed_node.get_distance(TEST_END_POINT_SHORT) == highway_types['track']
