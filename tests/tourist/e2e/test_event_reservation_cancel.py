"""
Test E2E — parcours TOURISTE : création et annulation d'une réservation
d'événement (système Stripe, distinct de la réservation par virement —
voir ANO-06 dans le rapport d'anomalies).

Couvre R-13 (matrice de traçabilité, jusqu'ici "✗ Non couvert").

Contrairement à la réservation par virement, ce système redirige vers
Stripe Checkout dès la création. Le test laisse cette redirection démarrer
(elle prouve que la réservation existe déjà côté serveur), sans aller
jusqu'au paiement, puis revient directement sur « Mes réservations » pour
vérifier le statut PENDING et annuler — nettoyage automatique, rejouable.

Le test commence par annuler toute réservation PENDING déjà existante sur
le compte (résidu d'une exécution précédente interrompue) : le backend
refuse en effet une nouvelle réservation sur un créneau déjà réservé par
le même compte ("Vous avez déjà une réservation pour ce créneau."), et le
frontend n'affichant aucun message dans ce cas (page silencieusement
figée), ce nettoyage préalable est indispensable à la rejouabilité.

Pré-conditions (sinon skip) : au moins un événement Ticketed publié avec
au moins une date disponible.
"""

import pytest

from pages.events_page import EventsPage
from pages.event_detail_page import EventDetailPage
from pages.new_reservation_page import NewReservationPage
from pages.event_reservations_page import EventReservationsPage


@pytest.mark.e2e
@pytest.mark.regression
def test_tourist_can_cancel_event_reservation(tourist_session):
    driver = tourist_session

    # 1. Nettoyage préventif : annule toute réservation PENDING orpheline
    #    d'une exécution précédente (sinon le backend refuse une nouvelle
    #    réservation sur un créneau déjà réservé par ce compte).
    reservations = EventReservationsPage(driver).load()
    reservations.cancel_all_pending()

    # Référence : plus grand ID de réservation existant avant création
    before_id = reservations.max_id()

    # 2. Trouver un événement Ticketed publié avec au moins une date
    events = EventsPage(driver).load()
    events.filter_ticketed()
    hrefs = events.detail_hrefs()
    if not hrefs:
        pytest.skip("Aucun événement Ticketed disponible.")

    detail = EventDetailPage(driver)
    found = False
    for href in hrefs[:8]:
        driver.get(href)
        if detail.is_loaded() and detail.has_available_dates() and detail.has_reserve_button():
            found = True
            break
    if not found:
        pytest.skip("Aucun événement Ticketed avec une date disponible trouvé.")

    # 3. Lancer la réservation
    detail.click_reserve()
    new_res = NewReservationPage(driver)
    assert new_res.is_loaded(), "La page de nouvelle réservation ne s'est pas affichée."
    if not new_res.has_available_slot():
        pytest.skip("Aucun créneau sélectionnable pour cet événement.")
    new_res.select_first_slot()
    new_res.set_quantity(1)
    new_res.submit_and_wait_redirect()  # part vers Stripe (abandonné volontairement)

    # 4. Revenir sur « Mes réservations » et retrouver la nouvelle entrée
    reservations = EventReservationsPage(driver).load()
    new_id = reservations.max_id()
    assert new_id > before_id, "Aucune nouvelle réservation détectée après la création."
    assert reservations.status_of(new_id) == "PENDING", (
        "La réservation créée n'est pas au statut PENDING attendu."
    )

    # 5. ANNULATION (nettoyage, prouve aussi ce parcours)
    reservations.cancel(new_id)
    reservations.wait_status_not(new_id, "PENDING")
    assert reservations.status_of(new_id) != "PENDING", (
        "La réservation annulée est toujours au statut PENDING."
    )
