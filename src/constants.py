from collections import namedtuple

MapPoint = namedtuple('MapPoint', 'lat lon')

DEFAULT_OPHOIS = './bin/ophois'

EXTRACTED_GRAPH_FILENAME_TEMPLATE = '{file_name}-extracted.graph'
SIMPLE_GRAPH_FILENAME_TEMPLATE = EXTRACTED_GRAPH_FILENAME_TEMPLATE#'{file_name}-simplified.graph'
OSM_FILENAME_TEMPLATE = '{file_name}.osm'

OVERPASS_URL = 'https://overpass-api.de/api/interpreter'
OVERPASS_QUERY = '''
[out:json];
way({s},{w},{n},{e})[highway];
(._;>;);
out body;
'''
COMMAND_REMOVE_FILES = ''#'rm {extracted_graph}'
COMMAND_OPHOIS_AVAILABLE = '{ophois_path} --help'

HTML_OUTFILE = '{file_name}.html'
HTML_OUTPATH = 'src/templates/{file_name}.html'

PRIORITY_QUIETNESS = 'quietness'
PRIORITY_SHORT_DISTANCE = 'distance'
