from datetime import datetime

from app.domain.publication import Publication
from app.domain.sector import Sector
from app.domain.category import Category

from app.repositories.publication_repository import (
    PublicationRepository
)

from app.services.persistence.publication_persistence_service import (
    PublicationPersistenceService
)

from app.services.download.download_service import (
    DownloadService
)


print("=" * 60)
print("TEST DOWNLOAD SERVICE")
print("=" * 60)


publication = Publication(

    title="Test Download Service",

    publication_date=datetime.now(),

    url="URL_REELLE_DU_FICHIER",

    source_id="hcp",

    sector=Sector.UNKNOWN,

    category=Category.OTHER
)


repository = PublicationRepository()

persistence = PublicationPersistenceService()


# ==================================================
# Vérifier existence
# ==================================================

exists = repository.exists(
    publication.url
)

print()

print(
    "Publication déjà existante :",
    exists
)


# ==================================================
# Création
# ==================================================

if not exists:

    publication_id = repository.save(
        publication
    )

    print(
        "Publication créée."
    )

else:

    rows = repository.find_all()

    publication_id = None

    for row in rows:

        if row.url == publication.url:

            publication_id = row.id

            break


print(
    "ID :",
    publication_id
)


# ==================================================
# Téléchargement
# ==================================================

service = DownloadService()


result = service.download_publication(

    publication_id,

    publication

)


print()

print(
    "Téléchargement réussi :",
    result["success"]
)

print(
    "Statut mis à jour :",
    result["status_updated"]
)

print(
    "Fichier :",
    result["file_path"]
)

print(
    "Taille :",
    result["file_size"]
)

print(
    "Erreur :",
    result["error"]
)


print("=" * 60)