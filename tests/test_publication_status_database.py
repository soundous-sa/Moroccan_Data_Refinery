from datetime import datetime

from app.domain.category import Category
from app.domain.publication import Publication
from app.domain.publication_status import PublicationStatus
from app.domain.sector import Sector

from app.repositories.publication_repository import (
    PublicationRepository
)

from app.services.persistence.publication_persistence_service import (
    PublicationPersistenceService
)


print("=" * 60)
print("TEST PUBLICATION STATUS + POSTGRESQL")
print("=" * 60)


# ==================================================
# Création de la publication
# ==================================================

publication = Publication(

    title="Test statut HCP",

    publication_date=datetime.now(),

    url="https://www.hcp.ma/test/status-test.pdf",

    source_id="hcp",

    sector=Sector.UNKNOWN,

    category=Category.OTHER

)


# ==================================================
# Initialisation
# ==================================================

repository = PublicationRepository()

persistence = PublicationPersistenceService()


# ==================================================
# Vérifier si la publication existe
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
# Récupérer ou créer la publication
# ==================================================

if not exists:

    publication_id = repository.save(
        publication
    )

    print()

    print(
        "✅ Publication créée."
    )

    print(
        "ID :",
        publication_id
    )

else:

    existing = repository.get_by_url(
        publication.url
    )

    if existing is None:

        print()

        print(
            "❌ Publication déclarée existante "
            "mais impossible à récupérer."
        )

        exit()

    publication_id = existing["id"]

    print()

    print(
        "ℹ️ Publication déjà présente."
    )

    print(
        "ID :",
        publication_id
    )


# ==================================================
# Vérification avant changement de statut
# ==================================================

existing = repository.get_by_id(
    publication_id
)

if existing is None:

    print()

    print(
        "❌ Publication introuvable dans PostgreSQL."
    )

    exit()


print()

print(
    "Statut avant modification :",
    existing["status"]
)


# ==================================================
# DISCOVERED → DOWNLOADED
# ==================================================

success = persistence.update_status(

    publication_id,

    PublicationStatus.DISCOVERED,

    PublicationStatus.DOWNLOADED

)


print()

print(
    "DISCOVERED → DOWNLOADED :",
    success
)


# ==================================================
# Vérification après modification
# ==================================================

row = repository.get_by_id(
    publication_id
)

if row is None:

    print()

    print(
        "❌ Publication introuvable après modification."
    )

    exit()


print()

print(
    "Statut actuel :",
    row["status"]
)


# ==================================================
# Informations finales
# ==================================================

print()

print(
    "ID       :",
    row["id"]
)

print(
    "Titre    :",
    row["title"]
)

print(
    "URL      :",
    row["url"]
)

print(
    "Source   :",
    row["source_id"]
)

print(
    "Status   :",
    row["status"]
)

print()

print("=" * 60)
print("TEST TERMINÉ")
print("=" * 60)