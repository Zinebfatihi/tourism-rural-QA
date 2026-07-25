"""
Test de RÉGRESSION — approbation d'un retrait par l'admin.

Couvre R-30 (matrice de traçabilité, jusqu'ici "✗ Non couvert").

Pré-condition : au moins une demande de retrait dans l'onglet « En attente ».
S'il n'y en a aucune, le test s'ignore proprement (skip) plutôt que
d'échouer — même logique que le test de validation KYC. Pour le voir passer
au vert : un hôte/guide avec un solde positif doit d'abord soumettre une
demande de retrait (voir test_host_withdrawal.py) sans l'annuler.
"""

import pytest

from pages.admin_withdrawals_page import AdminWithdrawalsPage


@pytest.mark.regression
def test_admin_approve_pending_withdrawal(admin_session):
    page = AdminWithdrawalsPage(admin_session).load()

    if not page.has_pending():
        pytest.skip("Aucune demande de retrait en attente à approuver.")

    target = page.approve_first_pending()
    assert target not in page._pending_identities(), (
        "Le retrait approuvé apparaît toujours dans la file d'attente « En attente »."
    )
