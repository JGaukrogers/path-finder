from dijkstra import Graph

from src.map_parser import MapParser
from src.graph_elements import NodeInfo

SEPARATOR = '␟'
NODE_SEPARATOR = '-'


class GraphParser:

    def __init__(self, graph_file_path: str, map_file_path: str):
        self.graph_file_path = graph_file_path
        self.map_file_path = map_file_path
        self.nodeId_to_nodeInfo_dict = dict()
        self.edge_to_weight_dict = dict()
        self.nodeId_to_nodes_dict = dict()

    def parse_simplified_map_to_graph(self):

        with open(self.graph_file_path, "r") as simplified_graph_file:
            for line in simplified_graph_file:
                line = line.strip()
                fields = line.split(SEPARATOR)
                if len(fields) == 3:
                    node_ids = fields[0]
                    for node_id in node_ids.split(NODE_SEPARATOR):
                        self.nodeId_to_nodeInfo_dict[node_id] = NodeInfo()
                        self.nodeId_to_nodes_dict[node_id] = node_ids

                elif len(fields) == 2:
                    node_ids_0, node_ids_1 = fields
                    self.edge_to_weight_dict[(node_ids_0, node_ids_1)] = None

        self.populate_node_to_way_dict()
        graph = self.calculate_weights()
        return graph

    def populate_node_to_way_dict(self):
        map_parser = MapParser(self.map_file_path)
        map_parser.parse_osm_map(self.nodeId_to_nodeInfo_dict)

    def calculate_weights(self):
        graph = Graph()
        for node_id_0, node_id_1 in self.edge_to_weight_dict:
            weight = self.get_weight(node_id_0, node_id_1)
            graph.add_edge(node_id_0, node_id_1, weight)
            graph.add_edge(node_id_1, node_id_0, weight)
        return graph

    def get_weight(self, node_ids_0: str, node_ids_1: str):
        ways_n0 = self.get_ways_for_nodes(node_ids_0)
        ways_n1 = self.get_ways_for_nodes(node_ids_1)
        # len(common_ways) can be > 1 if two or more ways are parallel to each other between two nodes.
        # For example, we have a road and a park way
        common_ways = ways_n0 & ways_n1
        weight = sum(way.get_quietness_value() for way in common_ways)
        return weight

    def get_ways_for_nodes(self, node_ids: str):
        ways = set()
        for node_id in node_ids.split(NODE_SEPARATOR):
            ways.update(self.nodeId_to_nodeInfo_dict[node_id].ways)
        return ways
