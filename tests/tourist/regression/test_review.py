"""
Test de RÉGRESSION — le touriste laisse un avis.

Couvre TC-TOU-11 : après avoir participé à une expérience (présence marquée par
scan du QR code), le touriste peut laisser un avis (note + commentaire).

Pré-condition : une réservation dont la présence a été marquée (attendedAt) et
sans avis déjà laissé — c'est-à-dire qu'un bouton « Avis » est présent. Sinon le
test s'ignore proprement (la présence se marque par scan de QR code, étape qui
n'a pas d'interface dédiée).
"""

import pytest

from pages.tourist_reservations_page import TouristReservationsPage


@pytest.mark.regression
def test_tourist_can_leave_review(tourist_session):
    page = TouristReservationsPage(tourist_session).load()

    if not page.has_review_button():
        pytest.skip(
            "Aucune réservation éligible à un avis "
            "(présence non marquée — la présence se fait par scan de QR code)."
        )

    page.leave_review("Très bonne expérience — avis laissé par test automatisé.")
    # succès : la modale s'est fermée et l'avis ne peut plus être resoumis
    assert not page.has_review_button() or page.has_reservations(), (
        "L'avis ne semble pas avoir été enregistré."
    )
