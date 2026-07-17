"""
Test E2E — parcours HÔTE : modifier une expérience existante.

Crée une expérience dédiée au test (titre unique, rejouable), la modifie
(titre + prix) depuis le formulaire d'édition, puis vérifie que les nouvelles
valeurs sont bien reflétées dans la liste « Mes expériences ».

Pré-condition : un compte hôte DÉJÀ vérifié (KYC validé). Ses identifiants
viennent du .env (HOST_EMAIL / HOST_PASSWORD). Si le mot de passe n'est pas
renseigné, le test s'ignore proprement.

Rejouable : chaque exécution crée sa propre expérience (titre horodaté),
donc aucun conflit d'une exécution à l'autre.
"""

from datetime import datetime

import pytest

from config.config import config
from pages.login_page import LoginPage
from pages.host_create_experience_page import HostCreateExperiencePage
from pages.host_experiences_list_page import HostExperiencesListPage
from pages.host_edit_experience_page import HostEditExperiencePage


@pytest.mark.e2e
@pytest.mark.regression
def test_host_can_edit_experience(driver):
    if not config.HOST_PASSWORD:
        pytest.skip("HOST_PASSWORD non défini dans .env — test hôte ignoré.")

    # 1. Connexion en tant qu'hôte
    login = LoginPage(driver).load()
    login.login(config.HOST_EMAIL, config.HOST_PASSWORD)
    login.wait.until(lambda d: login.get_token() is not None)

    # 2. Création d'une expérience dédiée au test (titre unique)
    original_title = f"Test Edit {datetime.now():%Y%m%d_%H%M%S}"
    create = HostCreateExperiencePage(driver).load()
    create.fill(
        title=original_title,
        description="Experience de test creee par Selenium pour valider la modification.",
        price=300,
    )
    create.submit()

    result = create.wait_result()
    if result != "created":
        date_dom = create.get_value(create.SLOT_DATETIME)
        pytest.fail(
            f"Création préalable non aboutie — résultat='{result}', "
            f"date du créneau='{date_dom}'. Impossible de tester la modification."
        )

    # 3. Ouverture du formulaire de modification depuis la liste
    listing = HostExperiencesListPage(driver)
    assert listing.open_edit(original_title), (
        f"Expérience '{original_title}' introuvable dans la liste pour modification."
    )

    # 4. Modification du titre et du prix
    new_title = original_title + " (modifie)"
    new_price = 450
    edit = HostEditExperiencePage(driver)
    assert edit.is_loaded(), "Le formulaire de modification ne s'est pas chargé."
    edit.update_title_and_price(new_title, new_price)

    # 5. Vérification dans la liste que les nouvelles valeurs sont bien reflétées
    assert listing.find_experience(new_title), (
        f"Le nouveau titre '{new_title}' n'apparaît pas dans la liste après modification."
    )
    price_text = listing.get_price(new_title)
    assert str(new_price) in price_text, (
        f"Le nouveau prix ({new_price}) n'apparaît pas dans la liste (trouvé: '{price_text}')."
    )
