from app.connectors.base.base_connector import BaseConnector


class MinistryConnector(BaseConnector):

    def get_id(self) -> str:

        return "ministry"

    def get_name(self) -> str:

        return "Ministère de l'Économie et des Finances"

    def get_base_url(self) -> str:

        return "https://www.finances.gov.ma"

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
            "budget",
            "fiscalite",
            "dette-publique",
            "economie",
            "finances-publiques"
        ]

    def get_metadata(self) -> dict:

        metadata = super().get_metadata()

        metadata["sectors"] = self.get_sectors()

        metadata["enabled"] = self.is_enabled()

        return metadata
