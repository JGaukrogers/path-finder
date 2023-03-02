from dijkstra import Graph

from src.map_parser import MapParser

SEPARATOR = '␟'


class GraphParser:

    def __init__(self, graph_file_path, map_file_path):
        self.graph_file_path = graph_file_path
        self.map_file_path = map_file_path
        self.node_to_way_dict = dict()
        self.edge_to_weight_dict = dict()

    def get_weight(self, node_id_0: str, node_id_1: str):
        return 1

    def parse_simplified_map_to_graph(self):
        graph = Graph()

        with open(self.graph_file_path, "r") as simplified_graph_file:
            for line in simplified_graph_file:
                line = line.strip()
                fields = line.split(SEPARATOR)
                if len(fields) == 3:
                    node_id = fields[0]
                    self.node_to_way_dict[node_id] = []
                elif len(fields) == 2:
                    node_id_0, node_id_1 = fields
                    self.edge_to_weight_dict[(node_id_0, node_id_1)] = None
                    weight = self.get_weight(node_id_0, node_id_1)
                    graph.add_edge(node_id_0, node_id_1, weight)
                    graph.add_edge(node_id_1, node_id_0, weight)

        self.populate_node_to_way_dict()
        return graph

    def populate_node_to_way_dict(self):
        map_parser = MapParser(self.map_file_path)
        map_parser.parse_dom(self.node_to_way_dict)
