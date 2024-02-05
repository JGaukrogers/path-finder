import json

from src.graph_elements import NodeInfo
from src.graph_elements import Way


class MapParser:
    def __init__(self, map_file_path: json):
        self.map_file_path = map_file_path

    def parse_osm_map_json(self, node_to_way: dict[str, NodeInfo]):
        for element in self.map_file_path['elements']:
            if element['type'] == 'node':
                node_id = str(element['id'])
                if node_id in node_to_way:
                    node_to_way[node_id].lat = float(element['lat'])
                    node_to_way[node_id].lon = float(element['lon'])
            if element['type'] == 'way':
                node_list = element['nodes']
                node_list = [str(node) for node in node_list]
                for node_value in node_list:
                    if node_value in node_to_way:
                        node_to_way[node_value].ways.add(Way(element))
