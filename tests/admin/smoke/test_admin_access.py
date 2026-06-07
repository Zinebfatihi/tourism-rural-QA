"""
Tests SMOKE — accès admin.

Couvre :
- TC-ADM-01 : connexion admin + tableau de bord
- TC-ADM-05 : liste des utilisateurs
- accès à la page de validation KYC

Tous déterministes : ils vérifient que les pages clés s'affichent,
indépendamment du contenu de la base.
"""

import pytest

from pages.admin_page import AdminPage
from pages.admin_kyc_page import AdminKycPage


@pytest.mark.smoke
def test_admin_dashboard_loads(admin_session):
    admin = AdminPage(admin_session).open_dashboard()
    assert admin.is_dashboard_loaded(), "Le tableau de bord admin ne s'est pas chargé."


@pytest.mark.smoke
def test_admin_users_list_loads(admin_session):
    admin = AdminPage(admin_session).open_users()
    assert admin.is_users_table_loaded(), "La liste des utilisateurs ne s'est pas chargée."


@pytest.mark.smoke
def test_admin_kyc_page_loads(admin_session):
    kyc = AdminKycPage(admin_session).load()
    assert kyc.is_loaded(), "La page de validation KYC ne s'est pas chargée."
