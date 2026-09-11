from datetime import datetime

from app.domain.publication import Publication
from app.domain.publication_collection import PublicationCollection
from app.domain.sector import Sector
from app.domain.category import Category

# ⚠️ Adapte ces valeurs selon tes enums Sector et Category
publication = Publication(
    title="Publication de test",
    publication_date=datetime.now(),
    url="https://www.hcp.ma/test.pdf",
    source_id="HCP",
    sector=Sector.PRIMARY,
    category=Category.POPULATION
)

publication2 = Publication(
    title="Publication de test 2",
    publication_date=datetime.now(),
    url="https://www.hcp.ma/test2.pdf",
    source_id="HCP",
    sector=Sector.PRIMARY,
    category=Category.POPULATION
)

collection = PublicationCollection()

collection.add(publication)

print("Nombre de publications :", collection.count())

for pub in collection:
    print(pub.title)