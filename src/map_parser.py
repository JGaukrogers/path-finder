from xml.dom import minidom

from src.graph_elements import NodeInfo
from src.graph_elements import Way


class MapParser:
    def __init__(self, map_file_path):
        self.map_file_path = map_file_path

    def parse_osm_map(self, node_to_way_dict: dict[str, NodeInfo]):
        dom_parser = minidom.parse(self.map_file_path)

        self.parse_ways(dom_parser, node_to_way_dict)
        self.parse_node_coordinates(dom_parser, node_to_way_dict)

    def parse_ways(self, dom_parser, node_to_way_dict):
        xml_ways = dom_parser.getElementsByTagName('way')
        for way in xml_ways:
            node_list = way.getElementsByTagName('nd')
            for node in node_list:
                node_value = node.attributes['ref'].value
                if node_value in node_to_way_dict:
                    node_to_way_dict[node_value].ways.add(Way(way))

    def parse_node_coordinates(self, dom_parser, node_to_way_dict):
        xml_nodes = dom_parser.getElementsByTagName('node')
        for xml_node in xml_nodes:
            node_id = xml_node.attributes['id'].value
            if node_id in node_to_way_dict:
                lat = float(xml_node.attributes['lat'].value)
                lon = float(xml_node.attributes['lon'].value)
                node_to_way_dict[node_id].lat = lat
                node_to_way_dict[node_id].lon = lon
