from datetime import datetime

from app.domain.category import Category
from app.domain.publication import Publication
from app.domain.publication_resource import PublicationResource
from app.domain.sector import Sector
from app.repositories.publication_repository import PublicationRepository
from app.repositories.publication_resource_repository import (
    PublicationResourceRepository
)
from app.services.collection.collection_service import CollectionService
from app.services.download.download_result import DownloadResult


TEST_URL = "https://test.local/collection-failure"


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
                title="Fichier valide",
                url="https://test.local/valid.pdf",
                source_id=source_id
            ),
            PublicationResource(
                title="Fichier indisponible",
                url="https://test.local/missing.pdf",
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

        if resource.url.endswith("missing.pdf"):

            return DownloadResult(
                success=False,
                url=resource.url,
                file_path=None,
                file_size=0,
                status_code=404,
                error="HTTP 404 : fichier introuvable"
            )

        return DownloadResult(
            success=True,
            url=resource.url,
            file_path="data/lake/raw/hcp/valid.pdf",
            file_size=100,
            status_code=200,
            error=None
        )


print()
print("=" * 60)
print("TEST COLLECTION SERVICE - ECHEC PARTIEL")
print("=" * 60)

repository = PublicationRepository()
resource_repository = PublicationResourceRepository()
publication_data = repository.get_by_url(TEST_URL)

if publication_data is None:

    publication = Publication(
        title="Test collecte en erreur",
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

service = CollectionService()
service.http = FakeHTTPClient()
service.extractor = FakeExtractor()
service.resolver = FakeResolver()
service.download_manager = FakeDownloadManager()

result = service.collect(publication)
row = repository.get_by_id(publication.id)
saved_resources = resource_repository.find_by_publication_id(
    publication.id
)

print("Succès :", result.success)
print("Ressources :", result.resource_count)
print("Fichiers réussis :", sum(
    download.success
    for download in result.download_results
))
print("Erreur :", result.error)
print("Statut PostgreSQL :", row["status"])
print("Ressources PostgreSQL :", len(saved_resources))

if result.success:

    raise SystemExit("La collecte aurait dû échouer.")

if result.resource_count != 2:

    raise SystemExit("Le nombre de ressources est incorrect.")

if len(result.download_results) != 2:

    raise SystemExit("Les résultats de téléchargement sont incomplets.")

if row["status"] != "FAILED":

    raise SystemExit(
        "Statut inattendu : "
        f"{row['status']} (attendu : FAILED)"
    )

resource_statuses = {
    resource["status"]
    for resource in saved_resources
}

if resource_statuses != {"DOWNLOADED", "FAILED"}:

    raise SystemExit(
        "Statuts de ressources inattendus : "
        f"{resource_statuses}"
    )

print("Gestion de l'échec validée.")
