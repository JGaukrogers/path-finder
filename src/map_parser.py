import json

from src.graph_elements import NodeInfo
from src.graph_elements import Way


class MapParser:
    def __init__(self, map_file_path):
        self.map_file_path = map_file_path

    def parse_osm_map_json(self, node_to_way: dict[str, NodeInfo]):
        with open(self.map_file_path) as file:
            json_string = json.load(file)
            for element in json_string['elements']:
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
