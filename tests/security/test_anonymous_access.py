"""
Test de SÉCURITÉ — authentification requise.

Un visiteur NON connecté qui tente d'accéder à une page protégée
(ex. « Mes réservations ») doit être redirigé vers la page de connexion.
Ce test ne nécessite aucun compte : il utilise un navigateur vierge.
"""

import pytest

from pages.base_page import BasePage


@pytest.mark.security
def test_anonymous_redirected_to_login(driver):
    page = BasePage(driver)
    page.open("/reservations")           # page protégée par authentification

    page.wait.until(lambda d: "/login" in d.current_url)
    assert "/login" in page.current_url, (
        "Un visiteur non connecté n'a pas été redirigé vers la connexion."
    )
