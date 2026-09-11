from dataclasses import dataclass

from app.domain.publication import Publication
from app.domain.file_metadata import FileMetadata


@dataclass
class Dataset:

    publication: Publication

    file: FileMetadata