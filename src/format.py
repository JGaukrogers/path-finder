import json

from itertools import pairwise

from src.graph_parser import SEPARATOR


def extract_and_write_to_file(in_file, out_file):
    extracted_data = format_json_to_graph(in_file)
    with open(out_file, 'w') as f:
        f.writelines(extracted_data)


def format_json_to_graph(file_name: str) -> list[str]:
    parsed_graph = []
    with open(file_name) as file:
        json_string = json.load(file)
        for element in json_string['elements']:
            if element['type'] == 'node':
                parsed_graph.append(extract_node(element))
            if element['type'] == 'way':
                parsed_graph = [*parsed_graph, *extract_way(element)]
    return parsed_graph


def extract_way(element):
    node_list = element['nodes']
    pairs = pairwise(node_list)
    pair_list = [f'{p[0]}{SEPARATOR}{p[1]}\n' for p in pairs]
    return pair_list


def extract_node(element):
    return f'{element["id"]}{SEPARATOR}{element["lat"]}{SEPARATOR}{element["lon"]}\n'
