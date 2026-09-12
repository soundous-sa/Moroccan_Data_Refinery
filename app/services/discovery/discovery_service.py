from datetime import datetime

from app.reports.discovery_report import DiscoveryReport
from app.reports.discovery_statistics import DiscoveryStatistics
from app.reports.report_builder import ReportBuilder

from app.services.crawler.http_client import HTTPClient

from app.services.discovery.category_discovery_crawler import (
    CategoryDiscoveryCrawler
)
from app.services.discovery.discovery_context import DiscoveryContext
from app.services.discovery.discovery_logger import DiscoveryLogger
from app.services.discovery.discovery_result import DiscoveryResult
from app.services.discovery.publication_detector import PublicationDetector
from app.services.discovery.url_normalizer import URLNormalizer

from app.services.persistence.publication_persistence_service import (
    PublicationPersistenceService
)


class DiscoveryService:

    def __init__(self):

        # ==================================================
        # Services
        # ==================================================

        self.http = HTTPClient()

        self.detector = PublicationDetector()

        self.category_crawler = CategoryDiscoveryCrawler()

        self.logger = DiscoveryLogger()

        self.report_builder = ReportBuilder()

        self.normalizer = URLNormalizer()

        # Service responsable de PostgreSQL
        self.persistence = PublicationPersistenceService()

    # ==================================================
    # DISCOVERY
    # ==================================================

    def discover(self, connector):

        # --------------------------------------------------
        # Début de la découverte
        # --------------------------------------------------

        started_at = datetime.now()

        metadata = connector.get_metadata()

        self.logger.start(metadata)

        # --------------------------------------------------
        # Création du contexte
        # --------------------------------------------------

        context = DiscoveryContext(

            source=metadata,

            started_at=started_at,

            base_url=connector.get_base_url()

        )

        # --------------------------------------------------
        # Navigation : catégories + pagination si le connecteur les
        # expose, sinon repli sur l'ancienne détection page unique.
        # --------------------------------------------------

        categories = getattr(connector, "get_categories", None)

        if categories and connector.get_categories():

            collection, pages_visited, links_found, format_counts = (
                self._discover_by_categories(connector)
            )

        else:

            collection, pages_visited, links_found, format_counts = (
                self._discover_single_page(connector, context)
            )

        # ==================================================
        # PERSISTENCE PostgreSQL
        # ==================================================

        persistence_result = self.persistence.save_collection(

            collection

        )

        print()

        print("=" * 60)
        print("PERSISTENCE")
        print("=" * 60)

        print(
            "Publications enregistrées :",
            persistence_result["saved"]
        )

        print(
            "Doublons :",
            persistence_result["duplicates"]
        )

        print(
            "Erreurs :",
            persistence_result["failed"]
        )

        print("=" * 60)

        # ==================================================
        # STATISTIQUES
        # ==================================================

        statistics = DiscoveryStatistics(

            pages_visited=pages_visited,

            links_found=links_found,

            publications_found=len(collection),

            duplicates_removed=persistence_result["duplicates"],

            pdf_count=format_counts.get("pdf_count", 0),

            excel_count=format_counts.get("excel_count", 0),

            csv_count=format_counts.get("csv_count", 0),

            html_count=format_counts.get("html_count", 0)

        )

        # ==================================================
        # RAPPORT
        # ==================================================

        report = DiscoveryReport(

            source=connector.get_name(),

            started_at=started_at,

            finished_at=datetime.now(),

            success=True,

            statistics=statistics,

            message="Découverte terminée avec succès."

        )

        # --------------------------------------------------
        # Logger
        # --------------------------------------------------

        self.logger.end(report)

        # --------------------------------------------------
        # Affichage du rapport
        # --------------------------------------------------

        print(

            self.report_builder.build(report)

        )

        # ==================================================
        # RESULTAT FINAL
        # ==================================================

        return DiscoveryResult(

            publications=collection,

            report=report

        )

    # ==================================================
    # NAVIGATION PAR CATEGORIES + PAGINATION
    # ==================================================

    def _discover_by_categories(self, connector):

        result = self.category_crawler.crawl(connector)

        return (
            result.publications,
            result.pages_visited,
            result.links_found,
            result.format_counts
        )

    # ==================================================
    # ANCIEN COMPORTEMENT : UNE SEULE PAGE
    # (connecteurs qui n'exposent pas encore de catégories)
    # ==================================================

    def _discover_single_page(self, connector, context):

        response = self.http.get(

            context.base_url

        )

        html = response.text

        collection = self.detector.detect(

            html,

            connector.get_id()

        )

        links = self.detector.parser.find_all(

            html,

            "a"

        )

        format_counts = {}

        for publication in collection:

            if publication.metadata is None:

                continue

            file_type = publication.metadata.file_type

            if file_type == "PDF":

                format_counts["pdf_count"] = (
                    format_counts.get("pdf_count", 0) + 1
                )

            elif file_type == "EXCEL":

                format_counts["excel_count"] = (
                    format_counts.get("excel_count", 0) + 1
                )

            elif file_type == "CSV":

                format_counts["csv_count"] = (
                    format_counts.get("csv_count", 0) + 1
                )

            elif file_type == "HTML":

                format_counts["html_count"] = (
                    format_counts.get("html_count", 0) + 1
                )

        return collection, 1, len(links), format_counts
