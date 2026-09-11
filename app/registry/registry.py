from app.registry.registry_validator import RegistryValidator


class Registry:

    def __init__(self):

        self._connectors = []

    def register(self, connector):

        RegistryValidator.validate(connector)

        self._connectors.append(connector)

    def get_connectors(self):

        return self._connectors

    def get(self, connector_id):

        for connector in self._connectors:

            if connector.get_id() == connector_id:

                return connector

        return None

    def count(self):

        return len(self._connectors)

    def clear(self):

        self._connectors.clear()