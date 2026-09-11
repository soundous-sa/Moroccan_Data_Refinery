from pathlib import Path


class DataLakeManager:

    def __init__(
        self,
        base_path="data/lake"
    ):

        self.base_path = Path(
            base_path
        )

        self.raw_path = (
            self.base_path / "raw"
        )

        self.failed_path = (
            self.base_path / "failed"
        )

        self.temp_path = (
            self.base_path / "temp"
        )

        self._create_directories()

    # ==================================================
    # CREATION DES DOSSIERS
    # ==================================================

    def _create_directories(self):

        self.raw_path.mkdir(
            parents=True,
            exist_ok=True
        )

        self.failed_path.mkdir(
            parents=True,
            exist_ok=True
        )

        self.temp_path.mkdir(
            parents=True,
            exist_ok=True
        )

    # ==================================================
    # DOSSIER RAW
    # ==================================================

    def get_source_directory(
        self,
        source_id
    ):

        path = (
            self.raw_path /
            source_id
        )

        path.mkdir(
            parents=True,
            exist_ok=True
        )

        return path

    # ==================================================
    # DOSSIER FAILED
    # ==================================================

    def get_failed_directory(
        self,
        source_id
    ):

        path = (
            self.failed_path /
            source_id
        )

        path.mkdir(
            parents=True,
            exist_ok=True
        )

        return path

    # ==================================================
    # DOSSIER TEMP
    # ==================================================

    def get_temp_directory(self):

        return self.temp_path