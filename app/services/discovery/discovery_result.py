from dataclasses import dataclass

from app.domain.publication_collection import PublicationCollection

from app.reports.discovery_report import DiscoveryReport


@dataclass
class DiscoveryResult:

    publications: PublicationCollection

    report: DiscoveryReport