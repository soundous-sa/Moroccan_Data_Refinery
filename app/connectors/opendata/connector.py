from app.connectors.base.base_connector import BaseConnector


class OpenDataConnector(BaseConnector):

    def get_id(self) -> str:

        return "opendata"

    def get_name(self) -> str:

        return "Portail National des Données Ouvertes"

    def get_base_url(self) -> str:

        return "https://data.gov.ma"

    def get_allowed_formats(self) -> list[str]:

        return [
            "csv",
            "json",
            "xlsx",
            "xls",
            "html"
        ]

    def get_update_frequency(self) -> int:

        return 15

    def is_enabled(self) -> bool:

        return True

    def get_sectors(self) -> list[str]:

        return [
            "agriculture",
            "sante",
            "education",
            "economie",
            "environnement",
            "administration"
        ]

    def get_metadata(self) -> dict:

        metadata = super().get_metadata()

        metadata["sectors"] = self.get_sectors()

        metadata["enabled"] = self.is_enabled()

        return metadata
