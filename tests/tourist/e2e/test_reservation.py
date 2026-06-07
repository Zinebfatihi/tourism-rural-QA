"""
Test E2E — parcours TOURISTE : réserver une expérience.

Couvre TC-TOU-06 : un touriste connecté réserve un créneau d'une expérience
publiée (réservation par virement), jusqu'à l'obtention du bon de virement (RIB).

Pré-conditions (sinon le test s'ignore proprement) :
- au moins une expérience publiée avec un créneau à venir (bouton « Réserver ») ;
- au moins une banque configurée côté admin (sélecteur de banque non vide).

Le test ne va pas jusqu'à l'upload de la preuve de virement (étape distincte).
"""

import pytest
from selenium.webdriver.common.by import By

from pages.experiences_page import ExperiencesPage
from pages.experience_detail_page import ExperienceDetailPage
from pages.reservation_page import ReservationPage


@pytest.mark.e2e
@pytest.mark.regression
def test_tourist_can_reserve_experience(tourist_session):
    driver = tourist_session

    # 1. Catalogue : récupérer les liens des expériences
    catalog = ExperiencesPage(driver).load()
    catalog.wait_results_settled()
    hrefs = [a.get_attribute("href") for a in driver.find_elements(*ExperiencesPage.EXPERIENCE_CARDS)]
    if not hrefs:
        pytest.skip("Catalogue vide : aucune expérience à réserver.")

    # 2. Trouver une expérience réservable (créneau à venir) et lancer la réservation
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
        pytest.skip("Aucune expérience avec un créneau à venir (bouton « Réserver »).")

    # 3. Page d'initialisation : choisir une banque puis obtenir le RIB
    reservation = ReservationPage(driver)
    assert reservation.is_loaded(), "La page de réservation ne s'est pas affichée."
    if not reservation.has_bank_options():
        pytest.skip("Aucune banque configurée côté admin : réservation impossible.")

    reservation.select_first_bank()
    reservation.submit()

    # 4. Succès : le bon de virement (RIB) s'affiche
    assert reservation.is_reservation_created(), (
        "La réservation n'a pas abouti (bon de virement non affiché)."
    )
