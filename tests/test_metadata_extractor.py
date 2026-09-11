from datetime import datetime

from app.domain.category import Category
from app.domain.publication import Publication
from app.domain.sector import Sector

from app.services.discovery.metadata_extractor import MetadataExtractor

publication = Publication(

    title="Rapport Emploi",

    publication_date=datetime.now(),

    url="https://www.hcp.ma/files/emploi_2025.xlsx",

    source_id="HCP",

    sector=Sector.UNKNOWN,

    category=Category.OTHER

)

extractor = MetadataExtractor()

metadata = extractor.extract(publication)

print()

print("=" * 60)

print("Nom :", metadata.filename)

print("Extension :", metadata.extension)

print("Type :", metadata.file_type)

print("Hash :", metadata.url_hash[:20], "...")

print("Storage :", metadata.storage_path)

print("=" * 60)