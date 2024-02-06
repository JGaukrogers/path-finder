import json

from itertools import pairwise

from src.graph_parser import SEPARATOR


def extract_osm_to_graph(osm_data: json) -> str:
    extracted_data = convert_json_to_graph(osm_data)
    return ''.join(extracted_data)


def convert_json_to_graph(downloaded_data: json) -> list[str]:
    parsed_graph = []
    for element in downloaded_data['elements']:
        if element['type'] == 'node':
            parsed_graph.append(extract_node(element))
        if element['type'] == 'way':
            parsed_graph = [*parsed_graph, *extract_way(element)]
    return parsed_graph


def extract_way(element) -> list:
    node_list = element['nodes']
    pairs = pairwise(node_list)
    pair_list = [f'{p[0]}{SEPARATOR}{p[1]}\n' for p in pairs]
    return pair_list


def extract_node(element) -> str:
    return f'{element["id"]}{SEPARATOR}{element["lat"]}{SEPARATOR}{element["lon"]}\n'
