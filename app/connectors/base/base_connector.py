from abc import ABC, abstractmethod


class BaseConnector(ABC):

    @abstractmethod
    def get_id(self) -> str:
        """
        Identifiant unique de la source.
        Exemple : hcp
        """
        pass

    @abstractmethod
    def get_name(self) -> str:
        """
        Nom officiel de la source.
        """
        pass

    @abstractmethod
    def get_base_url(self) -> str:
        """
        URL principale de la source.
        """
        pass

    @abstractmethod
    def get_allowed_formats(self) -> list[str]:
        """
        Formats que le connecteur peut traiter.
        """
        pass

    @abstractmethod
    def get_update_frequency(self) -> int:
        """
        Fréquence de vérification en jours.
        """
        pass

    def get_metadata(self) -> dict:
        """
        Retourne les métadonnées générales du connecteur.
        """

        return {
            "id": self.get_id(),
            "name": self.get_name(),
            "base_url": self.get_base_url(),
            "allowed_formats": self.get_allowed_formats(),
            "update_frequency": self.get_update_frequency(),
        }

    def is_enabled(self) -> bool:
        """
        Permet d'activer ou désactiver un connecteur.
        """

        return True