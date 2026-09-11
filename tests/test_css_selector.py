from app.services.crawler.http_client import HTTPClient
from app.services.discovery.html_parser import HTMLParser


client = HTTPClient()

response = client.get("https://www.hcp.ma")

parser = HTMLParser()

elements = parser.select(

response.text,

"a"

)

print()

print("Nombre :", len(elements))

client.close()