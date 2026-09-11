import requests

from app.config.logger import logger


class HTTPClient:

    def __init__(self):

        self.session = requests.Session()

        self.session.headers.update(
            {
                "User-Agent": (
                    "Mozilla/5.0 "
                    "(Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 "
                    "(KHTML, like Gecko) "
                    "Chrome/138.0 Safari/537.36"
                ),
                "Accept": "*/*",
            }
        )

    # ==================================================
    # GET
    # ==================================================

    def get(self, url):

        logger.info(f"Connexion : {url}")

        response = self.session.get(
            url,
            timeout=30,
            allow_redirects=True
        )

        response.raise_for_status()

        logger.success(
            f"Ressource téléchargée ({response.status_code})"
        )

        logger.debug(
            f"URL finale : {response.url}"
        )

        logger.debug(
            f"Content-Type : {response.headers.get('Content-Type')}"
        )

        logger.debug(
            f"Content-Disposition : "
            f"{response.headers.get('Content-Disposition')}"
        )

        return response

    # ==================================================
    # HEADERS
    # ==================================================

    def get_headers(self, url):

        logger.info(f"Lecture des headers : {url}")

        response = self.session.get(
            url,
            timeout=30,
            allow_redirects=True,
            stream=True
        )

        response.raise_for_status()

        return response.headers

    # ==================================================
    # CLOSE
    # ==================================================

    def close(self):

        self.session.close()