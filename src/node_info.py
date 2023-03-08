from src.way import Way
from dataclasses import dataclass


@dataclass
class NodeInfo:
    ways: set[Way]
    lat: float
    lon: float
