from pathlib import Path

from app.loaders.yaml_loader import YamlLoader


class SourceLoader:

    CONFIG_PATH = Path("app/config/sources")

    @classmethod
    def load_sources(cls):

        sources = []

        for file in cls.CONFIG_PATH.glob("*.yaml"):

            config = YamlLoader.load(file)

            sources.append(config)

        return sources