from haversine import Unit, haversine

from src.constants import PRIORITY_QUIETNESS, PRIORITY_SHORT_DISTANCE


class WeightCalculator:

    def __init__(self, path_way_priority, nodeId_to_nodeInfo_dict):
        self.path_way_priority = path_way_priority
        self.nodeId_to_nodeInfo_dict = nodeId_to_nodeInfo_dict

    def get_weight(self, node_id_0: str, node_id_1: str) -> float:
        ways_n0 = self.get_ways_for_nodes(node_id_0)
        ways_n1 = self.get_ways_for_nodes(node_id_1)
        # len(common_ways) can be > 1 if two or more ways are parallel to each other between two nodes.
        # For example, we have a road and a park way
        common_ways = ways_n0 & ways_n1
        weight = 1
        if self.path_way_priority == PRIORITY_QUIETNESS:
            # Is sum a good idea? Better min?
            weight = sum(way.get_quietness_value() for way in common_ways)
        elif self.path_way_priority == PRIORITY_SHORT_DISTANCE:
            weight = self.get_distance_for_nodes(node_id_0, node_id_1)
        return weight

    def get_ways_for_nodes(self, node_id: str) -> set:
        ways = set()
        ways.update(self.nodeId_to_nodeInfo_dict[node_id].ways)
        return ways

    def get_distance_for_nodes(self, node_id_0, node_id_1) -> float:
        node_0 = self.nodeId_to_nodeInfo_dict[node_id_0]
        node_1 = self.nodeId_to_nodeInfo_dict[node_id_1]

        coordinates_0 = (node_0.lat, node_0.lon)
        coordinates_1 = (node_1.lat, node_1.lon)

        return haversine(coordinates_0, coordinates_1, unit=Unit.METERS)
