import math

from dijkstra import Graph

from src.constants import PRIORITY_QUIETNESS, PRIORITY_SHORT_DISTANCE
from src.map_parser import MapParser
from src.graph_elements import NodeInfo
from haversine import haversine, Unit

SEPARATOR = '␟'
NODE_SEPARATOR = '-'


class GraphParser:

    def __init__(self, graph_file_path: str, map_file_path: str, path_way_priority: str):
        self.graph_file_path = graph_file_path
        self.map_file_path = map_file_path
        self.path_way_priority = path_way_priority
        self.nodeId_to_nodeInfo_dict = {}
        self.edge_to_weight_dict = {}
        self.nodeId_to_nodes_dict = {}

    def parse_simplified_map_to_graph(self) -> Graph:

        with open(self.graph_file_path, "r") as simplified_graph_file:
            for line in simplified_graph_file:
                line = line.strip()
                fields = line.split(SEPARATOR)
                if len(fields) == 3:
                    node_ids = fields[0]
                    for node_id in node_ids.split(NODE_SEPARATOR):
                        self.nodeId_to_nodeInfo_dict[node_id] = NodeInfo()
                        self.nodeId_to_nodes_dict[node_id] = self.make_frozenset(node_ids)

                elif len(fields) == 2:
                    node_ids_0, node_ids_1 = fields
                    self.edge_to_weight_dict[(self.make_frozenset(node_ids_0), self.make_frozenset(node_ids_1))] = None

        self.populate_node_to_way_dict()
        graph = self.calculate_weights()
        return graph

    def populate_node_to_way_dict(self):
        map_parser = MapParser(self.map_file_path)
        map_parser.parse_osm_map_json(self.nodeId_to_nodeInfo_dict)

    def calculate_weights(self) -> Graph:
        graph = Graph()
        for node_id_0, node_id_1 in self.edge_to_weight_dict:
            weight = self.get_weight(node_id_0, node_id_1)
            graph.add_edge(node_id_0, node_id_1, weight)
            graph.add_edge(node_id_1, node_id_0, weight)
        return graph

    def get_weight(self, node_ids_0: frozenset, node_ids_1: frozenset) -> float:
        ways_n0 = self.get_ways_for_nodes(node_ids_0)
        ways_n1 = self.get_ways_for_nodes(node_ids_1)
        # len(common_ways) can be > 1 if two or more ways are parallel to each other between two nodes.
        # For example, we have a road and a park way
        common_ways = ways_n0 & ways_n1
        weight = 1
        if self.path_way_priority == PRIORITY_QUIETNESS:
            # Is sum a good idea? Better min?
            weight = sum(way.get_quietness_value() for way in common_ways)
        elif self.path_way_priority == PRIORITY_SHORT_DISTANCE:
            weight = self.get_distance_for_nodes(self.get_first_node(node_ids_0),
                                                 self.get_first_node(node_ids_1))
        return weight

    @staticmethod
    def get_first_node(node_ids: frozenset) -> str:
        e, *_ = node_ids
        return e

    def get_ways_for_nodes(self, node_ids: frozenset) -> set:
        ways = set()
        for node_id in node_ids:
            ways.update(self.nodeId_to_nodeInfo_dict[node_id].ways)
        return ways

    def get_distance_for_nodes(self, node_id_0, node_id_1) -> float:
        node_0 = self.nodeId_to_nodeInfo_dict[node_id_0]
        node_1 = self.nodeId_to_nodeInfo_dict[node_id_1]

        coordinates_0 = (node_0.lat, node_0.lon)
        coordinates_1 = (node_1.lat, node_1.lon)

        return haversine(coordinates_0, coordinates_1, unit=Unit.METERS)

    def get_closest_node_id(self, coordinates: tuple[float, float]) -> str:
        closest_node = None
        closest_distance = math.inf
        for node_id, node in self.nodeId_to_nodeInfo_dict.items():
            lat = node.lat
            lon = node.lon
            distance = haversine((lat, lon), (coordinates[0], coordinates[1]), unit=Unit.METERS)
            if distance < closest_distance:
                closest_distance = distance
                closest_node = node_id

        return closest_node

    @staticmethod
    def make_frozenset(node_ids) -> frozenset:
        nodes_set = frozenset(node_ids.split(NODE_SEPARATOR))
        return nodes_set
