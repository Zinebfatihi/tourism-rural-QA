"""
Test de RÉGRESSION — réservations reçues par l'hôte.

Couvre TC-HOTE-06 : l'hôte accède à la page de ses réservations reçues.
La page affiche soit la liste des réservations, soit un état vide ; le test
vérifie que la page se charge correctement dans les deux cas (déterministe).
"""

import pytest

from pages.host_reservations_page import HostReservationsPage


@pytest.mark.regression
def test_host_reservations_page_loads(host_session):
    page = HostReservationsPage(host_session).load()

    assert page.is_loaded(), "Le titre « Mes réservations » ne s'est pas affiché."
    assert page.has_results_or_empty_state(), (
        "Ni tableau de réservations ni état vide ne sont apparus."
    )
