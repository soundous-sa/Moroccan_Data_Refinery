from app.domain.publication_collection import PublicationCollection


class PublicationFilter:

    SOCIAL_NETWORKS = [

        "facebook",

        "twitter",

        "linkedin",

        "instagram",

        "youtube"

    ]

    FORBIDDEN_WORDS = [

        "accueil",

        "contact",

        "mentions",

        "plan du site",

        "rss",

        "newsletter",

        "connexion"

    ]

    def filter(

        self,

        collection: PublicationCollection

    ) -> PublicationCollection:

        result = PublicationCollection()

        visited = set()

        for publication in collection:

            if not self._is_valid(publication, visited):

                continue

            visited.add(publication.url)

            result.add(publication)

        return result

    def _is_valid(

        self,

        publication,

        visited

    ):

        if publication.url is None:

            return False

        if publication.url == "":

            return False

        if publication.url in visited:

            return False

        url = publication.url.lower()

        title = publication.title.lower()

        if url.startswith("#"):

            return False

        if url.startswith("javascript"):

            return False

        if self._contains_forbidden_word(title):

            return False

        if self._contains_social_network(url):

            return False

        return True

    def _contains_social_network(

        self,

        url

    ):

        for network in self.SOCIAL_NETWORKS:

            if network in url:

                return True

        return False

    def _contains_forbidden_word(

        self,

        title

    ):

        for word in self.FORBIDDEN_WORDS:

            if word in title:

                return True

        return False