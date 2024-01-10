import os
from pathlib import Path

import pytest

from src.constants import MapPoint
from src.map_downloader import DataDownloader
from src.route_api import get_area_boundaries
from test.test_constants import TEST_END_POINT_LONG_LAT, TEST_END_POINT_LONG_LON, TEST_INIT_POINT_LAT, \
    TEST_INIT_POINT_LON

TEST_VILLAGE = "Taurinya"
TEST_EXTRACTED_GRAPH = f"{TEST_VILLAGE}-extracted.graph"


@pytest.fixture()
def rm_graph_file():
    try:
        Path(TEST_EXTRACTED_GRAPH).unlink()
    except FileNotFoundError:
        pass


@pytest.fixture()
def data_downloader(rm_graph_file):
    area_boundaries = get_area_boundaries(MapPoint(TEST_END_POINT_LONG_LAT, TEST_END_POINT_LONG_LON),
                                          MapPoint(TEST_INIT_POINT_LAT, TEST_INIT_POINT_LON))
    return DataDownloader(TEST_VILLAGE, area_boundaries)


def test_data_download_good(data_downloader):
    assert data_downloader.get_simplified_graph()
    assert os.path.isfile(TEST_EXTRACTED_GRAPH)
    assert os.path.getsize(TEST_EXTRACTED_GRAPH) > 0
