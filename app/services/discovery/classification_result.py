from dataclasses import dataclass


@dataclass
class ClassificationResult:

    score: int

    accepted: bool

    reason: str