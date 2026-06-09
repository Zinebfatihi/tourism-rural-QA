"""
Test de SÉCURITÉ — cloisonnement du rôle guide.

Un guide ne doit accéder ni à l'espace admin, ni à l'espace hôte : toute
tentative est redirigée hors de la zone protégée.
"""

import pytest
from selenium.webdriver.common.by import By

from pages.base_page import BasePage

ADMIN_SIDEBAR = (By.XPATH, "//a[contains(., 'Tableau de bord')]")


@pytest.mark.security
def test_guide_cannot_access_admin(guide_session):
    page = BasePage(guide_session)
    page.open("/admin")
    page.wait.until(lambda d: "/admin" not in d.current_url)
    assert "/admin" not in page.current_url, "Un guide a pu rester sur /admin."
    assert not page.is_visible(ADMIN_SIDEBAR, timeout=3), (
        "La barre d'administration est visible pour un compte guide."
    )


@pytest.mark.security
def test_guide_cannot_access_host(guide_session):
    page = BasePage(guide_session)
    page.open("/host")
    page.wait.until(lambda d: "/host" not in d.current_url)
    assert "/host" not in page.current_url, "Un guide a pu accéder à l'espace hôte."
