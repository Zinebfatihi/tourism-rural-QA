"""
Configuration centrale du framework.

Toutes les valeurs paramétrables (URL, navigateur, identifiants, délais) sont
regroupées ici et peuvent être surchargées via un fichier `.env` ou des
variables d'environnement. Cela évite d'éparpiller des valeurs « en dur »
dans le code des tests.
"""

import os
from pathlib import Path

from dotenv import load_dotenv

# Racine du projet (le dossier qui contient ce fichier config/)
BASE_DIR = Path(__file__).resolve().parent.parent

# Charge le fichier .env s'il existe (sinon on garde les valeurs par défaut)
load_dotenv(BASE_DIR / ".env")


def _as_bool(value: str) -> bool:
    return str(value).strip().lower() in {"1", "true", "yes", "y", "on"}


class Config:
    """Paramètres globaux accessibles depuis tout le framework."""

    # --- Application sous test ---
    BASE_URL: str = os.getenv("BASE_URL", "http://localhost:5173")

    # --- Navigateur ---
    BROWSER: str = os.getenv("BROWSER", "chrome").lower()      # chrome | firefox
    HEADLESS: bool = _as_bool(os.getenv("HEADLESS", "false"))   # True en CI/CD

    # --- Délais (en secondes) ---
    EXPLICIT_WAIT: int = int(os.getenv("EXPLICIT_WAIT", "10"))
    PAGE_LOAD_TIMEOUT: int = int(os.getenv("PAGE_LOAD_TIMEOUT", "30"))

    # --- Identifiants de test ---
    # Compte admin créé automatiquement au démarrage du backend.
    ADMIN_EMAIL: str = os.getenv("ADMIN_EMAIL", "admin@saih.com")
    ADMIN_PASSWORD: str = os.getenv("ADMIN_PASSWORD", "Admin123!")

    # --- Dossiers de sortie ---
    REPORTS_DIR: Path = BASE_DIR / "reports"
    SCREENSHOTS_DIR: Path = BASE_DIR / "screenshots"
    LOGS_DIR: Path = BASE_DIR / "logs"


config = Config()
