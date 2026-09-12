import re

from datetime import datetime

from app.domain.category import Category
from app.domain.publication import Publication
from app.domain.publication_collection import PublicationCollection
from app.domain.sector import Sector

from app.services.discovery.hcp_listing_result import HCPListingResult
from app.services.discovery.html_parser import HTMLParser
from app.services.discovery.url_manager import URLManager


class HCPListingParser:
    """
    Parse une page de listing HCP (https://www.hcp.ma/downloads/?tag=...)
    en s'appuyant sur le balisage réel du site (vérifié manuellement) :

        div.delimiter                     -> une publication
          div.titre_fichier > a[href]     -> titre + page de détail
          div.information > img.image     -> icône de format (icon_pdf.gif, ...)
          div.information (texte)         -> "Publié le : JJ/MM/AAAA"
    """

    ITEM_SELECTOR = "div.delimiter"

    DATE_PATTERN = re.compile(r"Publié le\s*:\s*(\d{2}/\d{2}/\d{4})")

    KNOWN_EXTENSIONS = [
        "xlsx",
        "docx",
        "pdf",
        "xls",
        "csv",
        "doc",
        "zip",
        "html",
        "htm"
    ]

    EXTENSION_TO_STAT_KEY = {
        "pdf": "pdf_count",
        "xlsx": "excel_count",
        "xls": "excel_count",
        "csv": "csv_count",
        "html": "html_count",
        "htm": "html_count"
    }

    TAG_TO_CATEGORY = {
        "emploi": Category.EMPLOYMENT,
        "population et démographie": Category.POPULATION,
        "education et formation": Category.EDUCATION,
        "développement durable": Category.OTHER
    }

    def __init__(self):

        self.html_parser = HTMLParser()

    # ==================================================
    # PARSE UNE PAGE DE LISTING
    # ==================================================

    def parse(
        self,
        html: str,
        page_url: str,
        source_id: str,
        category_name: str,
        allowed_formats: list[str] | None = None
    ) -> HCPListingResult:

        collection = PublicationCollection()

        format_counts = {}

        soup = self.html_parser.parse(html)

        normalized_formats = None

        if allowed_formats:

            normalized_formats = {
                fmt.lower() for fmt in allowed_formats
            }

        for item in soup.select(self.ITEM_SELECTOR):

            extension = self._detect_extension(item)

            if not self._is_format_allowed(extension, normalized_formats):

                continue

            publication = self._parse_item(
                item,
                page_url,
                source_id,
                category_name
            )

            if publication is None:

                continue

            collection.add(publication)

            self._count_format(format_counts, extension)

        return HCPListingResult(
            publications=collection,
            format_counts=format_counts
        )

    # ==================================================
    # UNE PUBLICATION
    # ==================================================

    def _parse_item(self, item, page_url, source_id, category_name):

        title_link = item.select_one("div.titre_fichier a[href]")

        if title_link is None:

            return None

        title = title_link.get_text(strip=True)

        if not title:

            return None

        url = URLManager.join(page_url, title_link["href"])

        return Publication(
            title=title,
            publication_date=self._extract_date(item),
            url=url,
            source_id=source_id,
            sector=Sector.UNKNOWN,
            category=self._resolve_category(category_name)
        )

    def _extract_date(self, item):

        text = item.get_text(" ", strip=True)

        match = self.DATE_PATTERN.search(text)

        if not match:

            return datetime.now()

        try:

            return datetime.strptime(
                match.group(1),
                "%d/%m/%Y"
            )

        except ValueError:

            return datetime.now()

    def _resolve_category(self, category_name):

        return self.TAG_TO_CATEGORY.get(
            category_name.strip().lower(),
            Category.OTHER
        )

    # ==================================================
    # FORMAT (icône)
    # ==================================================

    def _detect_extension(self, item):

        icon = item.select_one("div.information img")

        if icon is None or not icon.get("src"):

            return None

        src = icon["src"].lower()

        for extension in self.KNOWN_EXTENSIONS:

            if extension in src:

                return extension

        return None

    def _is_format_allowed(self, extension, normalized_formats):

        if normalized_formats is None:

            return True

        if extension is None:

            # Format inconnu : laissé passer, la résolution réelle du
            # fichier (Collection/Download) tranchera.
            return True

        return extension in normalized_formats

    def _count_format(self, format_counts, extension):

        stat_key = self.EXTENSION_TO_STAT_KEY.get(extension)

        if stat_key is None:

            return

        format_counts[stat_key] = format_counts.get(stat_key, 0) + 1
