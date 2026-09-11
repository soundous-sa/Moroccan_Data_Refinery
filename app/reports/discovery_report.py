from dataclasses import dataclass
from datetime import datetime

from app.reports.discovery_statistics import DiscoveryStatistics


@dataclass
class DiscoveryReport:

    source: str

    started_at: datetime

    finished_at: datetime

    success: bool

    statistics: DiscoveryStatistics

    message: str = ""