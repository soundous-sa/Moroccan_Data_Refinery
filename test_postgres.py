import psycopg2
import traceback

print("Test de connexion PostgreSQL...")

try:
    conn = psycopg2.connect(
        host="localhost",
        port=5432,
        database="moroccan_data_refinery",
        user="postgres",
        password="admin123"
    )

    print("✅ Connexion réussie !")
    conn.close()

except Exception as e:
    print("\nType d'erreur :", type(e).__name__)
    print("Message :", repr(e))
    print("\nTrace complète :")
    traceback.print_exc()