from dataclasses import dataclass


@dataclass
class DataSource:

    id: str

    name: str

    base_url: str

    description: str

    enabled: bool = True