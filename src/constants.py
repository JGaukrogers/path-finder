from collections import namedtuple

MapPoint = namedtuple('MapPoint', 'lat lon')

EXTRACTED_GRAPH_FILENAME_TEMPLATE = '{file_name}-extracted.graph'
OSM_FILENAME_TEMPLATE = '{file_name}.osm'

OVERPASS_URL = 'https://overpass-api.de/api/interpreter'
OVERPASS_QUERY = '''
[out:json];
way({s},{w},{n},{e})[highway];
(._;>;);
out body;
'''
COMMAND_REMOVE_FILES = ''#'rm {extracted_graph}'

HTML_OUTFILE = '{file_name}.html'
HTML_OUTPATH = 'src/templates/{file_name}.html'

PRIORITY_QUIETNESS = 'quietness'
PRIORITY_SHORT_DISTANCE = 'distance'
