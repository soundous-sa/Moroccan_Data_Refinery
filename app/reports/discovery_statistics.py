from dataclasses import dataclass


@dataclass
class DiscoveryStatistics:

    pages_visited: int = 0

    links_found: int = 0

    publications_found: int = 0

    duplicates_removed: int = 0

    pdf_count: int = 0

    excel_count: int = 0

    csv_count: int = 0

    html_count: int = 0
    