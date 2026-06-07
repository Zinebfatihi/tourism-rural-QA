"""
Test de SÉCURITÉ — contrôle d'accès par rôle.

Couvre TC-HOTE-10 : un utilisateur non-admin (ici un hôte) ne doit pas pouvoir
accéder à l'espace d'administration. La plateforme redirige les non-admins vers
l'accueil ; on vérifie donc qu'après une tentative d'accès à /admin :
- l'URL ne contient plus /admin (redirection effectuée)
- la barre latérale d'administration n'est pas affichée
"""

import pytest
from selenium.webdriver.common.by import By

from pages.base_page import BasePage

ADMIN_SIDEBAR = (By.XPATH, "//a[contains(., 'Tableau de bord')]")


@pytest.mark.security
def test_host_cannot_access_admin(host_session):
    page = BasePage(host_session)
    page.open("/admin")

    # un non-admin est redirigé : l'URL ne doit plus contenir /admin
    page.wait.until(lambda d: "/admin" not in d.current_url)

    assert "/admin" not in page.current_url, "Un hôte a pu rester sur /admin."
    assert not page.is_visible(ADMIN_SIDEBAR, timeout=3), (
        "La barre d'administration est visible pour un compte hôte."
    )
