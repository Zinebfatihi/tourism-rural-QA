"""
Test E2E — parcours HÔTE : demande de retrait (création + annulation).

Couvre R-18 (matrice de traçabilité, jusqu'ici "✗ Non couvert").

Crée une demande de retrait, vérifie qu'elle apparaît dans « Mes demandes
de retrait » avec le statut PENDING, puis l'annule et vérifie sa disparition
(nettoyage automatique, rejouable).

Pré-condition : compte hôte déjà vérifié (HOST_EMAIL/HOST_PASSWORD dans .env)
ET un solde disponible d'au moins 1 MAD (le backend refuse tout retrait
supérieur au solde réel). Si le solde est nul, le test s'ignore proprement
plutôt que d'échouer — il faudrait qu'une réservation payée ait déjà crédité
ce compte pour pouvoir tester ce parcours.
"""

import time

import pytest

from pages.host_wallet_page import HostWalletPage


@pytest.mark.e2e
@pytest.mark.regression
def test_host_can_request_and_cancel_withdrawal(host_session):
    wallet = HostWalletPage(host_session).load()
    assert wallet.is_loaded(), "La page portefeuille ne s'est pas chargée."

    balance = wallet.get_balance()
    if balance < 1:
        pytest.skip(
            f"Solde insuffisant ({balance} MAD) pour tester une demande de "
            f"retrait — nécessite au moins 1 MAD (réservation payée requise)."
        )

    amount = 1  # montant symbolique minimal, valide dès que le solde ≥ 1
    bank = "CFG Bank"
    rib = f"QA-RIB-{int(time.time())}"

    # 1) CRÉATION
    wallet.create_withdrawal(amount=amount, bank=bank, beneficiary="Bénéficiaire QA", rib=rib)
    assert wallet.has_withdrawal(bank, amount), (
        "La demande de retrait créée n'apparaît pas dans la liste."
    )
    assert wallet.get_withdrawal_status(bank, amount) == "PENDING", (
        "La nouvelle demande n'a pas le statut PENDING attendu."
    )

    # 2) ANNULATION (nettoyage, prouve aussi le parcours d'annulation)
    wallet.cancel_withdrawal(bank, amount)
    assert not wallet.has_withdrawal(bank, amount), (
        "La demande annulée est toujours visible dans la liste."
    )
