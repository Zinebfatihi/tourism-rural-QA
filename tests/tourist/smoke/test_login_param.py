"""
Test DATA-DRIVEN (paramétré) — connexion refusée pour plusieurs entrées invalides.

Démonstration de @pytest.mark.parametrize : au lieu d'écrire un test par cas,
on écrit UN seul test exécuté autant de fois qu'il y a de jeux de données.
Chaque jeu représente une façon différente de mal se connecter ; dans tous les
cas, le résultat attendu est identique : un message d'erreur, et aucun token JWT.

Couvre TC-TOU-03 (étendu) : robustesse de l'authentification face aux entrées
invalides.
"""

import pytest

from config.config import config
from pages.login_page import LoginPage


# Chaque tuple = (description lisible, email, mot de passe).
# La description sert d'identifiant de cas dans le rapport Pytest (ids=...).
INVALID_LOGINS = [
    ("mot_de_passe_errone",   config.TOURIST_EMAIL,      "MauvaisMotDePasse1!"),
    ("email_inexistant",      "inconnu_xyz@example.com", "NimporteQuoi123!"),
    ("email_malforme",        "pas-un-email",            "NimporteQuoi123!"),
    ("champs_vides",          "",                        ""),
    ("mot_de_passe_vide",     config.TOURIST_EMAIL,      ""),
]


@pytest.mark.negative
@pytest.mark.parametrize(
    "cas, email, password",
    INVALID_LOGINS,
    ids=[c[0] for c in INVALID_LOGINS],
)
def test_login_is_rejected_for_invalid_inputs(driver, cas, email, password):
    """Quelle que soit l'entrée invalide, la connexion doit échouer sans token."""
    login = LoginPage(driver).load()
    login.login(email, password)

    # 1) Aucun token JWT ne doit avoir été stocké (preuve qu'on n'est pas connecté).
    assert login.get_token() is None, (
        f"[{cas}] Un token a été stocké alors que la connexion aurait dû échouer."
    )

    # 2) On doit toujours être sur la page de connexion (pas de redirection).
    assert "/login" in login.current_url, (
        f"[{cas}] L'utilisateur a quitté /login alors que la connexion a échoué."
    )
