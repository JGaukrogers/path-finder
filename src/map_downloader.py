import subprocess
import src.constants as constants
# DEFAULT_OPHOIS = './../bin/ophois'

COMMAND_DOWNLOAD_CITY = '{} download --city {}'
COMMAND_EXTRACT_GRAPH = 'cat {} | {} format | {} extract > {}'
COMMAND_SIMPLIFY_GRAPH = 'cat {} | {} simplify --delta 10.0 > {}'
COMMAND_REMOVE_FILES = 'rm {}'
COMMAND_OPHOIS_AVAILABLE = '{} --help'


class DataDownloader:

    def __init__(self, city, ophois=constants.DEFAULT_OPHOIS):
        self.city = city
        self.ophois = ophois
        self.osm_file = constants.OSM_FILENAME_TEMPLATE.format(self.city)
        self.extracted_graph = constants.EXTRACTED_GRAPH_FILENAME_TEMPLATE.format(self.city)
        self.simplified_graph = constants.SIMPLE_GRAPH_FILENAME_TEMPLATE.format(self.city)

    def get_simplified_graph(self):
        if self.is_ophois_available():
            subprocess.check_output(COMMAND_DOWNLOAD_CITY.format(self.ophois, self.city), shell=True)
            subprocess.check_output(COMMAND_EXTRACT_GRAPH.format(self.osm_file, self.ophois, self.ophois, self.extracted_graph), shell=True)
            subprocess.check_output(COMMAND_SIMPLIFY_GRAPH.format(self.extracted_graph, self.ophois, self.simplified_graph), shell=True)
            subprocess.check_output(COMMAND_REMOVE_FILES.format(self.extracted_graph), shell=True)

        else:
            return False
        return True

    def is_ophois_available(self):
        try:
            res = subprocess.check_output(COMMAND_OPHOIS_AVAILABLE.format(self.ophois), shell=True)
            print('Decoded string: ', res.decode('utf-8'))
        except subprocess.CalledProcessError:
            return False
        return True
