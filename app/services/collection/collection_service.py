from app.config.logger import logger
from app.domain.publication_resource import PublicationResource
from app.domain.publication_status import PublicationStatus
from app.services.collection.collection_result import CollectionResult
from app.services.crawler.http_client import HTTPClient
from app.services.crawler.resource_resolver import ResourceResolver
from app.services.discovery.download_link_extractor import DownloadLinkExtractor
from app.services.download.download_manager import DownloadManager
from app.services.persistence.publication_persistence_service import (
    PublicationPersistenceService
)
from app.services.persistence.publication_resource_persistence_service import (
    PublicationResourcePersistenceService
)


class CollectionService:

    def __init__(self):

        self.http = HTTPClient()
        self.extractor = DownloadLinkExtractor()
        self.resolver = ResourceResolver()
        self.download_manager = DownloadManager()
        self.persistence = PublicationPersistenceService()
        self.resource_persistence = (
            PublicationResourcePersistenceService()
        )

    # ==================================================
    # COLLECTER UNE PUBLICATION ET SES RESSOURCES
    # ==================================================

    def collect(self, publication):

        logger.info(
            f"Début de collecte : {publication.title}"
        )

        if publication.id is None:

            raise ValueError(
                "La publication doit être enregistrée avant sa collecte "
                "afin de pouvoir mettre à jour son statut."
            )

        download_results = []

        try:

            page_response = self.http.get(publication.url)

            resources = self._extract_resources(
                publication,
                page_response
            )

            if not resources:

                return self._failure_result(
                    publication,
                    "Aucune ressource téléchargeable détectée.",
                    download_results,
                    0
                )

            for resource in resources:

                resolved_resource = self.resolver.resolve(
                    resource.url
                )

                resolved_resource.source_id = publication.source_id

                logger.success(
                    f"Ressource résolue : "
                    f"{resolved_resource.filename}"
                )

                download_result = self.download_manager.download(
                    publication,
                    resolved_resource
                )

                download_results.append(download_result)

                self.resource_persistence.save_download_result(
                    publication.id,
                    resolved_resource,
                    download_result
                )

                if not download_result.success:

                    logger.error(
                        f"Échec téléchargement : "
                        f"{download_result.error}"
                    )

            failed_results = [
                result
                for result in download_results
                if not result.success
            ]

            if failed_results:

                return self._failure_result(
                    publication,
                    failed_results[0].error,
                    download_results,
                    len(resources)
                )

            status_updated = self.persistence.update_status_to(
                publication.id,
                PublicationStatus.DOWNLOADED
            )

            if status_updated:

                logger.success(
                    "Statut mis à jour : "
                    "DISCOVERED -> DOWNLOADED"
                )

            else:

                logger.warning(
                    "Le statut n'a pas été mis à jour."
                )

            total_size = sum(
                result.file_size
                for result in download_results
            )

            logger.success(
                f"Publication collectée : {publication.title} "
                f"({len(download_results)} ressource(s))"
            )

            return CollectionResult(
                success=True,
                publication_id=publication.id,
                url=publication.url,
                file_path=(
                    download_results[0].file_path
                    if len(download_results) == 1
                    else None
                ),
                file_size=total_size,
                file_type=None,
                error=None,
                download_results=download_results,
                resource_count=len(resources)
            )

        except Exception as error:

            logger.error(f"Erreur collecte : {error}")

            return self._failure_result(
                publication,
                str(error),
                download_results,
                len(download_results)
            )

    # ==================================================
    # GERER UN ECHEC DE COLLECTE
    # ==================================================

    def _failure_result(
        self,
        publication,
        error,
        download_results,
        resource_count
    ):

        status_updated = self.persistence.update_status_to(
            publication.id,
            PublicationStatus.FAILED
        )

        if status_updated:

            logger.warning(
                "Statut mis à jour : FAILED"
            )

        else:

            logger.warning(
                "Le statut FAILED n'a pas été mis à jour."
            )

        return CollectionResult(
            success=False,
            publication_id=publication.id,
            url=publication.url,
            file_path=None,
            file_size=sum(
                result.file_size
                for result in download_results
            ),
            file_type=None,
            error=error,
            download_results=download_results,
            resource_count=resource_count
        )

    # ==================================================
    # IDENTIFIER LES RESSOURCES A COLLECTER
    # ==================================================

    def _extract_resources(self, publication, response):

        content_type = response.headers.get(
            "Content-Type",
            ""
        ).lower()

        if "html" in content_type:

            return self.extractor.extract(
                response.text,
                response.url,
                publication.source_id
            )

        # Compatibilité V1 : une publication peut déjà pointer directement
        # vers un fichier et non vers une page HTML.
        return [
            PublicationResource(
                title=publication.title,
                url=response.url,
                source_id=publication.source_id
            )
        ]
