from dataclasses import dataclass, field

from app.domain.publication import Publication


@dataclass
class PublicationCollection:

    publications: list[Publication] = field(default_factory=list)

    def add(self, publication: Publication):

        self.publications.append(publication)

    def remove(self, publication: Publication):

        self.publications.remove(publication)

    def count(self):

        return len(self.publications)

    def is_empty(self):

        return len(self.publications) == 0

    def clear(self):

        self.publications.clear()

    def all(self):

        return self.publications

    def __iter__(self):

        return iter(self.publications)

    def __len__(self):

        return len(self.publications)