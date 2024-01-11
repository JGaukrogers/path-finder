import requests

from src.constants import OSM_FILENAME_TEMPLATE, EXTRACTED_GRAPH_FILENAME_TEMPLATE, OVERPASS_QUERY, OVERPASS_URL
from src.format import extract_and_write_to_file


class DataDownloader:

    def __init__(self, file_name: str, area_boundaries: dict):
        self.area_boundaries = area_boundaries
        self.osm_file = OSM_FILENAME_TEMPLATE.format(file_name=file_name)
        self.extracted_graph = EXTRACTED_GRAPH_FILENAME_TEMPLATE.format(file_name=file_name)

    def get_simplified_graph(self) -> bool:
        if self.get_map_data():
            extract_and_write_to_file(self.osm_file, self.extracted_graph)
            return True
        return False

    def get_map_data(self) -> bool:
        overpass_query = OVERPASS_QUERY.format(n=self.area_boundaries['north'],
                                               s=self.area_boundaries['south'],
                                               e=self.area_boundaries['east'],
                                               w=self.area_boundaries['west'])
        try:
            response = requests.get(OVERPASS_URL, params={'data': overpass_query})
        except requests.RequestException | requests.ConnectionError | requests.HTTPError | requests.Timeout:
            return False
        with open(self.osm_file, 'w') as fd:
            fd.write(response.text)
        return True
