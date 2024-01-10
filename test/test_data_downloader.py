import os
from pathlib import Path

import pytest
from sys import platform

from src.constants import MapPoint
from src.map_downloader import DataDownloader
from src.route_api import get_area_boundaries
from test.test_constants import TEST_END_POINT_LONG_LAT, TEST_END_POINT_LONG_LON, TEST_INIT_POINT_LAT, \
    TEST_INIT_POINT_LON

TEST_VILLAGE = "Taurinya"
TEST_SIMPLIFIED_GRAPH = f"{TEST_VILLAGE}-extracted.graph"

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
    area_boundaries = get_area_boundaries(MapPoint(TEST_END_POINT_LONG_LAT, TEST_END_POINT_LONG_LON),
                                          MapPoint(TEST_INIT_POINT_LAT, TEST_INIT_POINT_LON))
    return DataDownloader(TEST_VILLAGE, area_boundaries, ophois=run_ophois_cmd_good)


@pytest.fixture()
def data_downloader_bad(rm_graph_file):
    area_boundaries = get_area_boundaries(MapPoint(TEST_END_POINT_LONG_LAT, TEST_END_POINT_LONG_LON),
                                                   MapPoint(TEST_INIT_POINT_LAT, TEST_INIT_POINT_LON))
    return DataDownloader(TEST_VILLAGE, area_boundaries, ophois=run_ophois_cmd_bad)


def _is_linux():
    return platform.startswith("linux")


@pytest.mark.skipif(not _is_linux(), reason="Only run on Linux")
def test_data_download_good(data_downloader):
    assert data_downloader.get_simplified_graph()
    assert os.path.isfile(TEST_SIMPLIFIED_GRAPH)
    assert os.path.getsize(TEST_SIMPLIFIED_GRAPH) > 0


@pytest.mark.skip('Soon ophois not needed')
def test_ophois_not_available(data_downloader_bad):
    assert not data_downloader_bad.get_simplified_graph()
    assert not os.path.exists(TEST_SIMPLIFIED_GRAPH)
