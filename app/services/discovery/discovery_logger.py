from app.config.logger import logger


class DiscoveryLogger:

    def start(self, source):

        logger.info(

            f"Début de la découverte : {source['name']}"

        )

    def end(self, report):

        logger.success(

            f"Découverte terminée : "

            f"{report.statistics.publications_found} publication(s)"

        )