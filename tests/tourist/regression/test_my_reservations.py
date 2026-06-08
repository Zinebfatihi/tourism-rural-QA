"""
Test de RÉGRESSION — le touriste consulte ses réservations.

Couvre TC-TOU : le touriste accède à « Mes réservations par virement » et y voit
ses réservations (avec leur statut), ou un état vide si aucune.

Déterministe : la page se charge dans les deux cas. Lorsqu'au moins une
réservation existe (ex. après le test TC-TOU-06), on vérifie aussi qu'un badge
de statut est bien affiché.
"""

import pytest

from pages.tourist_reservations_page import TouristReservationsPage


@pytest.mark.regression
def test_tourist_sees_their_reservations(tourist_session):
    page = TouristReservationsPage(tourist_session).load()

    assert page.has_reservations() or page.is_empty_state(), (
        "La page des réservations ne s'est pas chargée (ni tableau ni état vide)."
    )

    # si des réservations existent, leur statut doit être affiché
    if page.has_reservations():
        assert page.has_status_badge(), "Aucun badge de statut affiché sur les réservations."
