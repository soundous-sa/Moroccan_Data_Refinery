from app.config.settings import settings
from app.config.logger import logger
from app.config.database import test_connection

from app.registry.registry_loader import RegistryLoader
from app.loaders.source_loader import SourceLoader

from app.services.discovery.discovery_service import DiscoveryService
from app.services.collection.collection_service import CollectionService


def main():

    # ==================================================
    # 1. Affichage du titre
    # ==================================================

    print("=" * 50)
    print(f"      {settings.APP_NAME}")
    print("=" * 50)

    logger.info("Configuration chargée.")

    # ==================================================
    # 2. Vérification PostgreSQL
    # ==================================================

    if not test_connection():

        logger.error(
            "Impossible de se connecter à PostgreSQL."
        )

        return

    logger.success(
        "Connexion PostgreSQL réussie."
    )

    print()

    logger.info(
        "Application démarrée."
    )

    # ==================================================
    # 3. Chargement des sources YAML
    # ==================================================

    sources = SourceLoader.load_sources()

    print("=" * 50)
    print("Sources détectées")
    print("=" * 50)

    for source in sources:

        print(source)

    print()

    # ==================================================
    # 4. Chargement du Registry
    # ==================================================

    registry = RegistryLoader.load()

    logger.success(
        f"{registry.count()} connecteur(s) chargé(s)."
    )

    print()

    # ==================================================
    # 5. Création du Discovery Service
    # ==================================================

    discovery_service = DiscoveryService()
    collection_service = CollectionService()

    # ==================================================
    # 6. Exécution des connecteurs
    # ==================================================

    for connector in registry.get_connectors():

        print("-" * 50)

        logger.info(
            f"Exécution du connecteur : "
            f"{connector.get_name()}"
        )

        # ==================================================
        # Vérification du connecteur
        # ==================================================

        if not connector.is_enabled():

            logger.warning(
                f"Connecteur désactivé : "
                f"{connector.get_name()}"
            )

            continue

        # ==================================================
        # Discovery
        # ==================================================

        try:

            result = discovery_service.discover(
                connector
            )

            logger.success(
                "Discovery terminée."
            )

            print()

            print(
                f"Publications trouvées : "
                f"{len(result.publications)}"
            )

            print()

        except Exception as e:

            logger.exception(
                f"Erreur pendant la Discovery : {e}"
            )

            continue

        # ==================================================
        # Collection (publications en attente + retry des échecs)
        # ==================================================
        #
        # collect_pending() couvre à la fois les publications tout
        # juste découvertes ce run et d'anciennes lignes restées
        # bloquées en DISCOVERED (ex. run précédent interrompu).

        try:

            pending_results = collection_service.collect_pending(
                connector.get_id()
            )

        except Exception as e:

            pending_results = []

            logger.exception(
                f"Erreur pendant la collecte : {e}"
            )

        try:

            retry_results = collection_service.retry_failed(
                connector.get_id()
            )

        except Exception as e:

            retry_results = []

            logger.exception(
                f"Erreur pendant le retry des échecs : {e}"
            )

        all_results = pending_results + retry_results

        if not all_results:

            logger.info(
                "Aucune publication à collecter."
            )

            print()

            continue

        collected = sum(
            1
            for collection_result in all_results
            if collection_result.success
        )

        failed = len(all_results) - collected

        logger.success(
            f"Collecte terminée : {collected} réussie(s), "
            f"{failed} échouée(s)."
        )

        print()

    # ==================================================
    # 7. Fin
    # ==================================================

    logger.success(
        "Tous les connecteurs ont été traités."
    )

    print()

    print("=" * 50)
    print("Fin de l'exécution")
    print("=" * 50)


if __name__ == "__main__":

    main()