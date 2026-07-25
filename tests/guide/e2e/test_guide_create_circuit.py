"""
Test E2E — parcours GUIDE : création d'un circuit.

Couvre R-24 (matrice de traçabilité, jusqu'ici "✗ Non couvert").

Remplit le formulaire d'informations d'un nouveau circuit, vérifie la
redirection vers l'écran d'édition (preuve de création réussie côté
backend), puis retrouve le circuit dans « Mes circuits » et le supprime
(nettoyage automatique, rejouable).

Pré-condition : compte guide déjà vérifié (GUIDE_EMAIL/GUIDE_PASSWORD dans
.env — KYC guide validé au préalable, sinon cet espace n'est pas accessible).

Hors scope volontaire : le tracé GPS et l'image de couverture (voir
GuideCircuitFormPage pour le détail). Ce test couvre la création des
informations et la suppression, l'essentiel du cycle CRUD.
"""

import time

import pytest

from pages.guide_circuit_form_page import GuideCircuitFormPage
from pages.guide_page import GuidePage


@pytest.mark.e2e
@pytest.mark.regression
def test_guide_can_create_circuit(guide_session):
    title = f"Circuit Test QA {int(time.time())}"

    # 1) CRÉATION
    form = GuideCircuitFormPage(guide_session).load()
    form.fill_and_submit(
        title=title,
        description="Circuit cree automatiquement par Selenium pour valider la creation.",
        difficulty="EASY",
        duration=2,
        price=150,
        capacity=8,
    )
    form.wait_created()

    # 2) VÉRIFICATION dans « Mes circuits »
    guide = GuidePage(guide_session)
    assert guide.find_circuit(title), (
        f"Le circuit '{title}' n'apparaît pas dans « Mes circuits » après création."
    )

    # 3) SUPPRESSION (nettoyage, prouve aussi ce parcours)
    guide.delete_circuit(title)
    assert not guide.find_circuit(title), (
        f"Le circuit '{title}' est toujours visible après suppression."
    )
