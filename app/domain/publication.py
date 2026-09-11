from dataclasses import dataclass
from datetime import datetime

from app.domain.category import Category
from app.domain.sector import Sector


@dataclass
class Publication:

    title: str

    publication_date: datetime

    url: str

    source_id: str

    sector: Sector

    category: Category

    id: int | None = None

    metadata: object | None = None