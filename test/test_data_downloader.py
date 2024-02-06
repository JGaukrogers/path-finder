import pytest

from src.constants import MapPoint
from src.data_downloader import DataDownloader
from src.route_api import get_area_boundaries
from test.test_constants import TEST_END_POINT_LONG_LAT, TEST_END_POINT_LONG_LON, \
    TEST_INIT_POINT_LAT, TEST_INIT_POINT_LON


@pytest.fixture()
def data_downloader():
    area_boundaries = get_area_boundaries(MapPoint(TEST_END_POINT_LONG_LAT, TEST_END_POINT_LONG_LON),
                                          MapPoint(TEST_INIT_POINT_LAT, TEST_INIT_POINT_LON))
    return DataDownloader(area_boundaries)


def test_data_download_good(data_downloader):
    assert data_downloader.download_data_and_extract()
    assert data_downloader.osm_data
    assert data_downloader.extracted_graph
