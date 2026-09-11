from app.registry.registry_loader import RegistryLoader


registry = RegistryLoader.load()

print("=" * 60)
print("TEST REGISTRY")
print("=" * 60)

print("Nombre de connecteurs :", registry.count())

for connector in registry.get_connectors():

    print()
    print("ID :", connector.get_id())
    print("Nom :", connector.get_name())
    print("URL :", connector.get_base_url())

print()
print("Recherche HCP :")

hcp = registry.get("hcp")

print(hcp)

print("=" * 60)