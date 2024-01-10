import requests

import src.constants as constants
from src.format import extract_and_write_to_file


class DataDownloader:

    def __init__(self, file_name: str, area_boundaries: dict):
        self.area_boundaries = area_boundaries
        self.osm_file = constants.OSM_FILENAME_TEMPLATE.format(file_name=file_name)
        self.extracted_graph = constants.EXTRACTED_GRAPH_FILENAME_TEMPLATE.format(file_name=file_name)
        self.simplified_graph = constants.SIMPLE_GRAPH_FILENAME_TEMPLATE.format(file_name=file_name)

    def get_simplified_graph(self):
        self.get_map_data()
        extract_and_write_to_file(self.osm_file, self.extracted_graph)
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
