from app.repositories.publication_resource_repository import (
    PublicationResourceRepository
)


class PublicationResourcePersistenceService:

    def __init__(self):

        self.repository = PublicationResourceRepository()

    def save_download_result(
        self,
        publication_id,
        resource,
        download_result
    ):

        resource.publication_id = publication_id
        resource.file_path = download_result.file_path
        resource.file_size = download_result.file_size
        resource.status = (
            "DOWNLOADED"
            if download_result.success
            else "FAILED"
        )

        return self.repository.save_or_update(resource)
