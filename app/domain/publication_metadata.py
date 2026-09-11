from dataclasses import dataclass
from datetime import datetime


@dataclass
class PublicationMetadata:

    filename: str

    extension: str

    file_type: str

    absolute_url: str

    url_hash: str

    discovered_at: datetime

    storage_path: str