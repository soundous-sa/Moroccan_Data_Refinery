from datetime import datetime

from app.config.database import SessionLocal
from app.persistence.repositories.publication_repository import (
    PublicationRepository
)

from app.persistence.models.publication_model import (
    PublicationModel
)


print("=" * 60)
print("TEST PUBLICATION REPOSITORY")
print("=" * 60)


session = SessionLocal()


try:

    repository = PublicationRepository(session)

    url = "https://www.hcp.ma/test/rapport-test.pdf"

    # ==================================================
    # Vérifier si elle existe déjà
    # ==================================================

    exists = repository.exists_by_url(url)

    print()
    print("Publication déjà existante :", exists)

    # ==================================================
    # Insérer uniquement si elle n'existe pas
    # ==================================================

    if not exists:

        publication = PublicationModel(

            title="Rapport de test HCP",

            publication_date=datetime.now(),

            url=url,

            source_id="hcp",

            sector="UNKNOWN",

            category="OTHER",

            status="DISCOVERED"

        )

        saved = repository.add(
            publication
        )

        print()
        print("✅ Publication enregistrée.")

        print("ID :", saved.id)

    else:

        print()
        print("ℹ️ Publication déjà présente.")

    # ==================================================
    # Afficher toutes les publications
    # ==================================================

    publications = repository.find_all()

    print()
    print("Nombre de publications :", len(publications))

    for publication in publications:

        print()
        print("ID       :", publication.id)
        print("Titre    :", publication.title)
        print("URL      :", publication.url)
        print("Source   :", publication.source_id)
        print("Status   :", publication.status)


finally:

    session.close()