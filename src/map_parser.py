import xml.etree.ElementTree as elementTree
from xml.dom import minidom
from os import getcwd

resources_dir = getcwd() + '/../resources'
map_file_path = resources_dir + '/my_town.osm'


class MapParser:
    def parse_et(self):
        et_parser = elementTree.parse(map_file_path)

        root = et_parser.getroot()
        way_list = root.findall('way')

        for i in way_list:
            print(i.tag, i.attrib)

        # ways = parser.getElementsByTagName('way')
        # print(len(ways))
        #
        # tag= ways[0]
        # print(tag.attributes['id'].value)

    def parse_dom(self, node_to_way_dict: dict[str, list]):
        dom_parser = minidom.parse(map_file_path)

        ways = dom_parser.getElementsByTagName('way')

        for way in ways:
            node_list = way.getElementsByTagName('nd')
            for node in node_list:
                node_value = node.attributes['ref'].value
                if node_value in node_to_way_dict:
                    node_to_way_dict[node_value].append(way)


parser = MapParser()
parser.parse_dom({'6845757797': [], '6845757796': []})
