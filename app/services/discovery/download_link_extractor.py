from app.domain.publication_resource import PublicationResource
from app.services.discovery.resource_detector import ResourceDetector
from app.services.discovery.url_normalizer import URLNormalizer


class DownloadLinkExtractor:

    DOWNLOAD_KEYWORDS = [

        "télécharger",
        "telecharger",

        "download",

        "documentation",

        "métadonnées",
        "metadonnees",

        "note méthodologique",
        "note methodologique",

        "questionnaire",

        "microdonnées",
        "microdonnees",

        "stata",

        "spss",

        "csv",

        "excel",

        "xls",

        "xlsx",

        "pdf",

        "données",
        "donnees",

        "rapport"
    ]

    def __init__(self):

        self.normalizer = URLNormalizer()

    # ==================================================
    # EXTRAIRE LES RESSOURCES D'UNE PAGE PUBLICATION
    # ==================================================

    def extract(self, html, base_url, source_id):

        resources = []
        seen_urls = set()

        for link in self._find_links(html):

            if not link.href:
                continue

            title = link.text.strip()

            if not title:
                continue

            url = self.normalizer.normalize(
                link.href,
                base_url
            )

            if not url or url in seen_urls:
                continue

            if not self._is_download_link(title, url):
                continue

            seen_urls.add(url)

            resources.append(
                PublicationResource(
                    title=title,
                    url=url,
                    file_type=ResourceDetector.detect_from_url(url),
                    source_id=source_id
                )
            )

        return resources

    def _is_download_link(
        self,
        title,
        url
    ):

        normalized_url = url.lower()

        # Page d'index HCP de publications, et non fichier à télécharger.
        # Exemple : /downloads/?tag=Dernières+parutions
        if "/downloads/" in normalized_url and "tag=" in normalized_url:
            return False

        file_type = ResourceDetector.detect_from_url(
            url
        )

        # Une page HTML (contact, navigation, accueil...) n'est pas une
        # ressource téléchargeable, même si son texte contient un mot-clé.
        if file_type == "HTML":
            return False

        # Un fichier avec extension reconnue est une ressource directe.
        if file_type:
            return True

        # HCP expose certains fichiers sans extension dans leur URL.
        if (
            "/file/" in normalized_url
            or "/attachment/" in normalized_url
        ):

            return True

        text = f"{title} {url}".lower()

        return any(
            keyword in text
            for keyword in self.DOWNLOAD_KEYWORDS
        )

    def _find_links(self, html):

        """
        Cette méthode utilise le HTMLParser
        déjà présent dans le projet.
        """

        from app.services.discovery.html_parser import HTMLParser

        parser = HTMLParser()

        return parser.find_all(
            html,
            "a"
        )
