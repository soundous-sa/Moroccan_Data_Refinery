from dataclasses import dataclass
from datetime import datetime


@dataclass
class DiscoveryContext:

    source: dict

    started_at: datetime

    base_url: str