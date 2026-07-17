"""
Tests de RÉGRESSION — validation et rejet d'un KYC par l'admin.

Couvre TC-ADM-03 : l'admin valide une demande KYC en attente.
Couvre R-29 (matrice de traçabilité) : l'admin rejette une demande KYC.

Pré-condition (les deux tests) : au moins une demande dans l'onglet
« En attente ». S'il n'y en a aucune, le test s'ignore proprement (skip)
plutôt que d'échouer. Pour le voir passer au vert : soumettre un KYC depuis
un compte hôte/guide non encore validé.
"""

import pytest

from pages.admin_kyc_page import AdminKycPage


@pytest.mark.regression
def test_admin_validate_pending_kyc(admin_session):
    kyc = AdminKycPage(admin_session).load()

    if not kyc.has_pending():
        pytest.skip("Aucun KYC en attente à valider (file d'attente vide).")

    email = kyc.validate_first_pending()
    assert email, "Aucun email récupéré lors de la validation."
    assert email not in kyc._pending_emails(), (
        "Le KYC validé apparaît toujours dans la file d'attente."
    )


@pytest.mark.regression
def test_admin_reject_pending_kyc(admin_session):
    kyc = AdminKycPage(admin_session).load()

    if not kyc.has_pending():
        pytest.skip("Aucun KYC en attente à rejeter (file d'attente vide).")

    email = kyc.reject_first_pending()
    assert email, "Aucun email récupéré lors du rejet."
    assert email not in kyc._pending_emails(), (
        "Le KYC rejeté apparaît toujours dans la file d'attente « En attente »."
    )
