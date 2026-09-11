from app.domain.publication_collection import PublicationCollection
from app.services.discovery.duplicate_strategy import DuplicateStrategy


class DuplicateDetector:

    def __init__(self):

        self.strategy = DuplicateStrategy.URL

    def remove_duplicates(

        self,

        collection: PublicationCollection

    ) -> PublicationCollection:

        result = PublicationCollection()

        visited = set()

        for publication in collection:

            key = self._build_key(publication)

            if key in visited:

                continue

            visited.add(key)

            result.add(publication)

        return result

    def _build_key(self, publication):

        if self.strategy == DuplicateStrategy.URL:

            return publication.url.lower().strip()

        if self.strategy == DuplicateStrategy.TITLE:

            return publication.title.lower().strip()

        return (

            publication.url.lower().strip()

            +

            publication.title.lower().strip()

        )