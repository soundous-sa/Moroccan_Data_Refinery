from urllib.parse import urlparse


class URLValidator:

    def is_valid(self, url: str) -> bool:

        if not url:
            return False

        parsed = urlparse(url)

        return bool(parsed.scheme and parsed.netloc)