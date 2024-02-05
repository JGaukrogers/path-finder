import os
from collections import namedtuple
from dotenv import load_dotenv
from pathlib import Path

MapPoint = namedtuple('MapPoint', 'lat lon')
AreaBoundaries = namedtuple('AreaBoundaries', 'north south east west')
RADIUS_EARTH = 6378 #km
EXTRA_AREA_DISTANCE_IN_KM = 0.5

OVERPASS_URL = 'https://overpass-api.de/api/interpreter'
OVERPASS_QUERY = '''
[out:json];
way({s},{w},{n},{e})[highway];
(._;>;);
out body;
'''

dotenv_path = Path('.env')
load_dotenv(dotenv_path=dotenv_path)
DOWNLOADS_HOME = Path(os.environ['PF_HOME']) / 'downloads/'
TEMPLATES_HOME = Path(os.environ['PF_HOME']) / 'src/templates/'

EXTRACTED_GRAPH_FILENAME_TEMPLATE = str(DOWNLOADS_HOME / '{file_name}-extracted.graph')
OSM_FILENAME_TEMPLATE = str(DOWNLOADS_HOME / '{file_name}.osm')
HTML_OUTFILE = '{file_name}.html'
HTML_OUTPATH = str(TEMPLATES_HOME / '{file_name}.html')

PRIORITY_QUIETNESS = 'quietness'
PRIORITY_SHORT_DISTANCE = 'distance'
