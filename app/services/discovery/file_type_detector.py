from pathlib import Path


class FileTypeDetector:

    TYPES = {

        ".pdf": "PDF",

        ".csv": "CSV",

        ".xls": "EXCEL",

        ".xlsx": "EXCEL",

        ".json": "JSON",

        ".xml": "XML",

        ".zip": "ZIP",

        ".html": "HTML"

    }

    def detect(self, url: str):

        extension = Path(url).suffix.lower()

        return self.TYPES.get(extension, "UNKNOWN")