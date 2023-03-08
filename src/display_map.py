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


TEST_INIT_POINT = '6845757797'
TEST_END_POINT_SHORT = '6845757796'
get_quietest_way(TEST_INIT_POINT, TEST_END_POINT_SHORT)