from dataclasses import dataclass, field


@dataclass
class HTMLElement:

    tag: str

    text: str

    href: str | None = None

    classes: list[str] = field(default_factory=list)

    identifier: str = ""

    attributes: dict = field(default_factory=dict)