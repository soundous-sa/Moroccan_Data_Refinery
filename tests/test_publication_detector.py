from app.services.crawler.http_client import HTTPClient
from app.services.discovery.publication_detector import PublicationDetector


client = HTTPClient()

response = client.get(

    "https://www.hcp.ma"

)

detector = PublicationDetector()

collection = detector.detect(

    response.text,

    "HCP"

)

print()

print("=" * 60)

print(

    "Nombre de publications détectées :",

    collection.count()

)

print("=" * 60)

for publication in collection.all()[:20]:

    print()

    print("Titre :", publication.title)

    print("URL   :", publication.url)

client.close()