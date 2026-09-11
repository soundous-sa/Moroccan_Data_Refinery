from app.config.database import engine

from app.persistence.models.publication_model import Base
from app.persistence.models.publication_resource_model import (
    PublicationResourceModel
)


def create_tables():

    Base.metadata.create_all(
        bind=engine
    )

    print("Tables PostgreSQL créées avec succès.")
