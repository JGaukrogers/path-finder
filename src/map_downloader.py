import subprocess
import src.constants as constants


class DataDownloader:

    def __init__(self, city, ophois=constants.DEFAULT_OPHOIS):
        self.city = city
        self.ophois = ophois
        self.osm_file = constants.OSM_FILENAME_TEMPLATE.format(self.city)
        self.extracted_graph = constants.EXTRACTED_GRAPH_FILENAME_TEMPLATE.format(self.city)
        self.simplified_graph = constants.SIMPLE_GRAPH_FILENAME_TEMPLATE.format(self.city)

    def get_simplified_graph(self):
        if self.is_ophois_available():
            subprocess.check_output(
                constants.COMMAND_DOWNLOAD_CITY.format(ophois_path=self.ophois, area_name=self.city), shell=True)
            subprocess.check_output(
                constants.COMMAND_EXTRACT_GRAPH.format(osm_file=self.osm_file, ophois_path=self.ophois,
                                                       extracted_graph=self.extracted_graph), shell=True)
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
            print('Decoded string: ', res.decode('utf-8'))
        except subprocess.CalledProcessError:
            return False
        return True
