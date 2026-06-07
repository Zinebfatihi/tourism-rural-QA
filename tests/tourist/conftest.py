"""
Fixtures partagées par les tests du rôle touriste.

`tourist_session` ouvre un navigateur, se connecte avec le compte touriste et
attend le token, puis renvoie le driver. S'ignore si TOURIST_PASSWORD absent.
"""

import pytest

from config.config import config
from pages.login_page import LoginPage


@pytest.fixture
def tourist_session(driver):
    if not config.TOURIST_PASSWORD:
        pytest.skip("TOURIST_PASSWORD non défini dans .env — test touriste ignoré.")
    login = LoginPage(driver).load()
    login.login(config.TOURIST_EMAIL, config.TOURIST_PASSWORD)
    login.wait.until(lambda d: login.get_token() is not None)
    return driver
