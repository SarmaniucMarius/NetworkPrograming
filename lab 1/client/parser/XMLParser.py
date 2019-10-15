import xmltodict


class XMLParser:
    def parse(self, xml_data):
        data = xmltodict.parse(xml_data)
        return data["dataset"]["record"]
