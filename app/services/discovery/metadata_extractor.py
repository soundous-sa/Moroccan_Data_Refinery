from datetime import datetime
from pathlib import Path

from app.domain.publication_metadata import PublicationMetadata

from app.services.discovery.file_type_detector import FileTypeDetector
from app.services.discovery.hash_generator import HashGenerator


class MetadataExtractor:

    def __init__(self):

        self.detector = FileTypeDetector()

        self.hash_generator = HashGenerator()

    def extract(self, publication):

        filename = Path(

            publication.url

        ).name

        extension = Path(

            filename

        ).suffix.lower()

        file_type = self.detector.detect(

            publication.url

        )

        url_hash = self.hash_generator.generate(

            publication.url

        )

        storage_path = (

            f"raw/"

            f"{publication.source_id.lower()}/"

            f"{datetime.now().year}/"

            f"{datetime.now().month:02d}/"

            f"{filename}"

        )

        return PublicationMetadata(

            filename=filename,

            extension=extension,

            file_type=file_type,

            absolute_url=publication.url,

            url_hash=url_hash,

            discovered_at=datetime.now(),

            storage_path=storage_path

        )