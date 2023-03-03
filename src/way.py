import xml.dom.minidom

highway_types = {'motorway': 10,    #Autobahn. Should't prabably include it
                 'primary': 9,
                 'secondary': 8,
                 'tertiary': 7,
                 'unclassified': 1,
                 'residential': 3,

                 'living_street': 2,
                 'pedestrian': 3,
                 'track': 1,
                 'road': 5,         # Unkown type of road

                 'footway': 1,
                 'bridleway': 1,
                 'steps': 3,        # Depends on where they are. Should maybe delete it
                 'path': 2,         # Unspecifyed path
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
        quietness = 10
        highway_type = self.properties_dict['highway']
        if highway_type in highway_types:
            quietness = highway_types[highway_type]
        return quietness
