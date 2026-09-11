from app.connectors.base.base_connector import BaseConnector


class RegistryValidator:

    @staticmethod
    def validate(connector):

        if not isinstance(connector, BaseConnector):

            raise TypeError(
                "Le connecteur doit hériter de BaseConnector."
            )

        if not connector.get_id():

            raise ValueError(
                "Le connecteur doit avoir un identifiant."
            )

        if not connector.get_name():

            raise ValueError(
                "Le connecteur doit avoir un nom."
            )

        if not connector.get_base_url():

            raise ValueError(
                "Le connecteur doit avoir une URL."
            )

        if not connector.get_allowed_formats():

            raise ValueError(
                "Le connecteur doit définir ses formats."
            )