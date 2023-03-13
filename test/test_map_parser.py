from pathlib import Path
import pytest

from src.graph_elements import NodeInfo
from src.map_parser import MapParser

NODE_2 = '6845757796'

NODE_1 = '6845757797'

TEST_DICT = {NODE_1: NodeInfo(), NODE_2: NodeInfo()}

resources_dir = Path(".") / 'resources'
map_file_path = str(resources_dir / 'my_town.osm')


@pytest.fixture()
def parser():
    parser = MapParser(map_file_path)
    return parser


def test_parse_dom(parser):
    parser.parse_osm_map(TEST_DICT)
    assert len(TEST_DICT[NODE_1].ways) == 1
    assert len(TEST_DICT[NODE_2].ways) == 2
