import yaml


class YAMLParser:
    def parse(self, yaml_data):
        return yaml.safe_load(yaml_data)
