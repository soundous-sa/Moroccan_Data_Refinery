from dataclasses import dataclass
from typing import Optional


@dataclass
class PublicationResource:

    title: str

    url: str

    file_type: Optional[str] = None

    content_type: Optional[str] = None

    filename: Optional[str] = None

    source_id: Optional[str] = None

    id: int | None = None

    publication_id: int | None = None

    file_path: Optional[str] = None

    file_size: int = 0

    status: str = "DISCOVERED"
