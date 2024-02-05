import json

import requests

from src.constants import EXTRACTED_GRAPH_FILENAME_TEMPLATE, \
    OVERPASS_QUERY, OVERPASS_URL, \
    AreaBoundaries
from src.format import extract_and_write_to_file


class DataDownloader:

    def __init__(self, file_name: str, area_boundaries: AreaBoundaries):
        self.area_boundaries = area_boundaries
        self.osm_data = None
        self.extracted_graph = EXTRACTED_GRAPH_FILENAME_TEMPLATE.format(file_name=file_name)

    def download_graph_and_extract(self) -> bool:
        self.osm_data = self.download_map_data()
        self.osm_data = json.loads(self.osm_data)
        if self.osm_data:
            extract_and_write_to_file(self.osm_data, self.extracted_graph)
            return True
        return False

    def download_map_data(self) -> str | bool:
        overpass_query = OVERPASS_QUERY.format(n=self.area_boundaries.north,
                                               s=self.area_boundaries.south,
                                               e=self.area_boundaries.east,
                                               w=self.area_boundaries.west)
        try:
            response = requests.get(OVERPASS_URL, params={'data': overpass_query})
        except requests.RequestException | requests.ConnectionError | requests.HTTPError | requests.Timeout:
            return False
        osm_map_data = response.text
        return osm_map_data
