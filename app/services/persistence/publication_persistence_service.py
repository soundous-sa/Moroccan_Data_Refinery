from app.domain.publication_status import PublicationStatus

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
