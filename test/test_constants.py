import json
from pathlib import Path

resources_dir = Path(".") / 'resources'
MOCK_GRAPH_FILE = str(resources_dir / 'extracted-graph.txt')
MOCK_MAP_FILE = str(resources_dir / 'my_town.osm')
with open(MOCK_MAP_FILE) as fd:
    MOCK_MAP_CONTENT = json.load(fd)
with open(MOCK_GRAPH_FILE) as fd:
    MOCK_GRAPH_CONTENT = fd.read()

TEST_INIT_POINT_ID = '6845757797'
TEST_END_POINT_SHORT_ID = '6845757796'
TEST_END_POINT_LONG_ID = '1238435933'

TEST_INIT_POINT_LAT = 41.7885559
TEST_INIT_POINT_LON = 0.8201536

TEST_END_POINT_SHORT_LAT = 41.7889938
TEST_END_POINT_SHORT_LON = 0.8188493

TEST_END_POINT_LONG_LAT = 41.7903654
TEST_END_POINT_LONG_LON = 0.8180353
