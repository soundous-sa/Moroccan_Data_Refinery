from datetime import datetime

from app.domain.category import Category
from app.domain.publication import Publication
from app.domain.sector import Sector
from app.repositories.publication_repository import PublicationRepository
from app.repositories.publication_resource_repository import (
    PublicationResourceRepository
)
from app.services.collection.collection_service import CollectionService


PAGE_URL = (
    "https://www.hcp.ma/"
    "Note-d-information-sur-les-comptes-regionaux-de-l-annee-2024_a4333.html"
)

EXPECTED_RESOURCE_COUNT = 4


print()
print("=" * 60)
print("TEST COLLECTION SERVICE - PAGE HCP MULTI-FICHIERS")
print("=" * 60)

repository = PublicationRepository()
resource_repository = PublicationResourceRepository()
publication_data = repository.get_by_url(PAGE_URL)

if publication_data is None:

    publication = Publication(
        title="Note d'information sur les comptes régionaux 2024",
        publication_date=datetime.now(),
        url=PAGE_URL,
        source_id="hcp",
        sector=Sector.UNKNOWN,
        category=Category.OTHER
    )

    repository.save(publication)
    print("Publication de test créée :", publication.id)

else:

    publication = repository.get_publication_by_id(
        publication_data["id"]
    )
    print("Publication de test existante :", publication.id)

service = CollectionService()
result = service.collect(publication)

print()
print("Succès :", result.success)
print("Ressources détectées :", result.resource_count)
print("Taille totale :", result.file_size, "octets")
print("Erreur :", result.error)

for index, download in enumerate(result.download_results, start=1):

    print()
    print(f"Ressource {index}")
    print("URL :", download.url)
    print("Fichier :", download.file_path)
    print("Succès :", download.success)

row = repository.get_by_id(publication.id)
saved_resources = resource_repository.find_by_publication_id(
    publication.id
)

print()
print("Statut PostgreSQL final :", row["status"])
print("Ressources PostgreSQL :", len(saved_resources))

if not result.success:

    raise SystemExit("La collecte multi-fichiers a échoué.")

if result.resource_count != EXPECTED_RESOURCE_COUNT:

    raise SystemExit(
        "Nombre de ressources inattendu : "
        f"{result.resource_count} "
        f"(attendu : {EXPECTED_RESOURCE_COUNT})"
    )

if len(saved_resources) != EXPECTED_RESOURCE_COUNT:

    raise SystemExit(
        "Nombre de ressources persistées inattendu : "
        f"{len(saved_resources)} "
        f"(attendu : {EXPECTED_RESOURCE_COUNT})"
    )

if any(resource["status"] != "DOWNLOADED" for resource in saved_resources):

    raise SystemExit(
        "Une ressource persistée n'est pas dans le statut DOWNLOADED."
    )

if row["status"] != "DOWNLOADED":

    raise SystemExit(
        "Statut inattendu : "
        f"{row['status']} (attendu : DOWNLOADED)"
    )

print("Pipeline multi-fichiers validé.")
