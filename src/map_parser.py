import json
from xml.dom import minidom

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

    def parse_osm_map(self, node_to_way: dict[str, NodeInfo]):
        print(self.map_file_path)
        dom_parser = minidom.parse(self.map_file_path)

        self.parse_ways_xml(dom_parser, node_to_way)
        self.parse_node_coordinates_xml(dom_parser, node_to_way)

    def parse_ways_xml(self, osm_map_parser, node_to_way: dict[str, NodeInfo]):
        xml_ways = osm_map_parser.getElementsByTagName('way')
        for way in xml_ways:
            node_list = way.getElementsByTagName('nd')
            for node in node_list:
                node_value = node.attributes['ref'].value
                if node_value in node_to_way:
                    node_to_way[node_value].ways.add(Way(way))

    def parse_node_coordinates_xml(self, osm_map_parser, node_to_way: dict[str, NodeInfo]):
        xml_nodes = osm_map_parser.getElementsByTagName('node')
        for xml_node in xml_nodes:
            node_id = xml_node.attributes['id'].value
            if node_id in node_to_way:
                lat = float(xml_node.attributes['lat'].value)
                lon = float(xml_node.attributes['lon'].value)
                node_to_way[node_id].lat = lat
                node_to_way[node_id].lon = lon
