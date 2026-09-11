from dataclasses import dataclass
from typing import Optional


@dataclass
class DownloadResult:

    success: bool

    url: str

    file_path: Optional[str]

    file_size: int

    status_code: Optional[int]

    error: Optional[str]