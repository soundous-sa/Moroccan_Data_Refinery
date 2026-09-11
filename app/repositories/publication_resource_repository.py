from datetime import datetime

from sqlalchemy import text

from app.config.database import engine


class PublicationResourceRepository:

    def __init__(self):

        self.engine = engine

    # ==================================================
    # CREER OU METTRE A JOUR UNE RESSOURCE
    # ==================================================

    def save_or_update(self, resource):

        now = datetime.now()

        query = text("""
            INSERT INTO publication_resources (
                publication_id,
                title,
                url,
                filename,
                file_type,
                content_type,
                file_path,
                file_size,
                status,
                created_at,
                updated_at
            )
            VALUES (
                :publication_id,
                :title,
                :url,
                :filename,
                :file_type,
                :content_type,
                :file_path,
                :file_size,
                :status,
                :created_at,
                :updated_at
            )
            ON CONFLICT (publication_id, url)
            DO UPDATE SET
                title = EXCLUDED.title,
                filename = EXCLUDED.filename,
                file_type = EXCLUDED.file_type,
                content_type = EXCLUDED.content_type,
                file_path = EXCLUDED.file_path,
                file_size = EXCLUDED.file_size,
                status = EXCLUDED.status,
                updated_at = EXCLUDED.updated_at
            RETURNING id
        """)

        with self.engine.begin() as connection:

            result = connection.execute(
                query,
                {
                    "publication_id": resource.publication_id,
                    "title": resource.title,
                    "url": resource.url,
                    "filename": resource.filename,
                    "file_type": resource.file_type,
                    "content_type": resource.content_type,
                    "file_path": resource.file_path,
                    "file_size": resource.file_size,
                    "status": resource.status,
                    "created_at": now,
                    "updated_at": now
                }
            )

            resource.id = result.scalar()

            return resource.id

    # ==================================================
    # RESSOURCES D'UNE PUBLICATION
    # ==================================================

    def find_by_publication_id(self, publication_id):

        query = text("""
            SELECT
                id,
                publication_id,
                title,
                url,
                filename,
                file_type,
                content_type,
                file_path,
                file_size,
                status,
                created_at,
                updated_at
            FROM publication_resources
            WHERE publication_id = :publication_id
            ORDER BY id
        """)

        with self.engine.connect() as connection:

            result = connection.execute(
                query,
                {"publication_id": publication_id}
            )

            return [
                dict(row._mapping)
                for row in result.fetchall()
            ]
