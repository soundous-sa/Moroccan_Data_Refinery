from app.domain.category import Category
from app.domain.publication import Publication
from app.domain.publication_status import PublicationStatus
from app.domain.sector import Sector

from app.repositories.publication_repository import (
    PublicationRepository
)

from app.services.persistence.publication_status_service import (
    PublicationStatusService
)


class PublicationPersistenceService:

    def __init__(self):

        self.repository = PublicationRepository()

    # ==================================================
    # SAUVEGARDE D'UNE COLLECTION
    # ==================================================

    def save_collection(self, collection):

        saved = 0
        duplicates = 0
        failed = 0

        for publication in collection:

            try:

                # ------------------------------------------
                # Vérifier si elle existe
                # ------------------------------------------

                if self.repository.exists(
                    publication.url
                ):

                    duplicates += 1

                    continue

                # ------------------------------------------
                # Sauvegarder
                # ------------------------------------------

                publication_id = self.repository.save(
                    publication
                )

                if publication_id:

                    saved += 1

            except Exception as error:

                failed += 1

                print(
                    f"Erreur sauvegarde : {error}"
                )

        return {

            "saved": saved,

            "duplicates": duplicates,

            "failed": failed

        }

    # ==================================================
    # RECUPERER LES PUBLICATIONS EN ECHEC (POUR RETRY)
    # ==================================================

    def get_failed_publications(self, source_id):

        rows = self.repository.find_by_status(
            source_id,
            PublicationStatus.FAILED.value
        )

        return self._map_rows_to_publications(rows)

    # ==================================================
    # RECUPERER LES PUBLICATIONS JAMAIS COLLECTEES
    # ==================================================
    #
    # Couvre aussi bien les publications tout juste découvertes
    # (ce run) que d'anciennes lignes restées bloquées en DISCOVERED
    # (ex. un run interrompu avant la mise à jour de statut).

    def get_pending_publications(self, source_id):

        rows = self.repository.find_by_status(
            source_id,
            PublicationStatus.DISCOVERED.value
        )

        return self._map_rows_to_publications(rows)

    # ==================================================
    # CONVERSION LIGNES SQL -> OBJETS PUBLICATION
    # ==================================================

    def _map_rows_to_publications(self, rows):

        return [
            Publication(
                id=row["id"],
                title=row["title"],
                publication_date=row["publication_date"],
                url=row["url"],
                source_id=row["source_id"],
                sector=self._safe_enum(
                    Sector, row["sector"], Sector.UNKNOWN
                ),
                category=self._safe_enum(
                    Category, row["category"], Category.OTHER
                )
            )
            for row in rows
        ]

    # ==================================================
    # LECTURE TOLERANTE D'UN ENUM DEPUIS LA BASE
    # ==================================================
    #
    # D'anciennes lignes (insérées avant cette version du code) ont
    # pu stocker le nom du membre Python (ex. "UNKNOWN") plutôt que
    # sa valeur (ex. "Inconnu"). On tente les deux avant de retomber
    # sur une valeur par défaut plutôt que de faire échouer toute la
    # collecte pour un champ qui n'est de toute façon jamais utilisé
    # par le téléchargement.

    def _safe_enum(self, enum_cls, raw_value, default):

        try:

            return enum_cls(raw_value)

        except ValueError:

            pass

        try:

            return enum_cls[raw_value]

        except KeyError:

            return default

    # ==================================================
    # CHANGER LE STATUT
    # ==================================================

    def update_status(
        self,
        publication_id: int,
        old_status,
        new_status
    ) -> bool:

        # ------------------------------------------
        # Vérification de la transition
        # ------------------------------------------

        PublicationStatusService.validate_transition(

            old_status,

            new_status

        )

        # ------------------------------------------
        # Mise à jour PostgreSQL
        # ------------------------------------------

        return self.repository.update_status(

            publication_id,

            old_status,

            new_status

        )

    # ==================================================
    # METTRE A JOUR DEPUIS LE STATUT COURANT
    # ==================================================

    def update_status_to(
        self,
        publication_id: int,
        new_status: PublicationStatus
    ) -> bool:

        data = self.repository.get_by_id(publication_id)

        if data is None:
            return False

        current_status = PublicationStatus(data["status"])

        # Une collecte relancée peut retrouver une publication déjà dans
        # l'état attendu : ce cas est un succès idempotent.
        if current_status == new_status:
            return True

        return self.update_status(
            publication_id,
            current_status,
            new_status
        )
