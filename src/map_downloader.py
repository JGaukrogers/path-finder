import subprocess
import src.constants as constants
from src.format import extract_and_write_to_file


class DataDownloader:

    def __init__(self, file_name: str, area_boundaries: dict, ophois: str=constants.DEFAULT_OPHOIS):
        self.file_name = file_name
        self.area_boundaries = area_boundaries
        self.ophois = ophois
        self.osm_file = constants.OSM_FILENAME_TEMPLATE.format(file_name=file_name)
        self.extracted_graph = constants.EXTRACTED_GRAPH_FILENAME_TEMPLATE.format(file_name=file_name)
        self.simplified_graph = constants.SIMPLE_GRAPH_FILENAME_TEMPLATE.format(file_name=file_name)

    def get_simplified_graph(self):
        if self.is_ophois_available():
            subprocess.check_output(
                constants.COMMAND_DOWNLOAD_CITY.format(file_name=self.file_name,
                                                       n=self.area_boundaries['north'],
                                                       s=self.area_boundaries['south'],
                                                       e=self.area_boundaries['east'],
                                                       w=self.area_boundaries['west']),
                shell=True)
            extract_and_write_to_file(self.osm_file, self.extracted_graph)
            subprocess.check_output(
                constants.COMMAND_SIMPLIFY_GRAPH.format(extracted_graph=self.extracted_graph, ophois_path=self.ophois,
                                                        simplified_graph=self.simplified_graph), shell=True)
            subprocess.check_output(constants.COMMAND_REMOVE_FILES.format(extracted_graph=self.extracted_graph), shell=True)

        else:
            return False
        return True

    def is_ophois_available(self):
        try:
            res = subprocess.check_output(constants.COMMAND_OPHOIS_AVAILABLE.format(ophois_path=self.ophois), shell=True)
            # print('Decoded string: ', res.decode('utf-8'))
        except subprocess.CalledProcessError:
            return False
        return True
