from urllib.parse import urljoin

from app.services.discovery.url_validator import URLValidator


class URLNormalizer:

    def __init__(self):

        self.validator = URLValidator()

    def normalize(

        self,

        url: str,

        base_url: str

    ) -> str:

        if not url:

            return ""

        url = url.strip()

        if self.validator.is_valid(url):

            return url

        return urljoin(base_url, url)