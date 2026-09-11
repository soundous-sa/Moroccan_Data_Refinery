from dataclasses import dataclass


@dataclass
class FilterStatistics:

    total_links: int = 0

    removed_links: int = 0

    kept_links: int = 0

    duplicated_links: int = 0

    social_links: int = 0

    invalid_links: int = 0