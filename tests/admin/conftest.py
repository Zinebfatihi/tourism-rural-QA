"""
Fixtures partagées par les tests admin.

`admin_session` ouvre un navigateur, se connecte avec le compte admin et
attend que le token soit présent, puis renvoie le driver prêt à l'emploi.
"""

import pytest

from config.config import config
from pages.login_page import LoginPage


@pytest.fixture
def admin_session(driver):
    login = LoginPage(driver).load()
    login.login(config.ADMIN_EMAIL, config.ADMIN_PASSWORD)
    login.wait.until(lambda d: login.get_token() is not None)
    return driver
