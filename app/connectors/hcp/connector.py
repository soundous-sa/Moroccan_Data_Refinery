from app.connectors.base.base_connector import BaseConnector


class HCPConnector(BaseConnector):

    # Catégories réelles du site (paramètre "tag" de /downloads/?tag=...),
    # vérifiées manuellement sur hcp.ma. Contrairement aux anciennes
    # valeurs (agriculture, industrie, commerce, tourisme), qui ne
    # correspondent à aucun tag existant sur le site (0 résultat), celles-ci
    # renvoient des publications réelles.
    CATEGORIES = [
        "Emploi",
        "Population et démographie",
        "Comptes nationaux",
        "Indices des prix et production",
        "Conjoncture entreprise",
        "Revenu et conditions de vie",
        "Développement durable"
    ]

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

    def get_categories(self) -> list[str]:

        return list(self.CATEGORIES)

    def get_metadata(self) -> dict:

        metadata = super().get_metadata()

        metadata["categories"] = self.get_categories()

        metadata["enabled"] = self.is_enabled()

        return metadata