from app.connectors.hcp.connector import HCPConnector


connector = HCPConnector()

print("=" * 60)
print("TEST HCP CONNECTOR")
print("=" * 60)

print("ID              :", connector.get_id())
print("Nom             :", connector.get_name())
print("URL             :", connector.get_base_url())
print("Formats         :", connector.get_allowed_formats())
print("Fréquence       :", connector.get_update_frequency())
print("Activé          :", connector.is_enabled())
print("Secteurs        :", connector.get_sectors())

print()
print("Métadonnées :")
print(connector.get_metadata())

print("=" * 60)