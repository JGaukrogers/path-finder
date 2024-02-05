import folium
from dijkstra import DijkstraSPF

from src.constants import DEFAULT_HTML_OUTFILE, ZOOM_START
from src.graph_parser import GraphParser


class MapDisplayer:

    def __init__(self, graph_parser: GraphParser, dijkstra: DijkstraSPF):
        self.graph_parser = graph_parser
        self.dijkstra = dijkstra

    def generate_map(self, start_node_id: str, end_node_id: str, outfile_path=DEFAULT_HTML_OUTFILE):
        start_node_coords = self.get_node_coordinates(start_node_id)
        end_node_coords = self.get_node_coordinates(end_node_id)

        map = folium.Map(location=start_node_coords, zoom_start=ZOOM_START)

        folium.Marker(start_node_coords, popup='Start').add_to(map)
        folium.Marker(end_node_coords, popup='End').add_to(map)

        trail_coordinates = self.get_trail_coordinates(self.dijkstra.get_path(end_node_id))

        folium.PolyLine(trail_coordinates).add_to(map)

        map.save(outfile_path)

    def get_node_coordinates(self, node_id):
        start_node_info = self.graph_parser.nodeId_to_nodeInfo_dict[node_id]
        lat = start_node_info.lat
        lon = start_node_info.lon
        start_node_coords = [lat, lon]
        return start_node_coords

    def get_trail_coordinates(self, node_list):
        trail_coordinates = []
        for path_points in node_list:
            lat = self.graph_parser.nodeId_to_nodeInfo_dict[path_points].lat
            lon = self.graph_parser.nodeId_to_nodeInfo_dict[path_points].lon
            # TODO: make namedtuple
            trail_coordinates.append((lat, lon))
        return trail_coordinates
