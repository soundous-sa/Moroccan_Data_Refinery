from datetime import datetime

from sqlalchemy import text

from app.config.database import engine
from app.domain.publication import Publication
from app.domain.sector import Sector
from app.domain.category import Category

class PublicationRepository:

    def __init__(self):
        self.engine = engine

    # ==========================================================
    # Vérifier si une publication existe
    # ==========================================================

    def exists(self, url: str) -> bool:

        query = text("""
            SELECT EXISTS (
                SELECT 1
                FROM publications
                WHERE url = :url
            )
        """)

        with self.engine.connect() as connection:

            result = connection.execute(
                query,
                {
                    "url": url
                }
            )

            return result.scalar()

    # ==========================================================
    # Récupérer une publication par URL
    # ==========================================================

    def get_by_url(self, url):

        query = text("""
            SELECT
                id,
                title,
                publication_date,
                url,
                source_id,
                sector,
                category,
                status,
                created_at,
                updated_at
            FROM publications
            WHERE url = :url
            LIMIT 1
        """)

        with self.engine.connect() as connection:

            result = connection.execute(
                query,
                {
                    "url": url
                }
            )

            row = result.fetchone()

            if row is None:
                return None

            return dict(row._mapping)

    # ==========================================================
    # Récupérer une publication par ID
    # ==========================================================

    def get_by_id(self, publication_id):

        query = text("""
            SELECT
                id,
                title,
                publication_date,
                url,
                source_id,
                sector,
                category,
                status,
                created_at,
                updated_at
            FROM publications
            WHERE id = :publication_id
        """)

        with self.engine.connect() as connection:

            result = connection.execute(
                query,
                {
                    "publication_id": publication_id
                }
            )

            row = result.fetchone()

            if row is None:
                return None

            return dict(row._mapping)

    # ==========================================================
    # Enregistrer une publication
    # ==========================================================

    def save(self, publication):

        now = datetime.now()

        query = text("""
            INSERT INTO publications (
                title,
                publication_date,
                url,
                source_id,
                sector,
                category,
                status,
                created_at,
                updated_at
            )
            VALUES (
                :title,
                :publication_date,
                :url,
                :source_id,
                :sector,
                :category,
                :status,
                :created_at,
                :updated_at
            )
            RETURNING id
        """)

        with self.engine.begin() as connection:

            result = connection.execute(
                query,
                {
                    "title": publication.title,
                    "publication_date": publication.publication_date,
                    "url": publication.url,
                    "source_id": publication.source_id,
                    "sector": publication.sector.value,
                    "category": publication.category.value,
                    "status": "DISCOVERED",
                    "created_at": now,
                    "updated_at": now
                }
            )

            publication_id = result.scalar()

            # Important :
            # on remet l'ID PostgreSQL dans l'objet Python
            publication.id = publication_id

            return publication_id

    # ==========================================================
    # Modifier le statut d'une publication
    # ==========================================================

    def update_status(
        self,
        publication_id: int,
        old_status,
        new_status
    ) -> bool:

        query = text("""
            UPDATE publications
            SET
                status = :new_status,
                updated_at = :updated_at
            WHERE
                id = :publication_id
                AND status = :old_status
        """)

        now = datetime.now()

        with self.engine.begin() as connection:

            result = connection.execute(
                query,
                {
                    "publication_id": publication_id,
                    "old_status": old_status.value
                        if hasattr(old_status, "value")
                        else old_status,
                    "new_status": new_status.value
                        if hasattr(new_status, "value")
                        else new_status,
                    "updated_at": now
                }
            )

            return result.rowcount == 1



        
    def get_publication_by_id(self, publication_id):

            data = self.get_by_id(publication_id)

            if data is None:
                return None

            return Publication(

                id=data["id"],

                title=data["title"],

                publication_date=data["publication_date"],

                url=data["url"],

                source_id=data["source_id"],

                sector=Sector(data["sector"]),

                category=Category(data["category"])

            )

    # ==========================================================
    # Récupérer les publications d'une source par statut
    # ==========================================================

    def find_by_status(self, source_id, status):

        query = text("""
            SELECT
                id,
                title,
                publication_date,
                url,
                source_id,
                sector,
                category,
                status,
                created_at,
                updated_at
            FROM publications
            WHERE source_id = :source_id
                AND status = :status
            ORDER BY id
        """)

        with self.engine.connect() as connection:

            result = connection.execute(
                query,
                {
                    "source_id": source_id,
                    "status": status
                }
            )

            return [
                dict(row._mapping)
                for row in result.fetchall()
            ]

    # ==========================================================
    # Récupérer toutes les publications
    # ==========================================================

    def find_all(self):

        query = text("""
            SELECT
                id,
                title,
                publication_date,
                url,
                source_id,
                sector,
                category,
                status,
                created_at,
                updated_at
            FROM publications
            ORDER BY id
        """)

        with self.engine.connect() as connection:

            result = connection.execute(query)

            return result.fetchall()