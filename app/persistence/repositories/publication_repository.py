from sqlalchemy import select
from sqlalchemy.orm import Session

from app.persistence.models.publication_model import PublicationModel


class PublicationRepository:

    def __init__(self, session: Session):

        self.session = session

    # ==================================================
    # Vérifier si une publication existe
    # ==================================================

    def exists_by_url(self, url: str) -> bool:

        statement = (
            select(PublicationModel)
            .where(PublicationModel.url == url)
        )

        result = self.session.execute(statement)

        publication = result.scalar_one_or_none()

        return publication is not None

    # ==================================================
    # Ajouter une publication
    # ==================================================

    def add(self, publication: PublicationModel):

        self.session.add(publication)

        self.session.commit()

        self.session.refresh(publication)

        return publication

    # ==================================================
    # Trouver une publication par URL
    # ==================================================

    def find_by_url(self, url: str):

        statement = (
            select(PublicationModel)
            .where(PublicationModel.url == url)
        )

        result = self.session.execute(statement)

        return result.scalar_one_or_none()

    # ==================================================
    # Récupérer toutes les publications
    # ==================================================

    def find_all(self):

        statement = select(PublicationModel)

        result = self.session.execute(statement)

        return result.scalars().all()

    # ==================================================
    # Compter les publications
    # ==================================================

    def count(self) -> int:

        return len(self.find_all())