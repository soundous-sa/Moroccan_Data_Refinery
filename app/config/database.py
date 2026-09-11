from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from app.config.settings import settings


# ==================================================
# URL PostgreSQL
# ==================================================

DATABASE_URL = (
    f"postgresql+psycopg2://"
    f"{settings.DB_USER}:"
    f"{settings.DB_PASSWORD}@"
    f"{settings.DB_HOST}:"
    f"{settings.DB_PORT}/"
    f"{settings.DB_NAME}"
)


# ==================================================
# Engine
# ==================================================

engine = create_engine(
    DATABASE_URL,
    echo=False
)


# ==================================================
# Session
# ==================================================

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)


# ==================================================
# Test connexion
# ==================================================

def test_connection():

    try:

        with engine.connect() as connection:

            connection.execute(
                text("SELECT 1")
            )

        return True

    except Exception as e:

        print("Erreur PostgreSQL :")
        print(type(e).__name__)
        print(str(e))

        return False