"""
Test E2E — parcours HÔTE → ADMIN : soumission d'un document KYC.

Couvre R-17 (matrice de traçabilité, jusqu'ici "✗ Non couvert").

1) Le compte hôte téléverse un document (Carte d'identité - Recto) dont le
   statut n'est pas encore « En cours » ou « Validé ». Vérifie que le statut
   passe à « En cours ».
2) Pour rester rejouable (un document déjà « En cours »/« Validé » ne peut
   pas être re-soumis depuis l'interface hôte), le test se reconnecte comme
   admin sur le MÊME navigateur, rejette précisément cette demande, ce qui
   remet le document en statut « Refusé » — prêt pour l'exécution suivante.

Pré-conditions (sinon skip) : HOST_EMAIL/HOST_PASSWORD et ADMIN_EMAIL/
ADMIN_PASSWORD définis dans .env ; le compte hôte ne doit pas être déjà
entièrement vérifié (auquel cas l'appli affiche un tout autre écran, sans
aucun document à soumettre) ; et le document ciblé doit être au statut
« À déposer » ou « Refusé » au moment du test.
"""

import base64
import tempfile

import pytest

from config.config import config
from pages.login_page import LoginPage
from pages.host_kyc_page import HostKycPage
from pages.admin_kyc_page import AdminKycPage

_PNG_1x1 = base64.b64decode(
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAAC0lEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg=="
)


def _make_doc_file() -> str:
    f = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
    f.write(_PNG_1x1)
    f.close()
    return f.name


@pytest.mark.e2e
@pytest.mark.regression
def test_host_can_submit_kyc_document(driver):
    if not config.HOST_PASSWORD:
        pytest.skip("HOST_PASSWORD non défini dans .env — test hôte ignoré.")
    if not config.ADMIN_PASSWORD:
        pytest.skip("ADMIN_PASSWORD non défini dans .env — impossible de nettoyer via l'admin.")

    label = "Recto"

    # 1. Connexion hôte
    login = LoginPage(driver).load()
    login.login(config.HOST_EMAIL, config.HOST_PASSWORD)
    login.wait.until(lambda d: login.get_token() is not None)

    kyc = HostKycPage(driver).load()

    if kyc.is_already_verified():
        pytest.skip(
            "Le compte hôte est déjà entièrement vérifié (KYC approuvé) — "
            "aucun document à soumettre depuis cette interface."
        )
    assert kyc.is_loaded(), "La page KYC ne s'est pas chargée."

    if not kyc.can_upload(label):
        pytest.skip(
            f"Le document « Carte d'identité – {label} » n'est pas au statut "
            f"« À déposer » ou « Refusé » (statut actuel : {kyc.status_of(label)}) "
            f"— impossible de le (re)soumettre pour l'instant."
        )

    # 2. SOUMISSION du document
    kyc.upload(label, _make_doc_file())
    kyc.wait_status(label, "En cours")
    assert kyc.status_of(label) == "En cours", (
        "Le statut du document n'est pas passé à « En cours » après l'envoi."
    )

    # 3. NETTOYAGE : reconnexion en admin sur le même navigateur, pour
    #    rejeter précisément cette demande et rendre le test rejouable.
    driver.execute_script("window.localStorage.clear();")
    login = LoginPage(driver).load()
    login.login(config.ADMIN_EMAIL, config.ADMIN_PASSWORD)
    login.wait.until(lambda d: login.get_token() is not None)

    admin_kyc = AdminKycPage(driver).load()
    admin_kyc.reject_by_email(config.HOST_EMAIL)
