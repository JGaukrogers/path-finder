from collections import namedtuple

DEFAULT_HTML_OUTFILE = 'index.html'
ZOOM_START = 17

SEPARATOR = '␟'

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

HTML_OUTFILE = '{file_name}.html'
HTML_OUTPATH = 'src/templates/{file_name}.html'

PRIORITY_QUIETNESS = 'quietness'
PRIORITY_SHORT_DISTANCE = 'distance'
