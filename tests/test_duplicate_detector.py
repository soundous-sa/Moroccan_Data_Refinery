from datetime import datetime

from app.domain.category import Category
from app.domain.publication import Publication
from app.domain.publication_collection import PublicationCollection
from app.domain.sector import Sector

from app.services.discovery.duplicate_detector import DuplicateDetector

collection = PublicationCollection()

publication1 = Publication(

    title="Rapport emploi",

    publication_date=datetime.now(),

    url="https://www.hcp.ma/rapport.pdf",

    source_id="HCP",

    sector=Sector.UNKNOWN,

    category=Category.OTHER

)

publication2 = Publication(

    title="Rapport emploi",

    publication_date=datetime.now(),

    url="https://www.hcp.ma/rapport.pdf",

    source_id="HCP",

    sector=Sector.UNKNOWN,

    category=Category.OTHER

)

publication3 = Publication(

    title="Rapport population",

    publication_date=datetime.now(),

    url="https://www.hcp.ma/population.pdf",

    source_id="HCP",

    sector=Sector.UNKNOWN,

    category=Category.OTHER

)

collection.add(publication1)
collection.add(publication2)
collection.add(publication3)

print()

print("=" * 60)

print("Avant :", collection.count())

detector = DuplicateDetector()

new_collection = detector.remove_duplicates(collection)

print("Après :", new_collection.count())

print("=" * 60)

for publication in new_collection:

    print(publication.title)