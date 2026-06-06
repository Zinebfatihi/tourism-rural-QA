"""
Tests SMOKE — connexion.

Objectif de cette première suite : prouver que tout le framework est branché
correctement (config, driver, Page Objects, logger, captures) avec des cas
simples mais réels.

Couvre les cas du plan de test :
- chargement de la page d'accueil et du formulaire de connexion
- connexion valide (preuve : token JWT présent + sortie de /login)
- connexion invalide / TC-TOU-03 (preuve : message d'erreur + aucun token)
"""

import pytest

from config.config import config
from pages.home_page import HomePage
from pages.login_page import LoginPage


@pytest.mark.smoke
def test_home_page_loads(driver):
    """La page d'accueil publique s'affiche."""
    home = HomePage(driver).load()
    assert home.is_loaded(), "La page d'accueil ne s'est pas chargée."


@pytest.mark.smoke
def test_login_page_displays_form(driver):
    """La page /login affiche bien le formulaire de connexion."""
    login = LoginPage(driver).load()
    assert login.is_loaded(), "Le formulaire de connexion n'est pas affiché."


@pytest.mark.smoke
def test_login_with_valid_credentials(driver):
    """
    Connexion avec des identifiants valides.
    Preuve de succès : un token JWT est stocké et on a quitté la page /login.
    """
    login = LoginPage(driver).load()
    url_before = login.current_url

    login.login(config.ADMIN_EMAIL, config.ADMIN_PASSWORD)

    login.wait_until_url_changes(url_before)
    assert "/login" not in login.current_url, "Toujours sur la page de connexion."
    assert login.get_token() is not None, "Aucun token JWT après connexion."


@pytest.mark.smoke
@pytest.mark.negative
def test_login_with_invalid_credentials(driver):
    """
    TC-TOU-03 : connexion refusée avec un mauvais mot de passe.
    Preuve : message d'erreur affiché et aucun token stocké.
    """
    login = LoginPage(driver).load()

    login.login(config.ADMIN_EMAIL, "MauvaisMotDePasse!")

    assert login.is_error_displayed(), "Aucun message d'erreur affiché."
    assert login.get_token() is None, "Un token a été stocké malgré l'échec."
