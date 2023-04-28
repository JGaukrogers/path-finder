import xml.dom.minidom
from dataclasses import dataclass, field

highway_types = {'motorway': 10,  # Autobahn. Including it as reference for the noisiest highway type.
                 'primary': 8,
                 'secondary': 9,
                 'tertiary': 6,
                 'unclassified': 1,
                 'residential': 3,

                 'living_street': 2,
                 'pedestrian': 3,
                 'track': 1,
                 'road': 5,  # Unknown type of road

                 'footway': 1,
                 'bridleway': 1,
                 'steps': 3,  # Depends on where they are. Should maybe delete it
                 'path': 2,  # Unspecified path
                 'sidewalk': 3,
                 'crossing': 5,
                 }


class Way:
    def __init__(self, xml_way: xml.dom.minidom.Element):
        self.id = xml_way.getAttribute('id')
        self.properties_dict = dict()

        tags = xml_way.getElementsByTagName('tag')
        for tag in tags:
            self.properties_dict[tag.attributes['k'].value] = tag.attributes['v'].value

    def __eq__(self, other):
        if isinstance(other, Way):
            return self.id == other.id
        return False

    def __hash__(self):
        return hash(self.id)

    def get_quietness_value(self):
        highway_type = self.properties_dict['highway']
        return highway_types.get(highway_type, 10)


@dataclass
class NodeInfo:
    ways: set[Way] = field(default_factory=set)
    lat: float = 0
    lon: float = 0
