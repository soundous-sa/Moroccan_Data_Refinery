from dataclasses import dataclass, field

from app.domain.publication_collection import PublicationCollection


@dataclass
class HCPListingResult:

    publications: PublicationCollection

    format_counts: dict = field(default_factory=dict)
