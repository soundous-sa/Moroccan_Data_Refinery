from app.domain.publication_status import PublicationStatus

from app.services.download.download_manager import (
    DownloadManager
)

from app.services.persistence.publication_persistence_service import (
    PublicationPersistenceService
)


class DownloadService:

    def __init__(self):

        self.manager = DownloadManager()

        self.persistence = (
            PublicationPersistenceService()
        )

    def download_publication(
        self,
        publication_id,
        publication
    ):

        result = self.manager.download(
            publication
        )

        if result.success:

            status_updated = (
                self.persistence.update_status(
                    publication_id,
                    PublicationStatus.DISCOVERED,
                    PublicationStatus.DOWNLOADED
                )
            )

            return {

                "success": True,

                "status_updated": status_updated,

                "file_path": result.file_path,

                "file_size": result.file_size,

                "error": None
            }

        else:

            status_updated = (
                self.persistence.update_status(
                    publication_id,
                    PublicationStatus.DISCOVERED,
                    PublicationStatus.FAILED
                )
            )

            return {

                "success": False,

                "status_updated": status_updated,

                "file_path": None,

                "file_size": 0,

                "error": result.error
            }