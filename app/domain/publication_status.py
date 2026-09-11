from enum import Enum


class PublicationStatus(Enum):

    DISCOVERED = "DISCOVERED"

    DOWNLOADED = "DOWNLOADED"

    PARSED = "PARSED"

    PROCESSED = "PROCESSED"

    FAILED = "FAILED"


