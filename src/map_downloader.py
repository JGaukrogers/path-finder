import subprocess

city = 'Taurinya'
OPHOIS = './../bin/ophois'

osm_file = f'{city}.osm'
extracted_graph = f'{city}-extracted.graph'

COMMAND_DOWNLOAD_CITY = f'{OPHOIS} download --city {city}'
COMMAND_EXTRACT_GRAPH = f'cat {osm_file} | {OPHOIS} format | {OPHOIS} extract > {extracted_graph}'
COMMAND_SIMPLIFY_GRAPH = f'cat extracted_graph | {OPHOIS} simplify --delta 10.0 > {city}-simplified.graph'

COMMAND_REMOVE_FILES = f'rm {osm_file} {extracted_graph}'

res0 = subprocess.check_output(COMMAND_DOWNLOAD_CITY, shell=True)
res1 = subprocess.check_output(COMMAND_EXTRACT_GRAPH, shell=True)
res2 = subprocess.check_output(COMMAND_SIMPLIFY_GRAPH, shell=True)

res3 = subprocess.check_output(COMMAND_REMOVE_FILES, shell=True)

print('Decoded string: ', res0.decode('utf-8'))
print('Decoded string: ', res1.decode('utf-8'))
print('Decoded string: ', res2.decode('utf-8'))

print('Decoded string: ', res3.decode('utf-8'))

