from app.domain.publication_resource import (
    PublicationResource
)

from app.domain.publication import Publication
from app.domain.category import Category
from app.domain.sector import Sector
from datetime import datetime

from app.services.crawler.resource_resolver import (
    ResourceResolver
)

from app.services.download.download_manager import (
    DownloadManager
)


print()
print("=" * 60)
print("TEST DOWNLOAD MANAGER")
print("=" * 60)


# ==================================================
# Ressource HCP
# ==================================================

resource = PublicationResource(

    title="La documentation technique (métadonnées)",

    url="https://www.hcp.ma/file/230786/",

    source_id="hcp"
)


print()
print("RESSOURCE")
print()

print(
    "Titre :",
    resource.title
)

print(
    "URL :",
    resource.url
)


# ==================================================
# RESOLUTION
# ==================================================

resolver = ResourceResolver()

resolved_resource = resolver.resolve(
    resource.url
)


print()
print("RESSOURCE RESOLUE")
print()

print(
    "Nom fichier :",
    resolved_resource.filename
)

print(
    "Type :",
    resolved_resource.file_type
)


# ==================================================
# DOWNLOAD
# ==================================================

download_manager = DownloadManager()

publication = Publication(

    title="Ressource HCP de test",

    publication_date=datetime.now(),

    url=resource.url,

    source_id=resource.source_id,

    sector=Sector.UNKNOWN,

    category=Category.OTHER
)

result = download_manager.download(
    publication,
    resolved_resource
)


# ==================================================
# RESULTAT
# ==================================================

print()
print("=" * 60)
print("RESULTAT DU TELECHARGEMENT")
print("=" * 60)

print()

print(
    "Succès :",
    result.success
)

print(
    "URL :",
    result.url
)

print(
    "Fichier :",
    result.file_path
)

print(
    "Taille :",
    result.file_size,
    "octets"
)

print(
    "Status HTTP :",
    result.status_code
)

print(
    "Erreur :",
    result.error
)

print()
print("=" * 60)
