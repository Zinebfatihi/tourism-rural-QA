"""
Tests SMOKE (data-driven) — pages de gestion de l'espace administrateur.

Un seul test paramétré vérifie que chaque page de gestion de l'admin se charge
(titre attendu visible). Couvre des modules jusqu'ici non testés : destinations,
catégories, comptes bancaires, retraits et notifications.

La page « Comptes bancaires » est notamment liée à l'anomalie ANO-05 (sans
banque configurée, aucune réservation n'est possible) : sa supervision est donc
critique.
"""

import pytest
from selenium.webdriver.common.by import By

from pages.base_page import BasePage


# (identifiant lisible, chemin, titre attendu sur la page)
ADMIN_PAGES = [
    ("destinations",   "/admin/destinations",  "Destinations"),
    ("categories",     "/admin/categories",    "Catégories"),
    ("comptes_banque", "/admin/bank-accounts",  "Comptes bancaires"),
    ("retraits",       "/admin/withdrawals",   "Gestion des retraits"),
    ("notifications",  "/admin/notifications", "Notifications"),
]


@pytest.mark.smoke
@pytest.mark.parametrize(
    "cas, path, title",
    ADMIN_PAGES,
    ids=[c[0] for c in ADMIN_PAGES],
)
def test_admin_management_page_loads(admin_session, cas, path, title):
    """Chaque page de gestion admin doit afficher son titre."""
    page = BasePage(admin_session)
    page.open(path)
    title_locator = (
        By.XPATH,
        f"//*[self::h1 or self::h2][contains(., \"{title}\")]",
    )
    assert page.is_visible(title_locator), (
        f"[{cas}] La page {path} (titre « {title} ») ne s'est pas chargée."
    )
