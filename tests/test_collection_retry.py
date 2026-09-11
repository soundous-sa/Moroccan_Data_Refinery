from datetime import datetime

from app.domain.category import Category
from app.domain.publication import Publication
from app.domain.publication_resource import PublicationResource
from app.domain.publication_status import PublicationStatus
from app.domain.sector import Sector
from app.repositories.publication_repository import PublicationRepository
from app.services.collection.collection_service import CollectionService
from app.services.download.download_result import DownloadResult
from app.services.persistence.publication_persistence_service import (
    PublicationPersistenceService
)


TEST_URL = "https://test.local/collection-retry"


class FakeResponse:

    headers = {"Content-Type": "text/html"}
    text = "<html></html>"
    url = TEST_URL


class FakeHTTPClient:

    def get(self, url):

        return FakeResponse()


class FakeExtractor:

    def extract(self, html, base_url, source_id):

        return [
            PublicationResource(
                title="Premier fichier",
                url="https://test.local/first.pdf",
                source_id=source_id
            ),
            PublicationResource(
                title="Second fichier",
                url="https://test.local/second.pdf",
                source_id=source_id
            )
        ]


class FakeResolver:

    def resolve(self, url):

        return PublicationResource(
            title="Ressource résolue",
            url=url,
            filename=url.rsplit("/", 1)[-1],
            source_id="hcp"
        )


class FakeDownloadManager:

    def download(self, publication, resource):

        return DownloadResult(
            success=True,
            url=resource.url,
            file_path=(
                "data/lake/raw/hcp/"
                f"{resource.filename}"
            ),
            file_size=100,
            status_code=200,
            error=None
        )


print()
print("=" * 60)
print("TEST COLLECTION SERVICE - REPRISE FAILED -> DOWNLOADED")
print("=" * 60)

repository = PublicationRepository()
publication_data = repository.get_by_url(TEST_URL)

if publication_data is None:

    publication = Publication(
        title="Test reprise collecte",
        publication_date=datetime.now(),
        url=TEST_URL,
        source_id="hcp",
        sector=Sector.UNKNOWN,
        category=Category.OTHER
    )

    repository.save(publication)

else:

    publication = repository.get_publication_by_id(
        publication_data["id"]
    )

persistence = PublicationPersistenceService()

if not persistence.update_status_to(
    publication.id,
    PublicationStatus.FAILED
):

    raise SystemExit("Impossible de préparer le statut FAILED.")

service = CollectionService()
service.http = FakeHTTPClient()
service.extractor = FakeExtractor()
service.resolver = FakeResolver()
service.download_manager = FakeDownloadManager()

result = service.collect(publication)
row = repository.get_by_id(publication.id)

print("Succès :", result.success)
print("Ressources :", result.resource_count)
print("Statut PostgreSQL final :", row["status"])

if not result.success:

    raise SystemExit("La reprise aurait dû réussir.")

if result.resource_count != 2:

    raise SystemExit("Le nombre de ressources est incorrect.")

if row["status"] != "DOWNLOADED":

    raise SystemExit(
        "Statut inattendu : "
        f"{row['status']} (attendu : DOWNLOADED)"
    )

print("Reprise FAILED -> DOWNLOADED validée.")
