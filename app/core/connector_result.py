from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class ConnectorResult:

    connector: str

    discovered: int = 0

    downloaded: int = 0

    parsed: int = 0

    failed: int = 0

    execution_time: float = 0

    started_at: datetime = field(default_factory=datetime.now)

    finished_at: datetime | None = None