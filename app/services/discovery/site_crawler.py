from collections import deque
from urllib.parse import urlparse

from app.config.logger import logger

from app.domain.publication_collection import PublicationCollection

from app.services.crawler.http_client import HTTPClient

from app.services.discovery.duplicate_detector import DuplicateDetector
from app.services.discovery.html_parser import HTMLParser
from app.services.discovery.publication_detector import PublicationDetector
from app.services.discovery.url_normalizer import URLNormalizer


# Liens vers des fichiers : ce sont des ressources à détecter, pas des
# pages HTML à explorer davantage.
NON_HTML_EXTENSIONS = (
    ".pdf", ".xlsx", ".xls", ".csv", ".zip", ".doc", ".docx",
    ".json", ".xml", ".jpg", ".jpeg", ".png", ".gif", ".svg",
    ".mp4", ".mp3", ".rar", ".7z"
)

IGNORED_SCHEMES = ("mailto:", "tel:", "javascript:")


class SiteCrawler:
    """
    Explore plusieurs pages d'une même source (parcours en largeur,
    limité au domaine du connecteur) afin de détecter les publications
    qui ne sont pas visibles depuis la seule page d'accueil.
    """

    def __init__(self):

        self.http = HTTPClient()
        self.parser = HTMLParser()
        self.normalizer = URLNormalizer()
        self.detector = PublicationDetector()
        self.duplicate_detector = DuplicateDetector()

    # ==================================================
    # PARCOURS DU SITE
    # ==================================================

    def crawl(
        self,
        base_url: str,
        source_id: str,
        max_depth: int = 2,
        max_pages: int = 25
    ):

        domain = urlparse(base_url).netloc

        start_key = self._key(base_url, base_url)

        visited = set()
        queued = {start_key}
        queue = deque([(base_url, 0)])

        publications = PublicationCollection()

        pages_visited = 0
        links_found = 0

        while queue and pages_visited < max_pages:

            url, depth = queue.popleft()

            key = self._key(url, base_url)

            if key in visited:
                continue

            visited.add(key)

            try:

                response = self.http.get(url)

            except Exception as error:

                logger.warning(
                    f"Page ignorée ({url}) : {error}"
                )

                continue

            content_type = response.headers.get(
                "Content-Type", ""
            ).lower()

            if "html" not in content_type:
                continue

            pages_visited += 1

            html = response.text

            page_publications = self.detector.detect(
                html,
                source_id,
                base_url
            )

            for publication in page_publications:
                publications.add(publication)

            if depth >= max_depth:
                continue

            links = self.parser.find_all(html, "a")

            links_found += len(links)

            for link in links:

                next_url = self._resolve_navigation_link(
                    link.href,
                    base_url,
                    domain
                )

                if next_url is None:
                    continue

                next_key = self._key(next_url, base_url)

                if next_key in visited or next_key in queued:
                    continue

                queued.add(next_key)

                queue.append((next_url, depth + 1))

        deduplicated = self.duplicate_detector.remove_duplicates(
            publications
        )

        return deduplicated, pages_visited, links_found

    # ==================================================
    # RESOLUTION D'UN LIEN DE NAVIGATION
    # ==================================================

    def _resolve_navigation_link(self, href, base_url, domain):

        if not href:
            return None

        href = href.strip()

        if href == "" or href.startswith("#"):
            return None

        if href.lower().startswith(IGNORED_SCHEMES):
            return None

        absolute_url = self.normalizer.normalize(href, base_url)

        parsed = urlparse(absolute_url)

        if parsed.netloc != domain:
            return None

        path = parsed.path.lower()

        if path.endswith(NON_HTML_EXTENSIONS):
            return None

        return absolute_url

    def _key(self, url, base_url):

        normalized = self.normalizer.normalize(url, base_url)

        return normalized.rstrip("/").lower()

    def close(self):

        self.http.close()
