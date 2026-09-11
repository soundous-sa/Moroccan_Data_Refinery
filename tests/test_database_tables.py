from app.config.database import test_connection
from app.persistence.database import create_tables


print("=" * 60)
print("TEST CREATION DES TABLES")
print("=" * 60)


if not test_connection():

    print("Connexion PostgreSQL impossible.")

    raise SystemExit(1)


print("Connexion PostgreSQL réussie.")


create_tables()


print("Tables publications et publication_resources créées.")
