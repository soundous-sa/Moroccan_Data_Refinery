from datetime import datetime

from app.domain.category import Category
from app.domain.publication import Publication
from app.domain.sector import Sector

from app.services.discovery.publication_classifier import PublicationClassifier


publication = Publication(

    title="Rapport annuel sur l'emploi",

    publication_date=datetime.now(),

    url="https://www.hcp.ma/rapport.pdf",

    source_id="HCP",

    sector=Sector.UNKNOWN,

    category=Category.OTHER

)

classifier = PublicationClassifier()

result = classifier.classify(publication)

print()

print("=" * 60)

print("Score :", result.score)

print("Accepté :", result.accepted)

print("Raison :", result.reason)

print("=" * 60)