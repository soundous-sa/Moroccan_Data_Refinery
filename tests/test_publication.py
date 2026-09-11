from datetime import datetime

from app.domain.publication import Publication
from app.domain.category import Category
from app.domain.sector import Sector


def main():
    print("=" * 60)
    print("TEST PUBLICATION")
    print("=" * 60)

    print("\n1. Création d'une Publication sans ID...")

    publication = Publication(
        title="Test publication HCP",
        publication_date=datetime(2026, 9, 2),
        url="https://www.hcp.ma/test",
        source_id="hcp",
        sector=Sector.AGRICULTURE,
        category=Category.REPORT,
    )

    print("Publication créée :", publication)

    print("\n2. Vérification de l'ID...")
    print("ID :", publication.id)

    print("\n3. Vérification des attributs...")
    print("Titre :", publication.title)
    print("URL :", publication.url)
    print("Source :", publication.source_id)
    print("Secteur :", publication.sector)
    print("Catégorie :", publication.category)

    print("\n4. Vérification...")
    assert publication.id is None
    assert publication.title == "Test publication HCP"
    assert publication.url == "https://www.hcp.ma/test"
    assert publication.source_id == "hcp"

    print("\n✅ Publication fonctionne correctement.")


if __name__ == "__main__":
    main()