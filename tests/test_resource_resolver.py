from app.domain.publication_resource import (
    PublicationResource
)

from app.services.crawler.resource_resolver import (
    ResourceResolver
)


print()
print("=" * 60)
print("TEST RESOURCE RESOLVER")
print("=" * 60)


# ==================================================
# Ressource HCP réelle
# ==================================================

resource = PublicationResource(

    title="La documentation technique (métadonnées)",

    url="https://www.hcp.ma/file/230786/",

    source_id="hcp"
)


print()
print("URL demandée :")
print(resource.url)


# ==================================================
# Resolver
# ==================================================

resolver = ResourceResolver()


resolved = resolver.resolve(
    resource.url
)


# ==================================================
# Affichage
# ==================================================

print()
print("============================================================")

print()
print("RESULTAT RESOLUTION")

print()

print(
    "Titre :",
    resolved.title
)

print(
    "URL finale :",
    resolved.url
)

print(
    "Content-Type :",
    resolved.content_type
)

print(
    "Nom fichier :",
    resolved.filename
)

print(
    "Type fichier :",
    resolved.file_type
)

print(
    "Source :",
    resolved.source_id
)

print()

print("=" * 60)
