from os import getcwd
from dijkstra import DijkstraSPF

import folium

# from folium.plugins import MarkerCluster
# import pandas as pd
from src.graph_parser import GraphParser

resources_dir = getcwd() + '/../resources'
MOCK_GRAPH_FILE = resources_dir + '/ophois-graph.txt'
MOCK_MAP_FILE = resources_dir + '/my_town.osm'


def get_quietest_way(start_node_id: str, end_node_id: str):
    graph_parser = GraphParser(MOCK_GRAPH_FILE, MOCK_MAP_FILE)
    weighed_graph = graph_parser.parse_simplified_map_to_graph()
    dijkstra = DijkstraSPF(weighed_graph, start_node_id)
    # Print list of nodes in "lightest" way
    print(dijkstra.get_path(end_node_id))

    start_node_info = graph_parser.nodeId_to_nodeInfo_dict[start_node_id]
    lat = start_node_info.lat
    lon = start_node_info.lon

    start_node_coords = [float(lat), float(lon)]

    map = folium.Map(location=start_node_coords, zoom_start=17)

    start_node_info = graph_parser.nodeId_to_nodeInfo_dict[end_node_id]
    lat = start_node_info.lat
    lon = start_node_info.lon
    end_node_coords = [lat, lon]

    trail_coordinates = [
        (start_node_coords[0], start_node_coords[1]),
        (end_node_coords[0], end_node_coords[1]),
    ]

    folium.PolyLine(trail_coordinates, tooltip="Coast").add_to(map)

    folium.Marker(start_node_coords, popup='Start').add_to(map)
    folium.Marker(end_node_coords, popup='End').add_to(map)

    map.save("index.html")


'''
lat="41.7889938"
lon="0.8188493"

#Define coordinates of where we want to center our map

boulder_coords = [float(lat), float(lon)]

#Create the map
my_map = folium.Map(location = boulder_coords, zoom_start = 17)

#Define the coordinates we want our markers to be at
node_id_6845757796 = [41.7889938, 0.8188493]
node_id_6845757797 = [41.7885559, 0.8201536]


#Add markers to the map
folium.Marker(node_id_6845757796, popup = '6845757796').add_to(my_map)
folium.Marker(node_id_6845757797, popup = '6845757797').add_to(my_map)

# Add ways
trail_coordinates = [
    (node_id_6845757796[0], node_id_6845757796[1]),
    (node_id_6845757797[0], node_id_6845757797[1]),
]

folium.PolyLine(trail_coordinates, tooltip="Coast").add_to(my_map)

#Display the map
# my_map

# Save the map
my_map.save("index.html")
'''

TEST_INIT_POINT = '6845757797'
TEST_END_POINT_SHORT = '6845757796'
get_quietest_way(TEST_INIT_POINT, TEST_END_POINT_SHORT)