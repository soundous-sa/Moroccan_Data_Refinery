from urllib.parse import quote

from app.config.logger import logger

from app.domain.publication_collection import PublicationCollection

from app.services.crawler.http_client import HTTPClient

from app.services.discovery.category_crawl_result import CategoryCrawlResult
from app.services.discovery.duplicate_detector import DuplicateDetector
from app.services.discovery.hcp_listing_parser import HCPListingParser
from app.services.discovery.pagination_navigator import PaginationNavigator
from app.services.discovery.url_manager import URLManager


class CategoryDiscoveryCrawler:
    """
    Parcourt, pour un connecteur donné, chacune de ses catégories
    (connector.get_categories()) puis suit la pagination de chaque
    catégorie jusqu'à la dernière page.

    Une catégorie HCP correspond à un "tag" du site :
    https://www.hcp.ma/downloads/?tag=<catégorie>
    """

    LISTING_PATH = "/downloads/"

    DEFAULT_MAX_PAGES_PER_CATEGORY = 30

    def __init__(
        self,
        http_client=None,
        listing_parser=None,
        pagination_navigator=None,
        max_pages_per_category: int = DEFAULT_MAX_PAGES_PER_CATEGORY
    ):

        self.http = http_client or HTTPClient()

        self.listing_parser = listing_parser or HCPListingParser()

        self.pagination_navigator = (
            pagination_navigator or PaginationNavigator()
        )

        self.duplicate_detector = DuplicateDetector()

        self.max_pages_per_category = max_pages_per_category

    # ==================================================
    # PARCOURIR TOUTES LES CATEGORIES
    # ==================================================

    def crawl(self, connector) -> CategoryCrawlResult:

        collection = PublicationCollection()

        pages_visited = 0

        links_found = 0

        format_counts = {}

        categories = connector.get_categories()

        for category in categories:

            category_pages, category_links = self._crawl_category(
                connector,
                category,
                collection,
                format_counts
            )

            pages_visited += category_pages

            links_found += category_links

        deduplicated = self.duplicate_detector.remove_duplicates(
            collection
        )

        return CategoryCrawlResult(
            publications=deduplicated,
            pages_visited=pages_visited,
            links_found=links_found,
            categories_visited=len(categories),
            format_counts=format_counts
        )

    # ==================================================
    # PARCOURIR UNE CATEGORIE (avec pagination)
    # ==================================================

    def _crawl_category(self, connector, category, collection, format_counts):

        url = self._build_category_url(
            connector.get_base_url(),
            category
        )

        visited_urls = set()

        pages_visited = 0

        links_found = 0

        while (
            url
            and url not in visited_urls
            and pages_visited < self.max_pages_per_category
        ):

            visited_urls.add(url)

            logger.info(
                f"Discovery HCP [{category}] "
                f"page {pages_visited + 1} : {url}"
            )

            response = self.http.get(url)

            html = response.text

            links_found += len(
                self.listing_parser.html_parser.find_all(html, "a")
            )

            listing_result = self.listing_parser.parse(
                html,
                response.url,
                connector.get_id(),
                category,
                allowed_formats=connector.get_allowed_formats()
            )

            for publication in listing_result.publications:

                collection.add(publication)

            for stat_key, count in listing_result.format_counts.items():

                format_counts[stat_key] = (
                    format_counts.get(stat_key, 0) + count
                )

            pages_visited += 1

            url = self.pagination_navigator.find_next_url(
                html,
                response.url
            )

        return pages_visited, links_found

    def _build_category_url(self, base_url, category):

        return URLManager.join(
            base_url,
            f"{self.LISTING_PATH}?tag={quote(category)}"
        )
