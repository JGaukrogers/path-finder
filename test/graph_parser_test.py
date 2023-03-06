import pytest
from os import getcwd
from dijkstra import DijkstraSPF

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


@pytest.fixture()
def initialise_graph():
    parser = GraphParser(graph_file_path, map_file_path)
    graph = parser.parse_simplified_map_to_graph()
    dijkstra = DijkstraSPF(graph, TEST_INIT_POINT)
    return dijkstra


def test_shortest_distance_is_correct(initialise_graph):
    assert 9 == initialise_graph.get_distance(TEST_END_POINT_LONG)


# TODO: find an example where the result is always the same
def test_get_right_path(initialise_graph):
    assert initialise_graph.get_path(TEST_END_POINT_LONG) == TEST_PATH_POSSIBLE_RESULT_1 \
           or initialise_graph.get_path(TEST_END_POINT_LONG) == TEST_PATH_POSSIBLE_RESULT_2

def test_get_right_weight(initialise_graph):
    assert initialise_graph.get_distance(TEST_END_POINT_SHORT) == highway_types['residential']
