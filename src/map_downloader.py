import subprocess
import requests

import src.constants as constants
from src.format import extract_and_write_to_file


class DataDownloader:

    def __init__(self, file_name: str, area_boundaries: dict, ophois: str=constants.DEFAULT_OPHOIS):
        self.area_boundaries = area_boundaries
        self.ophois = ophois
        self.osm_file = constants.OSM_FILENAME_TEMPLATE.format(file_name=file_name)
        self.extracted_graph = constants.EXTRACTED_GRAPH_FILENAME_TEMPLATE.format(file_name=file_name)
        self.simplified_graph = constants.SIMPLE_GRAPH_FILENAME_TEMPLATE.format(file_name=file_name)

    def get_simplified_graph(self):
        if self.is_ophois_available():
            self.get_map_data()
            extract_and_write_to_file(self.osm_file, self.extracted_graph)
            subprocess.check_output(
                constants.COMMAND_SIMPLIFY_GRAPH.format(extracted_graph=self.extracted_graph, ophois_path=self.ophois,
                                                        simplified_graph=self.simplified_graph), shell=True)
            subprocess.check_output(constants.COMMAND_REMOVE_FILES.format(extracted_graph=self.extracted_graph), shell=True)

        else:
            return False
        return True

    def get_map_data(self):
        overpass_query = constants.OVERPASS_QUERY.format(n=self.area_boundaries['north'],
                                                         s=self.area_boundaries['south'],
                                                         e=self.area_boundaries['east'],
                                                         w=self.area_boundaries['west'])
        response = requests.get(constants.OVERPASS_URL,
                                params={'data': overpass_query})
        with open(self.osm_file, 'w') as fd:
            fd.write(response.text)

    def is_ophois_available(self):
        try:
            res = subprocess.check_output(constants.COMMAND_OPHOIS_AVAILABLE.format(ophois_path=self.ophois), shell=True)
            # print('Decoded string: ', res.decode('utf-8'))
        except subprocess.CalledProcessError:
            return False
        return True
