from os import getcwd
from dijkstra import Graph
from dijkstra import DijkstraSPF

resources_dir = getcwd() + '/resources'
graph_file_path = resources_dir + '/ophois-graph.txt'
SEPARATOR = '␟'

node_to_way_dict = dict()


def get_weight(node_id_0, node_id_1):
    return 1


def parse_simplified_map_to_graph():
    graph = Graph()

    with open(graph_file_path, "r") as simplified_graph_file:
        for line in simplified_graph_file:
            line = line.strip()
            fields = line.split('␟')
            if len(fields) == 3:
                node_id = fields[0]
                node_to_way_dict[node_id] = []
            elif len(fields) == 2:
                node_id_0 = fields[0]
                node_id_1 = fields[1]
                weight = get_weight(node_id_0, node_id_1)
                graph.add_edge(node_id_0, node_id_1, weight)
                graph.add_edge(node_id_1, node_id_0, weight)

    return graph

MOCK_INIT_POINT = '6845757797'
MOCK_END_POINT = '1238436031'


graph = parse_simplified_map_to_graph()
dijkstra = DijkstraSPF(graph, MOCK_INIT_POINT)

print(dijkstra.get_distance(MOCK_END_POINT))
