from app.services.discovery.url_normalizer import URLNormalizer

normalizer = URLNormalizer()

base = "https://www.hcp.ma"

urls = [

    "/publication.pdf",

    "publication.pdf",

    "../upload/data.xlsx",

    "https://www.hcp.ma/files/report.pdf"

]

print()

print("=" * 60)

for url in urls:

    print()

    print("Avant :", url)

    print(

        "Après :",

        normalizer.normalize(

            url,

            base

        )

    )

print()

print("=" * 60)