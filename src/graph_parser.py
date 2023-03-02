from dijkstra import Graph

SEPARATOR = '␟'


class GraphParser:

    def __init__(self, graph_file_path):
        self.graph_file_path = graph_file_path
        self.node_to_way_dict = dict()

    def get_weight(self, node_id_0, node_id_1):
        return 1

    def parse_simplified_map_to_graph(self):
        graph = Graph()

        with open(self.graph_file_path, "r") as simplified_graph_file:
            for line in simplified_graph_file:
                line = line.strip()
                fields = line.split('␟')
                if len(fields) == 3:
                    node_id = fields[0]
                    self.node_to_way_dict[node_id] = []
                elif len(fields) == 2:
                    node_id_0 = fields[0]
                    node_id_1 = fields[1]
                    weight = self.get_weight(node_id_0, node_id_1)
                    graph.add_edge(node_id_0, node_id_1, weight)
                    graph.add_edge(node_id_1, node_id_0, weight)

        return graph
