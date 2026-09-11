from pathlib import Path
import re
from urllib.parse import urlparse

from app.services.crawler.http_client import HTTPClient
from app.services.download.download_result import DownloadResult
from app.services.download.data_lake_manager import DataLakeManager


class DownloadManager:

    def __init__(self):

        self.http = HTTPClient()
        self.data_lake = DataLakeManager()

    # ==================================================
    # NOM DU FICHIER DEPUIS L'URL
    # ==================================================

    def _get_filename(self, url):

        parsed_url = urlparse(url)

        filename = Path(
            parsed_url.path
        ).name

        if not filename:
            filename = "downloaded_file"

        return filename

    # ==================================================
    # NOM COMPATIBLE AVEC LE SYSTEME DE FICHIERS
    # ==================================================

    def _sanitize_filename(self, filename):

        # Content-Disposition peut contenir un nom valide côté serveur mais
        # incompatible avec Windows (notamment le caractère ':').
        sanitized = re.sub(
            r'[<>:"/\\|?*]',
            "_",
            filename
        )

        sanitized = sanitized.rstrip(". ")

        return sanitized or "downloaded_file"

    # ==================================================
    # TELECHARGEMENT
    # ==================================================

    def download(self, publication, resource=None):

        # Une publication peut référencer une page de détail contenant
        # plusieurs fichiers. Lorsqu'une ressource a été résolue, c'est donc
        # son URL (et non celle de la publication) qui doit être téléchargée.
        url = (
            resource.url
            if resource is not None
            else publication.url
        )
        source_id = publication.source_id

        try:

            # ==================================================
            # TELECHARGEMENT HTTP
            # ==================================================

            response = self.http.get(url)

            # ==================================================
            # DETERMINATION DU NOM DU FICHIER
            # ==================================================

            # Priorité au nom détecté par ResourceResolver
            # Exemple HCP :
            #
            # /file/230786/
            #
            # devient :
            #
            # La documentation technique (Métadonnées) :
            # Anonymisation des microdonnées du RGPH 2014.xlsx

            if resource is not None and resource.filename:

                filename = resource.filename

            else:

                filename = self._get_filename(url)

            # ==================================================
            # SECURITE DU NOM DE FICHIER
            # ==================================================

            filename = Path(filename).name

            filename = self._sanitize_filename(
                filename
            )

            if not filename:

                filename = "downloaded_file"

            # ==================================================
            # DOSSIER DE LA SOURCE
            # ==================================================

            source_directory = (
                self.data_lake
                .get_source_directory(
                    source_id
                )
            )

            # ==================================================
            # CHEMIN FINAL
            # ==================================================

            file_path = (
                source_directory /
                filename
            )

            # ==================================================
            # VERIFICATION DU DOUBLON
            # ==================================================

            if file_path.exists():

                return DownloadResult(

                    success=True,

                    url=url,

                    file_path=str(
                        file_path
                    ),

                    file_size=(
                        file_path
                        .stat()
                        .st_size
                    ),

                    status_code=(
                        response.status_code
                    ),

                    error=None
                )

            # ==================================================
            # SAUVEGARDE DU FICHIER
            # ==================================================

            with open(
                file_path,
                "wb"
            ) as file:

                file.write(
                    response.content
                )

            # ==================================================
            # TAILLE DU FICHIER
            # ==================================================

            file_size = (
                file_path
                .stat()
                .st_size
            )

            # ==================================================
            # RESULTAT
            # ==================================================

            return DownloadResult(

                success=True,

                url=url,

                file_path=str(
                    file_path
                ),

                file_size=file_size,

                status_code=(
                    response.status_code
                ),

                error=None
            )

        # ==================================================
        # GESTION DES ERREURS
        # ==================================================

        except Exception as e:

            return DownloadResult(

                success=False,

                url=url,

                file_path=None,

                file_size=0,

                status_code=None,

                error=str(e)
            )
