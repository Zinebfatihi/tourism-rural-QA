"""
Tests de RÉGRESSION — catalogue des expériences (parcours touriste).

Couvre les cas du plan de test :
- TC-TOU-04 : recherche / filtres du catalogue
- TC-TOU-05 : consultation de la page détail d'une expérience

Principe : ces tests sont DÉTERMINISTES — ils ne dépendent pas du contenu de
la base. Le catalogue peut être vide (aucune expérience publiée) : dans ce cas
le test qui ouvre une fiche s'ignore proprement (skip) au lieu d'échouer.
"""

import pytest

from pages.experiences_page import ExperiencesPage
from pages.experience_detail_page import ExperienceDetailPage


@pytest.mark.regression
def test_experiences_page_loads(driver):
    """La page catalogue s'affiche (titre visible)."""
    page = ExperiencesPage(driver).load()
    assert page.is_loaded(), "Le catalogue d'expériences ne s'est pas chargé."


@pytest.mark.regression
def test_filter_bar_is_present(driver):
    """TC-TOU-04 : la barre de filtres (région) est présente."""
    page = ExperiencesPage(driver).load()
    assert page.is_filter_bar_present(), "La barre de filtres est absente."


@pytest.mark.regression
def test_catalogue_shows_results_or_empty_state(driver):
    """
    Le catalogue affiche soit des cartes, soit le message « aucune expérience ».
    Valide la logique d'affichage quel que soit le contenu de la base.
    """
    page = ExperiencesPage(driver).load()
    assert page.has_results() or page.is_empty_state_displayed(), (
        "Ni résultats ni message d'état vide : la page ne s'est pas chargée correctement."
    )


@pytest.mark.regression
def test_open_experience_detail(driver):
    """
    TC-TOU-05 : ouvrir la fiche détail de la première expérience.
    S'ignore si le catalogue est vide (aucune fiche à ouvrir).
    """
    page = ExperiencesPage(driver).load()

    if not page.has_results():
        pytest.skip("Catalogue vide : aucune expérience publiée à ouvrir.")

    page.open_first_experience()

    detail = ExperienceDetailPage(driver)
    assert detail.is_loaded(), "La page détail de l'expérience ne s'est pas ouverte."
    assert detail.is_booking_section_displayed(), "Section de réservation absente."
