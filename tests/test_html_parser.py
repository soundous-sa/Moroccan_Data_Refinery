from app.services.crawler.http_client import HTTPClient
from app.services.discovery.html_parser import HTMLParser


client = HTTPClient()

response = client.get("https://www.hcp.ma")

parser = HTMLParser()

links = parser.find_all(

response.text,

"a"

)

print()

print("=" * 60)

print("Nombre de liens :", len(links))

print("=" * 60)

for link in links[:10]:

    print()

    print(link)

client.close()