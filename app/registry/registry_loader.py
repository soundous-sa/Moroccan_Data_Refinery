from app.registry.registry import Registry
from app.connectors.hcp.connector import HCPConnector


class RegistryLoader:

    @staticmethod
    def load():

        registry = Registry()

        registry.register(
            HCPConnector()
        )

        return registry