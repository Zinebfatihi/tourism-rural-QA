"""
Test de SÉCURITÉ — un hôte ne peut pas accéder à l'espace guide.

Complète TC-HOTE-10 : on vérifie le cloisonnement entre rôles « métier ».
Un hôte n'a pas le rôle GUIDE ; toute tentative d'accès à /guide doit être
redirigée vers l'accueil.
"""

import pytest
from selenium.webdriver.common.by import By

from pages.base_page import BasePage

GUIDE_NAV = (By.XPATH, "//a[contains(@href, '/guide/circuits')]")


@pytest.mark.security
def test_host_cannot_access_guide(host_session):
    page = BasePage(host_session)
    page.open("/guide")

    # rôle insuffisant : redirection hors de /guide
    page.wait.until(lambda d: "/guide" not in d.current_url)

    assert "/guide" not in page.current_url, "Un hôte a pu rester dans l'espace guide."
    assert not page.is_visible(GUIDE_NAV, timeout=3), (
        "La navigation guide est visible pour un compte hôte."
    )
