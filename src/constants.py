from collections import namedtuple

MapPoint = namedtuple('MapPoint', 'lat lon')
EXTRA_AREA_DISTANCE_IN_KM = 3

OVERPASS_URL = 'https://overpass-api.de/api/interpreter'
OVERPASS_QUERY = '''
[out:json];
way({s},{w},{n},{e})[highway];
(._;>;);
out body;
'''

EXTRACTED_GRAPH_FILENAME_TEMPLATE = '{file_name}-extracted.graph'
OSM_FILENAME_TEMPLATE = '{file_name}.osm'
HTML_OUTFILE = '{file_name}.html'
HTML_OUTPATH = 'src/templates/{file_name}.html'

PRIORITY_QUIETNESS = 'quietness'
PRIORITY_SHORT_DISTANCE = 'distance'
