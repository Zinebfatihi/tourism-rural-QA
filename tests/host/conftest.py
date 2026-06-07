"""
Fixtures partagées par les tests du rôle hôte.

`host_session` ouvre un navigateur, se connecte avec le compte hôte et attend
le token, puis renvoie le driver. S'ignore si HOST_PASSWORD n'est pas défini.
"""

import pytest

from config.config import config
from pages.login_page import LoginPage


@pytest.fixture
def host_session(driver):
    if not config.HOST_PASSWORD:
        pytest.skip("HOST_PASSWORD non défini dans .env — test hôte ignoré.")
    login = LoginPage(driver).load()
    login.login(config.HOST_EMAIL, config.HOST_PASSWORD)
    login.wait.until(lambda d: login.get_token() is not None)
    return driver
