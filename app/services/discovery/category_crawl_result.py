from dataclasses import dataclass, field

from app.domain.publication_collection import PublicationCollection


@dataclass
class CategoryCrawlResult:

    publications: PublicationCollection

    pages_visited: int = 0

    links_found: int = 0

    categories_visited: int = 0

    format_counts: dict = field(default_factory=dict)
