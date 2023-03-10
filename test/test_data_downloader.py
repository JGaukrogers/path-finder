import subprocess

import pytest
import os

from src.map_downloader import DataDownloader

TEST_VILLAGE = 'Taurinya'
TEST_SIMPLIFIED_GRAPH = f'{TEST_VILLAGE}-simplified.graph'
run_ophois_cmd_good = os.getcwd() + './../bin/ophois'
run_ophois_cmd_bad = os.getcwd() + './ophoisAAAA'


@pytest.fixture()
def data_downloader():
    data_downloader = DataDownloader(TEST_VILLAGE, run_ophois_cmd_good)
    return data_downloader


def remove_test_graph_file():
    if os.path.exists(TEST_SIMPLIFIED_GRAPH):
        subprocess.check_output(f'rm {TEST_SIMPLIFIED_GRAPH}', shell=True)


def test_data_download_good(data_downloader):
    data_downloader = DataDownloader(TEST_VILLAGE)
    remove_test_graph_file()
    data_downloader.get_simplified_graph()
    assert os.path.isfile(TEST_SIMPLIFIED_GRAPH)
    assert os.path.getsize(TEST_SIMPLIFIED_GRAPH) > 0


def test_ophois_not_available():
    data_downloader = DataDownloader(TEST_VILLAGE, run_ophois_cmd_bad)
    remove_test_graph_file()
    assert not data_downloader.get_simplified_graph()
    assert not os.path.exists(TEST_SIMPLIFIED_GRAPH)
