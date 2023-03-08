from src.way import Way


class NodeInfo:
    def __init__(self):
        self.ways = set()
        self.lat = None
        self.lon = None

    def get_connected_ways(self):
        return self.ways

    def add_way(self, way: Way):
        self.ways.add(way)