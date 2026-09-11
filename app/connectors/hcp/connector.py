from app.connectors.base.base_connector import BaseConnector


class HCPConnector(BaseConnector):

    def get_id(self) -> str:

        return "hcp"

    def get_name(self) -> str:

        return "Haut-Commissariat au Plan"

    def get_base_url(self) -> str:

        return "https://www.hcp.ma"

    def get_allowed_formats(self) -> list[str]:

        return [
            "pdf",
            "xlsx",
            "xls",
            "csv",
            "html"
        ]

    def get_update_frequency(self) -> int:

        return 15

    def is_enabled(self) -> bool:

        return True

    def get_sectors(self) -> list[str]:

        return [
            "agriculture",
            "industrie",
            "commerce",
            "tourisme",
            "population",
            "emploi"
        ]

    def get_metadata(self) -> dict:

        metadata = super().get_metadata()

        metadata["sectors"] = self.get_sectors()

        metadata["enabled"] = self.is_enabled()

        return metadata