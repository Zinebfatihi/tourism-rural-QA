"""
BasePage : classe mère de tous les Page Objects.

Le principe du Page Object Model (POM) : chaque page de l'application est
représentée par une classe. Cette classe de base regroupe les actions communes
(cliquer, saisir, attendre un élément...) pour qu'on ne les réécrive jamais.

Tous les accès aux éléments passent par des « explicit waits » : Selenium attend
qu'un élément soit prêt avant d'agir, plutôt que d'utiliser des time.sleep()
fragiles.
"""

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from config.config import config
from utilities.logger import get_logger

log = get_logger("page")


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, config.EXPLICIT_WAIT)

    # ---------- Navigation ----------
    def open(self, path: str = ""):
        """Ouvre une URL relative à BASE_URL (ex. open('/login'))."""
        url = config.BASE_URL.rstrip("/") + "/" + path.lstrip("/")
        log.info("Ouverture de la page : %s", url)
        self.driver.get(url)

    @property
    def current_url(self) -> str:
        return self.driver.current_url

    # ---------- Actions de base ----------
    def find(self, locator):
        """Attend la présence d'un élément et le renvoie."""
        return self.wait.until(EC.presence_of_element_located(locator))

    def click(self, locator):
        """Attend qu'un élément soit cliquable, puis clique."""
        log.info("Clic sur : %s", locator)
        self.wait.until(EC.element_to_be_clickable(locator)).click()

    def type(self, locator, text: str):
        """Saisit du texte dans un champ (après l'avoir vidé)."""
        log.info("Saisie dans %s", locator)
        element = self.wait.until(EC.visibility_of_element_located(locator))
        element.clear()
        element.send_keys(text)

    def get_text(self, locator) -> str:
        return self.wait.until(EC.visibility_of_element_located(locator)).text

    def is_visible(self, locator, timeout: int | None = None) -> bool:
        """True si l'élément devient visible dans le délai, False sinon."""
        try:
            wait = self.wait if timeout is None else WebDriverWait(self.driver, timeout)
            wait.until(EC.visibility_of_element_located(locator))
            return True
        except Exception:
            return False

    # ---------- Attentes utilitaires ----------
    def wait_until_url_changes(self, old_url: str):
        """Attend que l'URL ne soit plus l'ancienne (utile après une action)."""
        self.wait.until(lambda d: d.current_url != old_url)

    # ---------- Accès au localStorage (vérification du token JWT) ----------
    def get_local_storage_item(self, key: str):
        """Renvoie la valeur d'une clé du localStorage (ou None)."""
        return self.driver.execute_script(
            "return window.localStorage.getItem(arguments[0]);", key
        )
