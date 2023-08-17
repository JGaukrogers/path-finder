DEFAULT_OPHOIS = './bin/ophois'

SIMPLE_GRAPH_FILENAME_TEMPLATE = '{file_name}-simplified.graph'
EXTRACTED_GRAPH_FILENAME_TEMPLATE = '{file_name}-extracted.graph'
OSM_FILENAME_TEMPLATE = '{file_name}.osm'

COMMAND_DOWNLOAD_CITY = \
    'wget "https://overpass-api.de/api/interpreter?data=[out:json]; way({s},{w},{n},{e})[highway]; (._;>;); out body;"'\
    + ' --output-document={file_name}.osm'
# COMMAND_EXTRACT_GRAPH = 'cat {osm_file} | {ophois_path} format | {ophois_path} extract > {extracted_graph}'
COMMAND_SIMPLIFY_GRAPH = 'cat {extracted_graph} | {ophois_path} simplify --delta 10.0 > {simplified_graph}'
COMMAND_REMOVE_FILES = 'rm {extracted_graph}'
COMMAND_OPHOIS_AVAILABLE = '{ophois_path} --help'

HTML_OUTFILE = '{file_name}.html'
HTML_OUTPATH = 'src/templates/{file_name}.html'

PRIORITY_QUIETNESS = 'quietness'
PRIORITY_SHORT_DISTANCE = 'distance'
