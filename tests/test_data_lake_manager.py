from app.services.download.data_lake_manager import DataLakeManager


print("=" * 60)
print("TEST DATA LAKE MANAGER")
print("=" * 60)


manager = DataLakeManager()


raw_path = manager.get_source_directory("hcp")

failed_path = manager.get_failed_directory("hcp")

temp_path = manager.get_temp_directory()


print()

print("RAW     :", raw_path)

print("FAILED  :", failed_path)

print("TEMP    :", temp_path)


print()

print("Data Lake initialisé avec succès.")

print("=" * 60)