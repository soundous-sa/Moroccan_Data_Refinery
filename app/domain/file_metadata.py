from dataclasses import dataclass


@dataclass
class FileMetadata:

    filename: str

    extension: str

    size: int

    checksum: str

    download_url: str