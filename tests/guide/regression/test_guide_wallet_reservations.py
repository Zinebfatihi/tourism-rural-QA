"""
Tests de RÉGRESSION — espace guide (portefeuille et réservations reçues).

Réutilisent les pages de l'hôte (mêmes composants côté application), sur les
chemins du guide. Déterministes (s'adaptent à un solde nul ou à une liste vide).
"""

import pytest

from pages.guide_page import GuideWalletPage, GuideReservationsPage


@pytest.mark.regression
def test_guide_wallet_displays_balance(guide_session):
    wallet = GuideWalletPage(guide_session).load()
    assert wallet.is_loaded(), "La page portefeuille (titre + solde) ne s'est pas chargée."
    assert wallet.has_withdraw_button(), "Le bouton « Demander un retrait » est absent."


@pytest.mark.regression
def test_guide_reservations_page_loads(guide_session):
    page = GuideReservationsPage(guide_session).load()
    assert page.is_loaded(), "Le titre « Mes réservations » ne s'est pas affiché."
    assert page.has_results_or_empty_state(), (
        "Ni tableau de réservations ni état vide ne sont apparus."
    )
