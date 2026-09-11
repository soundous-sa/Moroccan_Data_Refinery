from urllib.parse import urlparse
import os


class ResourceDetector:

    CONTENT_TYPE_MAP = {

        # PDF
        "application/pdf": "PDF",

        # Excel
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": "XLSX",
        "application/vnd.ms-excel": "XLS",

        # CSV
        "text/csv": "CSV",

        # ZIP
        "application/zip": "ZIP",
        "application/x-zip-compressed": "ZIP",

        # Word
        "application/msword": "DOC",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document": "DOCX",

        # PowerPoint
        "application/vnd.ms-powerpoint": "PPT",
        "application/vnd.openxmlformats-officedocument.presentationml.presentation": "PPTX",

        # Texte
        "text/plain": "TXT",

        # HTML
        "text/html": "HTML",
        "application/xhtml+xml": "HTML",
    }

    EXTENSION_MAP = {

        ".pdf": "PDF",

        ".xlsx": "XLSX",
        ".xls": "XLS",

        ".csv": "CSV",

        ".zip": "ZIP",

        ".doc": "DOC",
        ".docx": "DOCX",

        ".ppt": "PPT",
        ".pptx": "PPTX",

        ".txt": "TXT",

        ".html": "HTML",
        ".htm": "HTML",
    }

    @classmethod
    def detect_from_content_type(cls, content_type):

        if not content_type:
            return None

        content_type = content_type.lower()

        # Supprimer les paramètres éventuels
        # exemple :
        # application/pdf; charset=UTF-8

        content_type = content_type.split(";")[0].strip()

        return cls.CONTENT_TYPE_MAP.get(content_type)

    @classmethod
    def detect_from_url(cls, url):

        if not url:
            return None

        parsed = urlparse(url)

        path = parsed.path.lower()

        _, extension = os.path.splitext(path)

        if not extension:
            return None

        return cls.EXTENSION_MAP.get(extension)

    @classmethod
    def detect(cls, url=None, content_type=None):

        # Priorité au Content-Type
        file_type = cls.detect_from_content_type(
            content_type
        )

        if file_type:
            return file_type

        # Sinon utiliser l'extension
        return cls.detect_from_url(
            url
        )