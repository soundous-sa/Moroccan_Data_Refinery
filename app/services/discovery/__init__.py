class DiscoveryService:

    def __init__(self):

        self.http = HTTPClient()

        self.detector = PublicationDetector()

        self.logger = DiscoveryLogger()

        self.report_builder = ReportBuilder()

        self.normalizer = URLNormalizer()

        self.persistence = PublicationPersistenceService()