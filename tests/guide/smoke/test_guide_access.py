"""
Tests SMOKE — accès à l'espace guide.

Couvre :
- connexion guide + tableau de bord
- affichage de la liste « Mes circuits »

Déterministes : ils vérifient que les pages clés s'affichent.
"""

import pytest

from pages.guide_page import GuidePage


@pytest.mark.smoke
def test_guide_dashboard_loads(guide_session):
    guide = GuidePage(guide_session).open_dashboard()
    assert guide.is_dashboard_loaded(), "Le tableau de bord guide ne s'est pas chargé."


@pytest.mark.smoke
def test_guide_circuits_page_loads(guide_session):
    guide = GuidePage(guide_session).open_circuits()
    assert guide.is_circuits_loaded(), "La page « Mes circuits » ne s'est pas chargée."
