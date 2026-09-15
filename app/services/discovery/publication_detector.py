from datetime import datetime

from app.domain.category import Category
from app.domain.publication import Publication
from app.domain.publication_collection import PublicationCollection
from app.domain.sector import Sector

from app.services.discovery.html_parser import HTMLParser
from app.services.discovery.metadata_extractor import MetadataExtractor
from app.services.discovery.publication_filter import PublicationFilter
from app.services.discovery.publication_classifier import PublicationClassifier
from app.services.discovery.url_normalizer import URLNormalizer
from app.services.discovery.duplicate_detector import DuplicateDetector

class PublicationDetector:

    def __init__(self):

        self.parser = HTMLParser()
        self.filter = PublicationFilter()
        self.classifier = PublicationClassifier()
        self.normalizer = URLNormalizer()
        self.duplicate_detector = DuplicateDetector()
        self.metadata_extractor = MetadataExtractor()
    def detect(
        self,
        html: str,
        source_id: str,
        base_url: str = "https://www.hcp.ma"
    ) -> PublicationCollection:

        collection = PublicationCollection()

        links = self.parser.find_all(
            html,
            "a"
        )

        for link in links:

            if link.href is None:
                continue

            if link.text.strip() == "":
                continue

            # Normalisation de l'URL
            absolute_url = self.normalizer.normalize(
                link.href,
                base_url
            )

            # Création de la publication
            publication = Publication(
                title=link.text.strip(),
                publication_date=datetime.now(),
                url=absolute_url,
                source_id=source_id,
                sector=Sector.UNKNOWN,
                category=Category.OTHER
            )
            publication.metadata = self.metadata_extractor.extract(
                    publication
)

            # Classification
            result = self.classifier.classify(publication)

            if result.accepted:
                collection.add(publication)

        # Filtrage final
        filtered = self.filter.filter(collection)

        return self.duplicate_detector.remove_duplicates(filtered)