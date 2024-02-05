import os
from pathlib import Path

import pytest

from src.constants import MapPoint, EXTRACTED_GRAPH_FILENAME_TEMPLATE
from src.data_downloader import DataDownloader
from src.route_api import get_area_boundaries
from test.test_constants import TEST_END_POINT_LONG_LAT, TEST_END_POINT_LONG_LON, \
    TEST_INIT_POINT_LAT, TEST_INIT_POINT_LON, TEST_VILLAGE

TEST_EXTRACTED_GRAPH = EXTRACTED_GRAPH_FILENAME_TEMPLATE.format(file_name=TEST_VILLAGE)


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
    assert data_downloader.download_data_and_extract()
    assert os.path.isfile(TEST_EXTRACTED_GRAPH)
    assert os.path.getsize(TEST_EXTRACTED_GRAPH) > 0
