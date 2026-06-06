"""
Logger centralisé.

Fournit une fonction `get_logger()` qui renvoie un logger configuré pour écrire
à la fois dans la console et dans un fichier horodaté sous logs/. Utiliser des
logs (plutôt que des print) permet de comprendre après coup le déroulement et
les échecs d'une exécution — indispensable en CI/CD.
"""

import logging
from datetime import datetime

from config.config import config

# Un seul fichier de log par exécution (nom horodaté)
_LOG_FILE = config.LOGS_DIR / f"run_{datetime.now():%Y%m%d_%H%M%S}.log"

_FORMAT = "%(asctime)s | %(levelname)-7s | %(name)s | %(message)s"


def get_logger(name: str = "qa") -> logging.Logger:
    """Renvoie un logger configuré (idempotent : pas de handlers en double)."""
    logger = logging.getLogger(name)

    if logger.handlers:          # déjà configuré → on le réutilise
        return logger

    logger.setLevel(logging.INFO)
    config.LOGS_DIR.mkdir(parents=True, exist_ok=True)

    formatter = logging.Formatter(_FORMAT)

    # Sortie console
    console = logging.StreamHandler()
    console.setFormatter(formatter)
    logger.addHandler(console)

    # Sortie fichier
    file_handler = logging.FileHandler(_LOG_FILE, encoding="utf-8")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger
