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

    def get_trail_coordinates(self, node_list) -> list[tuple[float, float]]:
        trail_coordinates = []
        for path_points in node_list:
            lat = self.graph_parser.nodeId_to_nodeInfo_dict[path_points].lat
            lon = self.graph_parser.nodeId_to_nodeInfo_dict[path_points].lon
            trail_coordinates.append((lat, lon))
        return trail_coordinates

    def display_downloaded_data(self, start_node_coords, out_file: str):
        map = folium.Map(location=start_node_coords, zoom_start=ZOOM_START)

        trail_coordinates = [(node_id,
                              (self.graph_parser.nodeId_to_nodeInfo_dict[node_id].lat,
                              self.graph_parser.nodeId_to_nodeInfo_dict[node_id].lon,))
                             for node_id in self.graph_parser.nodeId_to_nodeInfo_dict]

        for node_id, coordinate in trail_coordinates:
            folium.vector_layers.Circle(coordinate, radius=1, color='#ff0000', fill=True,
                                        popup=f'{node_id}: {coordinate[0]}, {coordinate[1]}')\
                .add_to(map)

        map.save(out_file)
