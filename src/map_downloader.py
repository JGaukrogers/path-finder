import subprocess

class DataDownloader:
    OPHOIS = './../bin/ophois'

    # osm_file = f'{city}.osm'
    # extracted_graph = f'{city}-extracted.graph'

    # COMMAND_DOWNLOAD_CITY = f'{OPHOIS} download --city {city}'
    # COMMAND_EXTRACT_GRAPH = f'cat {osm_file} | {OPHOIS} format | {OPHOIS} extract > {extracted_graph}'
    # COMMAND_SIMPLIFY_GRAPH = f'cat extracted_graph | {OPHOIS} simplify --delta 10.0 > {city}-simplified.graph'
    #
    # COMMAND_REMOVE_FILES = f'rm {osm_file} {extracted_graph}'

    def __init__(self, city):
        self.city = city
        self.osm_file = f'{self.city}.osm'
        self.extracted_graph = f'{self.city}-extracted.graph'
        self.COMMAND_DOWNLOAD_CITY = f'{self.OPHOIS} download --city {self.city}'
        self.COMMAND_EXTRACT_GRAPH = f'cat {self.osm_file} | {self.OPHOIS} format | {self.OPHOIS} extract > {self.extracted_graph}'
        self.COMMAND_SIMPLIFY_GRAPH = f'cat {self.extracted_graph} | {self.OPHOIS} simplify --delta 10.0 > {self.city}-simplified.graph'

        self.COMMAND_REMOVE_FILES = f'rm {self.osm_file} {self.extracted_graph}'

    def get_simplified_graph(self):

        res0 = subprocess.check_output(self.COMMAND_DOWNLOAD_CITY, shell=True)
        res1 = subprocess.check_output(self.COMMAND_EXTRACT_GRAPH, shell=True)
        res2 = subprocess.check_output(self.COMMAND_SIMPLIFY_GRAPH, shell=True)
        res3 = subprocess.check_output(self.COMMAND_REMOVE_FILES, shell=True)

        print('Decoded string: ', res0.decode('utf-8'))
        print('Decoded string: ', res1.decode('utf-8'))
        print('Decoded string: ', res2.decode('utf-8'))
        print('Decoded string: ', res3.decode('utf-8'))


test_city = 'Taurinya'
data_downloader = DataDownloader(test_city)
data_downloader.get_simplified_graph()