from dataclasses import dataclass
from datetime import datetime


@dataclass
class DownloadTask:

    url: str

    destination: str

    created_at: datetime

    downloaded: bool = False