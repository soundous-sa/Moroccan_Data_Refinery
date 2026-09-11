from enum import Enum


class ConnectorStatus(Enum):
    READY = "READY"
    RUNNING = "RUNNING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"


class DownloadStatus(Enum):
    PENDING = "PENDING"
    DOWNLOADING = "DOWNLOADING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class ParserStatus(Enum):
    NOT_PARSED = "NOT_PARSED"
    PARSED = "PARSED"
    FAILED = "FAILED"