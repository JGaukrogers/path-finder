import json
import math

from dijkstra import Graph
from haversine import haversine, Unit

from src.constants import PRIORITY_QUIETNESS, PRIORITY_SHORT_DISTANCE, SEPARATOR
from src.graph_elements import NodeInfo, Way


class GraphParser:

    def __init__(self, map_graph: str, downloaded_map_info: json, path_way_priority: str):
        self.map_graph = map_graph
        self.downloaded_map_info = downloaded_map_info
        self.path_way_priority = path_way_priority
        self.nodeId_to_nodeInfo_dict = {}
        self.edge_to_weight_dict = {}

    def parse_map_to_graph(self) -> Graph:
        for line in self.map_graph.split():
            line = line.strip()
            fields = line.split(SEPARATOR)
            if len(fields) == 3:
                node_id = fields[0]
                self.nodeId_to_nodeInfo_dict[node_id] = NodeInfo()

            elif len(fields) == 2:
                node_ids_0, node_ids_1 = fields
                self.edge_to_weight_dict[(node_ids_0, node_ids_1)] = None

        self.populate_node_to_nodeInfo_dict()
        graph = self.create_weighted_graph()
        return graph

    def populate_node_to_nodeInfo_dict(self):
        for element in self.downloaded_map_info['elements']:
            if element['type'] == 'node':
                node_id = str(element['id'])
                if node_id in self.nodeId_to_nodeInfo_dict:
                    self.nodeId_to_nodeInfo_dict[node_id].lat = float(element['lat'])
                    self.nodeId_to_nodeInfo_dict[node_id].lon = float(element['lon'])
            if element['type'] == 'way':
                node_list = element['nodes']
                node_list = [str(node) for node in node_list]
                for node_value in node_list:
                    if node_value in self.nodeId_to_nodeInfo_dict:
                        self.nodeId_to_nodeInfo_dict[node_value].ways.add(Way(element))

    def create_weighted_graph(self) -> Graph:
        graph = Graph()
        for node_id_0, node_id_1 in self.edge_to_weight_dict:
            weight = self.get_weight(node_id_0, node_id_1)
            graph.add_edge(node_id_0, node_id_1, weight)
            graph.add_edge(node_id_1, node_id_0, weight)
        return graph

    def get_weight(self, node_id_0: str, node_id_1: str) -> float:
        ways_n0 = self.get_ways_for_nodes(node_id_0)
        ways_n1 = self.get_ways_for_nodes(node_id_1)
        # len(common_ways) can be > 1 if two or more ways are parallel to each other between two nodes.
        # For example, we have a road and a park way
        common_ways = ways_n0 & ways_n1
        weight = 1
        if self.path_way_priority == PRIORITY_QUIETNESS:
            # Is sum a good idea? Better min?
            weight = sum(way.get_quietness_value() for way in common_ways)
        elif self.path_way_priority == PRIORITY_SHORT_DISTANCE:
            weight = self.get_distance_for_nodes(node_id_0, node_id_1)
        return weight

    def get_ways_for_nodes(self, node_id: str) -> set:
        ways = set()
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
