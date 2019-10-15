from client.parser.XMLParser import XMLParser
from client.parser.YAMLParser import YAMLParser
from client.parser.CSVParser import CSVParser
from client.parser.JSONParser import JSONParser


class ParserFactory:
    @staticmethod
    def get_parser(parser_type):
        if parser_type == 'application/xml':
            return XMLParser()
        elif parser_type == 'application/x-yaml':
            return YAMLParser()
        elif parser_type == 'text/csv':
            return CSVParser()
        elif parser_type == 'json':
            return JSONParser()
