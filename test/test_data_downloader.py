import subprocess
from pathlib import Path
from sys import platform

import pytest
import os

from src.map_downloader import DataDownloader

TEST_VILLAGE = "Taurinya"
TEST_SIMPLIFIED_GRAPH = f"{TEST_VILLAGE}-simplified.graph"

run_ophois_cmd_good = "./bin/ophois"
run_ophois_cmd_bad = "./ophoisAAAA"


@pytest.fixture()
def rm_graph_file():
    try:
        Path(TEST_SIMPLIFIED_GRAPH).unlink()
    except FileNotFoundError:
        pass


@pytest.fixture()
def data_downloader(rm_graph_file):
    return DataDownloader(TEST_VILLAGE, ophois=run_ophois_cmd_good)


@pytest.fixture()
def data_downloader_bad(rm_graph_file):
    return DataDownloader(TEST_VILLAGE, ophois=run_ophois_cmd_bad)


def _is_linux():
    return platform.startswith("linux")


@pytest.mark.skipif(not _is_linux(), reason="Only run on Linux")
def test_data_download_good(data_downloader):
    assert data_downloader.get_simplified_graph()
    assert os.path.isfile(TEST_SIMPLIFIED_GRAPH)
    assert os.path.getsize(TEST_SIMPLIFIED_GRAPH) > 0


def test_ophois_not_available(data_downloader_bad):
    assert not data_downloader_bad.get_simplified_graph()
    assert not os.path.exists(TEST_SIMPLIFIED_GRAPH)
