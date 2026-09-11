from app.registry.registry_loader import RegistryLoader

from app.services.discovery.discovery_service import (
    DiscoveryService
)


registry = RegistryLoader.load()

connector = registry.get("hcp")

if connector is None:

    raise RuntimeError(
        "Le connecteur HCP n'existe pas dans le Registry."
    )

service = DiscoveryService()

result = service.discover(
    connector
)

print()

print("=" * 60)

print(
    "Nombre de publications :",
    len(result.publications)
)

print(
    "Source :",
    result.report.source
)

print(
    "Succès :",
    result.report.success
)

print("=" * 60)