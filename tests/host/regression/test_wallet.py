"""
Test de RÉGRESSION — portefeuille hôte.

Couvre TC-HOTE-08 : l'hôte accède à son portefeuille et y voit son solde,
le bouton de demande de retrait et la section de ses demandes.

Déterministe : la page s'affiche quel que soit le montant du solde (même 0).
"""

import pytest

from pages.host_wallet_page import HostWalletPage


@pytest.mark.regression
def test_host_wallet_displays_balance(host_session):
    wallet = HostWalletPage(host_session).load()

    assert wallet.is_loaded(), "La page portefeuille (titre + solde) ne s'est pas chargée."
    assert wallet.has_withdraw_button(), "Le bouton « Demander un retrait » est absent."
    assert wallet.has_withdrawals_section(), "La section des demandes de retrait est absente."
