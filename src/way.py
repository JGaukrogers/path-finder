import xml.dom.minidom


class Way:
    def __init__(self, xml_way: xml.dom.minidom.Element):
        tags = xml_way.getElementsByTagName('tag')
        self.properties_dict = dict()
        for tag in tags:
            self.properties_dict[tag.attributes['k'].value] = tag.attributes['v'].value
