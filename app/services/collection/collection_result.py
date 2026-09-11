from dataclasses import dataclass, field
from typing import Optional

from app.services.download.download_result import DownloadResult


@dataclass
class CollectionResult:

    success: bool

    publication_id: Optional[int]

    url: str

    file_path: Optional[str]

    file_size: int

    file_type: Optional[str]

    error: Optional[str]

    download_results: list[DownloadResult] = field(
        default_factory=list
    )

    resource_count: int = 0
