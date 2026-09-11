import yaml
from pathlib import Path


class YamlLoader:

    @staticmethod
    def load(file_path):

        with open(file_path, "r", encoding="utf-8") as file:

            return yaml.safe_load(file)