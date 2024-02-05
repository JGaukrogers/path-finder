import pytest

from src.graph_elements import NodeInfo
from src.map_parser import MapParser
from test.test_constants import TEST_END_POINT_SHORT_ID, TEST_INIT_POINT_ID, MOCK_MAP_CONTENT

TEST_DICT = {TEST_INIT_POINT_ID: NodeInfo(), TEST_END_POINT_SHORT_ID: NodeInfo()}


@pytest.fixture()
def parser():
    parser = MapParser(MOCK_MAP_CONTENT)
    return parser


def test_parse_osm_map(parser):
    parser.parse_osm_map_json(TEST_DICT)
    assert len(TEST_DICT[TEST_INIT_POINT_ID].ways) == 1
    assert len(TEST_DICT[TEST_END_POINT_SHORT_ID].ways) == 2
