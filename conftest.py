"""
conftest.py : configuration partagée par tous les tests (vu automatiquement par Pytest).

On y définit :
1. La fixture `driver` : ouvre un navigateur avant chaque test et le ferme après.
2. Un hook qui prend automatiquement une capture d'écran quand un test échoue.
"""

from datetime import datetime

import pytest

from config.config import config
from utilities.driver_factory import create_driver
from utilities.logger import get_logger

log = get_logger("conftest")


@pytest.fixture
def driver():
    """Fournit un navigateur neuf à chaque test, puis le referme."""
    drv = create_driver()
    yield drv
    drv.quit()
    log.info("Navigateur fermé.")


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Après l'exécution d'un test : si la phase 'call' a échoué et qu'un driver
    est disponible, on enregistre une capture d'écran dans screenshots/.
    """
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        drv = item.funcargs.get("driver")
        if drv is not None:
            config.SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)
            filename = f"{item.name}_{datetime.now():%Y%m%d_%H%M%S}.png"
            path = config.SCREENSHOTS_DIR / filename
            try:
                drv.save_screenshot(str(path))
                log.error("Test '%s' échoué — capture : %s", item.name, path)
            except Exception as exc:                       # pragma: no cover
                log.error("Impossible de capturer l'écran : %s", exc)
