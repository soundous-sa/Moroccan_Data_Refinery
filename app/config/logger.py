from loguru import logger
import sys

logger.remove()

# La console Windows (cp1252) ne sait pas encoder les accents français,
# l'arabe ou certaines ligatures : on force l'UTF-8 pour éviter les
# UnicodeEncodeError en cours d'exécution (ex. noms de fichiers HCP).
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="backslashreplace")

logger.add(
    sys.stdout,
    level="INFO",
    colorize=True
)

logger.add(
    "logs/application.log",
    rotation="10 MB",
    retention="30 days",
    level="INFO",
    encoding="utf-8"
)