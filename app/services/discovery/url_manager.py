from urllib.parse import urljoin


class URLManager:

    @staticmethod
    def join(base_url, path):

        return urljoin(base_url, path)

    @staticmethod
    def normalize(url):

        return url.strip()

    @staticmethod
    def is_absolute(url):

        return url.startswith(
            (
                "http://",
                "https://"
            )
        )