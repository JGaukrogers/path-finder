from pathlib import Path
import pytest

from src.graph_elements import NodeInfo
from src.map_parser import MapParser
from test.test_constants import TEST_END_POINT_SHORT_ID, TEST_INIT_POINT_ID

TEST_DICT = {TEST_INIT_POINT_ID: NodeInfo(), TEST_END_POINT_SHORT_ID: NodeInfo()}

resources_dir = Path(".") / 'resources'
map_file_path = str(resources_dir / 'my_town.osm')


@pytest.fixture()
def parser():
    parser = MapParser(map_file_path)
    return parser


def test_parse_osm_map(parser):
    print(resources_dir)
    print(map_file_path)
    parser.parse_osm_map_json(TEST_DICT)
    assert len(TEST_DICT[TEST_INIT_POINT_ID].ways) == 1
    assert len(TEST_DICT[TEST_END_POINT_SHORT_ID].ways) == 2
