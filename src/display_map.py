import folium
from dijkstra import DijkstraSPF

from src.graph_parser import GraphParser

DEFAULT_HTML_OUTFILE = 'index.html'

ZOOM_START = 17


class MapDisplayer:

    def __init__(self, graph_parser: GraphParser, dijkstra: DijkstraSPF):
        self.graph_parser = graph_parser
        self.dijkstra = dijkstra

    def get_quietest_way(self, start_node_id: str, end_node_id: str, outfile_path=DEFAULT_HTML_OUTFILE):
        start_node_coords = self.get_node_coordinates(start_node_id)
        end_node_coords = self.get_node_coordinates(end_node_id)

        map = folium.Map(location=start_node_coords, zoom_start=ZOOM_START)

        folium.Marker(start_node_coords, popup='Start').add_to(map)
        folium.Marker(end_node_coords, popup='End').add_to(map)

        nodes_group = self.graph_parser.nodeId_to_nodes_dict[end_node_id]
        trail_coordinates = self.get_trail_coordinates(self.dijkstra.get_path(nodes_group))

        folium.PolyLine(trail_coordinates, tooltip='Coast').add_to(map)

        map.save(outfile_path)

    def get_node_coordinates(self, start_node_id):
        start_node_info = self.graph_parser.nodeId_to_nodeInfo_dict[start_node_id]
        lat = start_node_info.lat
        lon = start_node_info.lon
        start_node_coords = [lat, lon]
        return start_node_coords

    def get_trail_coordinates(self, node_list):
        trail_coordinates = []
        for path_points in node_list:
            lat = self.graph_parser.nodeId_to_nodeInfo_dict[set(path_points).pop()].lat
            lon = self.graph_parser.nodeId_to_nodeInfo_dict[set(path_points).pop()].lon
            # TODO: make namedtuple
            trail_coordinates.append((lat, lon))
        return trail_coordinates
