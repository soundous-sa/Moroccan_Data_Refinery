import re

from urllib.parse import unquote

from app.config.logger import logger

from app.services.crawler.http_client import HTTPClient

from app.domain.publication_resource import PublicationResource


class ResourceResolver:

    def __init__(self):

        self.http = HTTPClient()

    # ==================================================
    # RESOLVE
    # ==================================================

    def resolve(self, url):

        logger.info(
            f"Résolution de la ressource : {url}"
        )

        # ==================================================
        # Télécharger la ressource
        # ==================================================

        response = self.http.get(url)

        # ==================================================
        # URL finale après redirection
        # ==================================================

        final_url = response.url

        # ==================================================
        # HEADERS
        # ==================================================

        content_type = response.headers.get(
            "Content-Type"
        )

        content_disposition = response.headers.get(
            "Content-Disposition"
        )

        # ==================================================
        # NOM DU FICHIER
        # ==================================================

        filename = self._extract_filename(
            content_disposition
        )

        # ==================================================
        # Si aucun nom dans Content-Disposition
        # utiliser l'URL
        # ==================================================

        if not filename:

            filename = self._filename_from_url(
                final_url
            )

        # ==================================================
        # TYPE DU FICHIER
        # ==================================================

        file_type = self._detect_file_type(

            filename=filename,

            content_type=content_type,

            url=final_url
        )

        # ==================================================
        # LOGS
        # ==================================================

        logger.info(
            f"URL finale : {final_url}"
        )

        logger.info(
            f"Content-Type : {content_type}"
        )

        logger.info(
            f"Content-Disposition : "
            f"{content_disposition}"
        )

        logger.info(
            f"Nom fichier : {filename}"
        )

        logger.info(
            f"Type fichier : {file_type}"
        )

        # ==================================================
        # RETOUR
        # ==================================================

        return PublicationResource(

            title=filename,

            url=final_url,

            file_type=file_type,

            content_type=content_type,

            filename=filename

        )

    # ==================================================
    # EXTRAIRE NOM FICHIER
    # ==================================================

    def _extract_filename(
        self,
        content_disposition
    ):

        if not content_disposition:

            return None

        # ==================================================
        # filename*=UTF-8''document.xlsx
        # ==================================================

        match = re.search(

            r"filename\*\s*=\s*UTF-8''([^;]+)",

            content_disposition,

            re.IGNORECASE
        )

        if match:

            filename = unquote(
                match.group(1)
            )

            return self._clean_filename(
                filename
            )

        # ==================================================
        # filename="document.xlsx"
        # ==================================================

        match = re.search(

            r'filename="([^"]+)"',

            content_disposition,

            re.IGNORECASE
        )

        if match:

            return self._clean_filename(
                match.group(1)
            )

        # ==================================================
        # filename=document.xlsx
        # ==================================================

        match = re.search(

            r"filename\s*=\s*([^;]+)",

            content_disposition,

            re.IGNORECASE
        )

        if match:

            return self._clean_filename(
                match.group(1).strip()
            )

        return None

    # ==================================================
    # NOM DEPUIS URL
    # ==================================================

    def _filename_from_url(
        self,
        url
    ):

        if not url:

            return None

        # Supprimer les paramètres
        url_without_query = url.split(
            "?",
            1
        )[0]

        filename = (
            url_without_query
            .rstrip("/")
            .split("/")[-1]
        )

        if not filename:

            return None

        # Une URL comme /file/230786/
        # ne contient pas d'extension
        if "." not in filename:

            return None

        return self._clean_filename(
            unquote(filename)
        )

    # ==================================================
    # NETTOYAGE NOM FICHIER
    # ==================================================

    def _clean_filename(
        self,
        filename
    ):

        if not filename:

            return None

        filename = filename.strip()

        filename = filename.replace(
            "\x00",
            ""
        )

        filename = self._fix_encoding(
            filename
        )

        return filename

    # ==================================================
    # DETECTION TYPE
    # ==================================================

    def _detect_file_type(
        self,
        filename=None,
        content_type=None,
        url=None
    ):

        # ==================================================
        # 1. D'après le nom du fichier
        # ==================================================

        if filename:

            lower_filename = filename.lower()

            if lower_filename.endswith(".pdf"):
                return "PDF"

            if lower_filename.endswith(".xlsx"):
                return "EXCEL"

            if lower_filename.endswith(".xls"):
                return "EXCEL"

            if lower_filename.endswith(".csv"):
                return "CSV"

            if lower_filename.endswith(".doc"):
                return "WORD"

            if lower_filename.endswith(".docx"):
                return "WORD"

            if lower_filename.endswith(".zip"):
                return "ZIP"

            if lower_filename.endswith(".html"):
                return "HTML"

            if lower_filename.endswith(".htm"):
                return "HTML"

        # ==================================================
        # 2. D'après Content-Type
        # ==================================================

        if content_type:

            content_type = (
                content_type
                .lower()
                .split(";")[0]
                .strip()
            )

            if "pdf" in content_type:

                return "PDF"

            if (
                "spreadsheet" in content_type
                or "excel" in content_type
                or "ms-excel" in content_type
                or "officedocument.spreadsheetml"
                in content_type
            ):

                return "EXCEL"

            if (
                "csv" in content_type
                or "comma-separated"
                in content_type
            ):

                return "CSV"

            if (
                "word" in content_type
                or "officedocument.wordprocessingml"
                in content_type
            ):

                return "WORD"

            if "zip" in content_type:

                return "ZIP"

            if "html" in content_type:

                return "HTML"

        # ==================================================
        # 3. D'après URL
        # ==================================================

        if url:

            lower_url = url.lower()

            if lower_url.endswith(".pdf"):
                return "PDF"

            if (
                lower_url.endswith(".xlsx")
                or lower_url.endswith(".xls")
            ):

                return "EXCEL"

            if lower_url.endswith(".csv"):
                return "CSV"

            if (
                lower_url.endswith(".html")
                or lower_url.endswith(".htm")
            ):

                return "HTML"

        return None

    # ==================================================
    # CORRECTION ENCODAGE
    # ==================================================

    def _fix_encoding(
        self,
        text
    ):

        if not text:

            return text

        try:

            return (
                text
                .encode("latin1")
                .decode("utf-8")
            )

        except (
            UnicodeEncodeError,
            UnicodeDecodeError
        ):

            return text