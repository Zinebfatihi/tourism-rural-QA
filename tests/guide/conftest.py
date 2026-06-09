"""
Fixtures partagées par les tests du rôle guide.

`guide_session` ouvre un navigateur, se connecte avec le compte guide et attend
le token, puis renvoie le driver. S'ignore si GUIDE_PASSWORD n'est pas défini.
"""

import pytest

from config.config import config
from pages.login_page import LoginPage


@pytest.fixture
def guide_session(driver):
    if not config.GUIDE_PASSWORD:
        pytest.skip("GUIDE_PASSWORD non défini dans .env — test guide ignoré.")
    login = LoginPage(driver).load()
    login.login(config.GUIDE_EMAIL, config.GUIDE_PASSWORD)
    login.wait.until(lambda d: login.get_token() is not None)
    return driver
