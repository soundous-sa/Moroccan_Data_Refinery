from app.connectors.base.base_connector import BaseConnector


class BAMConnector(BaseConnector):

    def get_id(self) -> str:

        return "bam"

    def get_name(self) -> str:

        return "Bank Al-Maghrib"

    def get_base_url(self) -> str:

        return "https://www.bkam.ma"

    def get_allowed_formats(self) -> list[str]:

        return [
            "pdf",
            "xlsx",
            "xls",
            "csv",
            "html"
        ]

    def get_update_frequency(self) -> int:

        return 7

    def is_enabled(self) -> bool:

        return True

    def get_sectors(self) -> list[str]:

        return [
            "politique-monetaire",
            "taux-de-change",
            "inflation",
            "statistiques-monetaires",
            "supervision-bancaire"
        ]

    def get_metadata(self) -> dict:

        metadata = super().get_metadata()

        metadata["sectors"] = self.get_sectors()

        metadata["enabled"] = self.is_enabled()

        return metadata
