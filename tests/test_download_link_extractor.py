from app.services.discovery.download_link_extractor import (
    DownloadLinkExtractor
)

from app.services.crawler.http_client import HTTPClient


PAGE_URL = (
    "https://www.hcp.ma/"
    "Note-d-information-sur-les-comptes-regionaux-de-l-annee-2024_a4333.html"
)

EXPECTED_URLS = {
    "https://www.hcp.ma/attachment/2891118/",
    "https://www.hcp.ma/attachment/2891119/",
    "https://www.hcp.ma/file/248487/",
    "https://www.hcp.ma/file/248485/"
}


extractor = DownloadLinkExtractor()

http = HTTPClient()

response = http.get(PAGE_URL)

resources = extractor.extract(

    response.text,

    response.url,

    "hcp"

)


print()
print("=" * 60)
print("TEST DOWNLOAD LINK EXTRACTOR")
print("=" * 60)


print(
    "Nombre de ressources :",
    len(resources)
)


for resource in resources:

    print()
    print("Titre       :", resource.title)

    print(
        "URL         :",
        resource.url
    )

    print(
        "Type        :",
        resource.file_type
    )

    print(
        "Source      :",
        resource.source_id
    )


print("=" * 60)


found_urls = {
    resource.url
    for resource in resources
}

if found_urls != EXPECTED_URLS:

    raise SystemExit(
        "Ressources inattendues : "
        f"{sorted(found_urls)}"
    )

print("Extraction et filtrage valides.")
