from os import getcwd
import pytest

from src.map_parser import MapParser

NODE_2 = '6845757796'

NODE_1 = '6845757797'

TEST_DICT = {NODE_1: [], NODE_2: []}

resources_dir = getcwd() + '/../resources'
map_file_path = resources_dir + '/my_town.osm'


@pytest.fixture()
def parser():
    parser = MapParser(map_file_path)
    return parser


def test_parse_dom(parser):
    parser.parse_dom(TEST_DICT)
    assert len(TEST_DICT[NODE_1]) == 1
    assert len(TEST_DICT[NODE_2]) == 2
