from app.services.crawler.http_client import HTTPClient
from app.services.discovery.publication_detector import PublicationDetector
from app.services.discovery.publication_filter import PublicationFilter


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

print("Avant filtrage :", collection.count())

print("=" * 60)

filter_engine = PublicationFilter()

filtered = filter_engine.filter(collection)

print()

print("=" * 60)

print("Après filtrage :", filtered.count())

print("=" * 60)

for publication in filtered.all()[:20]:

    print()

    print(publication.title)

    print(publication.url)

client.close()