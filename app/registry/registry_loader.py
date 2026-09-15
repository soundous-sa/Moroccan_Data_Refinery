from app.registry.registry import Registry
from app.connectors.hcp.connector import HCPConnector
from app.connectors.bam.connector import BAMConnector
from app.connectors.ministry.connector import MinistryConnector
from app.connectors.opendata.connector import OpenDataConnector


class RegistryLoader:

    @staticmethod
    def load():

        registry = Registry()

        registry.register(
            HCPConnector()
        )

        registry.register(
            BAMConnector()
        )

        registry.register(
            MinistryConnector()
        )

        registry.register(
            OpenDataConnector()
        )

        return registry