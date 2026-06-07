"""
Test E2E — parcours HÔTE : créer puis publier une expérience.

Couvre les cas du plan de test :
- TC-HOTE-03 / TC-HOTE-04 : création d'une expérience
- TC-HOTE-05 : publication (DRAFT -> PUBLISHED)

Pré-condition : un compte hôte DÉJÀ vérifié (KYC validé). Ses identifiants
viennent du .env (HOST_EMAIL / HOST_PASSWORD). Si le mot de passe n'est pas
renseigné, le test s'ignore proprement.

Rejouable : chaque exécution crée une expérience au titre unique (horodaté),
donc aucun conflit d'une exécution à l'autre.
"""

from datetime import datetime

import pytest

from config.config import config
from pages.login_page import LoginPage
from pages.host_create_experience_page import HostCreateExperiencePage
from pages.host_experiences_list_page import HostExperiencesListPage


@pytest.mark.e2e
@pytest.mark.regression
def test_host_create_and_publish_experience(driver):
    if not config.HOST_PASSWORD:
        pytest.skip("HOST_PASSWORD non défini dans .env — test hôte ignoré.")

    # 1. Connexion en tant qu'hôte (on attend le token pour être bien authentifié)
    login = LoginPage(driver).load()
    login.login(config.HOST_EMAIL, config.HOST_PASSWORD)
    login.wait.until(lambda d: login.get_token() is not None)

    # 2. Création d'une expérience au titre unique
    title = f"Test Auto {datetime.now():%Y%m%d_%H%M%S}"
    create = HostCreateExperiencePage(driver).load()
    create.fill(
        title=title,
        description="Experience de test automatisee creee par Selenium pour valider le parcours hote.",
    )
    create.submit()

    # Diagnostic : on classe l'issue et on remonte la valeur réelle du champ date
    result = create.wait_result()
    if result != "created":
        date_dom = create.get_value(create.SLOT_DATETIME)
        pytest.fail(
            f"Création non aboutie — résultat='{result}', URL='{create.current_url}', "
            f"date du créneau (valeur réelle dans le champ)='{date_dom}'"
        )

    # 3. Publication via la liste « Mes expériences »
    listing = HostExperiencesListPage(driver)
    assert listing.find_and_publish(title), f"Expérience '{title}' introuvable dans la liste."
    assert listing.is_published(title), "L'expérience n'est pas passée au statut « Publié »."
