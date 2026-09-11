from app.services.crawler.http_client import HTTPClient
from app.services.discovery.resource_detector import ResourceDetector


class ResourceResolver:

    def __init__(self):

        self.http = HTTPClient()

    def resolve(self, resource):

        try:

            response = self.http.get(
                resource.url
            )

            content_type = response.headers.get(
                "Content-Type"
            )

            resource.content_type = content_type

            file_type = ResourceDetector.detect(
                url=resource.url,
                content_type=content_type
            )

            resource.file_type = file_type

            content_disposition = response.headers.get(
                "Content-Disposition"
            )

            if content_disposition:

                filename = self._extract_filename(
                    content_disposition
                )

                resource.filename = filename

            return resource

        except Exception as error:

            print(
                f"Erreur résolution ressource : {error}"
            )

            return resource

    def _extract_filename(
        self,
        content_disposition
    ):

        value = content_disposition

        parts = value.split(";")

        for part in parts:

            part = part.strip()

            if part.lower().startswith(
                "filename="
            ):

                filename = part.split(
                    "=",
                    1
                )[1]

                return filename.strip(
                    '"'
                )

        return None