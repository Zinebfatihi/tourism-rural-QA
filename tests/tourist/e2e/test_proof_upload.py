"""
Test E2E — parcours TOURISTE : envoi du justificatif de virement.

Couvre TC-TOU-07 : après avoir réservé (par virement), le touriste téléverse
sa preuve de paiement. Démontre l'upload de fichier en Selenium.

Le test crée lui-même sa réservation (réutilise le flux de TC-TOU-06), passe à
la page d'upload, envoie une image générée à la volée, puis vérifie le message
de succès « Preuve envoyée ».

Pré-conditions (sinon skip) : une expérience réservable et une banque configurée.
"""

import base64
import tempfile

import pytest

from pages.experiences_page import ExperiencesPage
from pages.experience_detail_page import ExperienceDetailPage
from pages.reservation_page import ReservationPage
from pages.proof_upload_page import ProofUploadPage

# image PNG 1×1 valide, écrite dans un fichier temporaire pour l'upload
_PNG_1x1 = base64.b64decode(
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAAC0lEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg=="
)


def _make_proof_file() -> str:
    f = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
    f.write(_PNG_1x1)
    f.close()
    return f.name


@pytest.mark.e2e
@pytest.mark.regression
def test_tourist_can_upload_payment_proof(tourist_session):
    driver = tourist_session

    # 1. Trouver une expérience réservable et lancer la réservation
    catalog = ExperiencesPage(driver).load()
    catalog.wait_results_settled()
    hrefs = [a.get_attribute("href") for a in driver.find_elements(*ExperiencesPage.EXPERIENCE_CARDS)]
    if not hrefs:
        pytest.skip("Catalogue vide : aucune expérience à réserver.")

    detail = ExperienceDetailPage(driver)
    reserved = False
    for href in hrefs[:8]:
        driver.get(href)
        detail.wait_slots_settled()
        if detail.has_reservable_slot():
            detail.reserve_first_slot()
            reserved = True
            break
    if not reserved:
        pytest.skip("Aucune expérience avec un créneau à venir.")

    # 2. Créer la réservation (banque + RIB)
    reservation = ReservationPage(driver)
    assert reservation.is_loaded(), "La page de réservation ne s'est pas affichée."
    if not reservation.has_bank_options():
        pytest.skip("Aucune banque configurée côté admin.")
    reservation.select_first_bank()
    reservation.submit()
    assert reservation.is_reservation_created(), "La réservation n'a pas abouti."

    # 3. Passer à la page d'upload et envoyer le justificatif
    reservation.proceed_to_proof()
    proof = ProofUploadPage(driver)
    assert proof.is_loaded(), "La page d'upload du justificatif ne s'est pas affichée."
    proof.upload(_make_proof_file())
    proof.submit()

    # 4. Succès
    assert proof.is_uploaded(), "Le justificatif n'a pas été accepté (message de succès absent)."
