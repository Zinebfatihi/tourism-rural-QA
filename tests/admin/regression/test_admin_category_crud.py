"""
Test de RÉGRESSION (opération réelle) — CRUD d'une catégorie par l'admin.

Contrairement à un test « la page se charge », celui-ci effectue de vraies
opérations : il CRÉE une catégorie, vérifie qu'elle apparaît dans la liste, puis
la SUPPRIME et vérifie qu'elle a bien disparu. Le test nettoie donc ses propres
données (aucune pollution) et peut être rejoué autant de fois qu'on veut grâce à
un nom unique horodaté.

Couvre TC-ADM-08 : gestion des catégories (création + suppression).
"""

import time

import pytest

from pages.admin_categories_page import AdminCategoriesPage


@pytest.mark.regression
def test_admin_create_and_delete_category(admin_session):
    page = AdminCategoriesPage(admin_session).load()
    assert page.is_loaded(), "La page des catégories ne s'est pas chargée."

    # Nom unique pour éviter tout conflit et permettre de rejouer le test.
    name = f"QA-Cat-{int(time.time())}"

    # 1) CRÉATION
    page.create_category(name, icon="MapPin")
    assert page.has_category(name), (
        "La catégorie créée n'apparaît pas dans la liste."
    )

    # 2) SUPPRESSION (nettoyage)
    page.delete_category(name)
    assert page.is_category_absent(name), (
        "La catégorie n'a pas été supprimée de la liste."
    )
