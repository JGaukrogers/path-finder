DEFAULT_OPHOIS = './bin/ophois'

SIMPLE_GRAPH_FILENAME_TEMPLATE = '{}-simplified.graph'
EXTRACTED_GRAPH_FILENAME_TEMPLATE = '{}-extracted.graph'
OSM_FILENAME_TEMPLATE = '{}.osm'

COMMAND_DOWNLOAD_CITY = '{ophois_path} download --city {area_name}'
COMMAND_EXTRACT_GRAPH = 'cat {osm_file} | {ophois_path} format | {ophois_path} extract > {extracted_graph}'
COMMAND_SIMPLIFY_GRAPH = 'cat {extracted_graph} | {ophois_path} simplify --delta 10.0 > {simplified_graph}'
COMMAND_REMOVE_FILES = 'rm {extracted_graph}'
COMMAND_OPHOIS_AVAILABLE = '{ophois_path} --help'

HTML_OUTFILE = '{area_name}.html'
HTML_OUTPATH = 'src/templates/{area_name}.html'

PRIORITY_QUIETNESS = 'quietness'
PRIORITY_SHORT_DISTANCE = 'distance'