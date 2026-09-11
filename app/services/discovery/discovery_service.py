from datetime import datetime

from app.reports.discovery_report import DiscoveryReport
from app.reports.discovery_statistics import DiscoveryStatistics
from app.reports.report_builder import ReportBuilder

from app.services.crawler.http_client import HTTPClient

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
        # Téléchargement de la page source
        # --------------------------------------------------

        response = self.http.get(

            context.base_url

        )

        html = response.text

        # --------------------------------------------------
        # Détection des publications
        # --------------------------------------------------

        collection = self.detector.detect(

            html,

            connector.get_id()

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

        # --------------------------------------------------
        # Récupération des liens
        # --------------------------------------------------

        links = self.detector.parser.find_all(

            html,

            "a"

        )

        # ==================================================
        # STATISTIQUES
        # ==================================================

        statistics = DiscoveryStatistics(

            pages_visited=1,

            links_found=len(links),

            publications_found=len(collection),

            duplicates_removed=persistence_result["duplicates"]

        )

        # --------------------------------------------------
        # Statistiques par type de fichier
        # --------------------------------------------------

        for publication in collection:

            if publication.metadata is None:

                continue

            file_type = publication.metadata.file_type

            if file_type == "PDF":

                statistics.pdf_count += 1

            elif file_type == "EXCEL":

                statistics.excel_count += 1

            elif file_type == "CSV":

                statistics.csv_count += 1

            elif file_type == "HTML":

                statistics.html_count += 1

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