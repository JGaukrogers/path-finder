from haversine import Unit, haversine

from src.constants import PRIORITY_QUIETNESS, PRIORITY_SHORT_DISTANCE, RADIUS_LAT, RADIUS_LON
from src.graph_elements import NodeInfo


class WeightCalculator:

    def __init__(self, path_way_priority: str, nodeId_to_nodeInfo_dict: dict[str, NodeInfo]):
        self.path_way_priority = path_way_priority
        self.nodeId_to_nodeInfo_dict = nodeId_to_nodeInfo_dict
        self.nodes_ordered_by_lat = [(node_id,
                                      nodeId_to_nodeInfo_dict[node_id].lat, nodeId_to_nodeInfo_dict[node_id].lon)
                                     for node_id in nodeId_to_nodeInfo_dict]
        self.nodes_ordered_by_lat.sort(key=lambda coord: coord[1])

    def get_weight(self, node_id_0: str, node_id_1: str) -> float:
        weight = 1
        if self.path_way_priority == PRIORITY_QUIETNESS:
            ways_n0 = self.get_ways_for_nodes(self.get_nearby_nodes(node_id_0))
            ways_n1 = self.get_ways_for_nodes(self.get_nearby_nodes(node_id_1))
            # len(common_ways) can be > 1 if two or more ways are parallel to each other between two nodes.
            # For example, we have a road and a park way
            common_ways = ways_n0 & ways_n1
            weight = sum(way.get_quietness_value() for way in common_ways) \
                     + (0.1 * self.get_distance_for_nodes(node_id_0, node_id_1))
        elif self.path_way_priority == PRIORITY_SHORT_DISTANCE:
            weight = self.get_distance_for_nodes(node_id_0, node_id_1)
        return weight

    def get_ways_for_nodes(self, node_ids: set[str]) -> set:
        ways = set()
        for node_id in node_ids:
            ways.update(self.nodeId_to_nodeInfo_dict[node_id].ways)
        return ways

    def get_distance_for_nodes(self, node_id_0: str, node_id_1: str) -> float:
        node_0 = self.nodeId_to_nodeInfo_dict[node_id_0]
        node_1 = self.nodeId_to_nodeInfo_dict[node_id_1]

        coordinates_0 = (node_0.lat, node_0.lon)
        coordinates_1 = (node_1.lat, node_1.lon)

        return haversine(coordinates_0, coordinates_1, unit=Unit.METERS)

    def get_nearby_nodes(self, node_id: str) -> set[str]:
        neighbours = set()
        lat_reference = self.nodeId_to_nodeInfo_dict[node_id].lat
        lon_reference = self.nodeId_to_nodeInfo_dict[node_id].lon

        for index in range(len(self.nodes_ordered_by_lat)):
            if self.nodes_ordered_by_lat[index][1] > lat_reference + RADIUS_LAT:
                break
            if self.nodes_ordered_by_lat[index][1] >= lat_reference - RADIUS_LAT \
                    and lon_reference - RADIUS_LON <= self.nodes_ordered_by_lat[index][2] <= lon_reference + RADIUS_LON:
                neighbours.add(self.nodes_ordered_by_lat[index][0])

        return neighbours
