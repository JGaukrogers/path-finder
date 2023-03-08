from xml.dom import minidom

from src.node_info import NodeInfo
from src.way import Way


class MapParser:
    def __init__(self, map_file_path):
        self.map_file_path = map_file_path

    def parse_dom(self, node_to_way_dict: dict[str, NodeInfo]):
        dom_parser = minidom.parse(self.map_file_path)

        ways = dom_parser.getElementsByTagName('way')

        for way in ways:
            node_list = way.getElementsByTagName('nd')
            for node in node_list:
                node_value = node.attributes['ref'].value
                if node_value in node_to_way_dict:
                    node_to_way_dict[node_value].add_way(Way(way))
