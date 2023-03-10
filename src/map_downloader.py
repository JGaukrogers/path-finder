import subprocess

DEFAULT_OPHOIS = './../bin/ophois'


class DataDownloader:

    def __init__(self, city, ophois=DEFAULT_OPHOIS):
        self.city = city
        self.OPHOIS = ophois
        self.osm_file = f'{self.city}.osm'
        self.extracted_graph = f'{self.city}-extracted.graph'
        self.simplified_graph = f'{self.city}-simplified.graph'
        self.COMMAND_DOWNLOAD_CITY = f'{self.OPHOIS} download --city {self.city}'
        self.COMMAND_EXTRACT_GRAPH = f'cat {self.osm_file} | {self.OPHOIS} format | {self.OPHOIS} extract > {self.extracted_graph}'
        self.COMMAND_SIMPLIFY_GRAPH = f'cat {self.extracted_graph} | {self.OPHOIS} simplify --delta 10.0 > {self.simplified_graph}'
        self.COMMAND_REMOVE_FILES = f'rm {self.osm_file} {self.extracted_graph}'
        self.COMMAND_OPHOIS_AVAILABLE = f'{self.OPHOIS} --help'

    def get_simplified_graph(self):
        if self.is_ophois_available():
            res0 = subprocess.check_output(self.COMMAND_DOWNLOAD_CITY, shell=True)
            res1 = subprocess.check_output(self.COMMAND_EXTRACT_GRAPH, shell=True)
            res2 = subprocess.check_output(self.COMMAND_SIMPLIFY_GRAPH, shell=True)
            res3 = subprocess.check_output(self.COMMAND_REMOVE_FILES, shell=True)

            # print('Decoded string: ', res0.decode('utf-8'))
            # print('Decoded string: ', res1.decode('utf-8'))
            # print('Decoded string: ', res2.decode('utf-8'))
            # print('Decoded string: ', res3.decode('utf-8'))
        else:
            return False
        return True

    def is_ophois_available(self):
        try:
            res = subprocess.check_output(self.COMMAND_OPHOIS_AVAILABLE, shell=True)
            print('Decoded string: ', res.decode('utf-8'))
        except subprocess.CalledProcessError:
            return False
        return True
