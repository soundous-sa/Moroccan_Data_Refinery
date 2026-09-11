from app.services.crawler.http_client import HTTPClient


client = HTTPClient()

response = client.get("https://www.hcp.ma")

print("\n" + "=" * 50)

print("Status :", response.status_code)
print("URL    :", response.url)

print("\nDébut du HTML :\n")

print(response.text[:500])

print("=" * 50)

client.close()