"""
Page Object de la page admin de validation KYC (/admin/kyc).

Onglets : « En attente » (SUBMITTED), « Validés », « Refusés ».
Dans l'onglet « En attente » : soit le message « Aucun document en attente »,
soit un tableau d'utilisateurs avec un bouton « Procéder » par ligne, qui ouvre
un panneau latéral contenant le bouton « Valider ».
"""

from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class AdminKycPage(BasePage):
    PATH = "/admin/kyc"

    # Le titre contient un espace insécable : on matche sur « Validation ».
    TITLE = (By.XPATH, "//h1[contains(., 'Validation')]")
    TAB_PENDING = (By.XPATH, "//button[normalize-space()='En attente']")
    EMPTY_PENDING = (By.XPATH, "//p[contains(text(), 'Aucun document en attente')]")
    PROCEED_BTN = (By.XPATH, "//button[normalize-space()='Procéder']")
    PENDING_ROWS = (By.CSS_SELECTOR, "table tbody tr")
    VALIDATE_BTN = (By.XPATH, "//button[contains(., 'Valider')]")

    def load(self):
        self.open(self.PATH)
        self.find(self.TITLE)
        return self

    def is_loaded(self) -> bool:
        return self.is_visible(self.TITLE) and self.is_visible(self.TAB_PENDING)

    def is_pending_empty(self) -> bool:
        return self.is_visible(self.EMPTY_PENDING, timeout=5)

    def has_pending(self) -> bool:
        return len(self.driver.find_elements(*self.PROCEED_BTN)) > 0

    def _pending_emails(self):
        return [r.text for r in self.driver.find_elements(*self.PENDING_ROWS)]

    def validate_first_pending(self) -> str:
        """Valide le premier KYC en attente. Renvoie l'email traité."""
        rows = self.driver.find_elements(*self.PENDING_ROWS)
        email = rows[0].find_elements(By.TAG_NAME, "td")[0].text

        self.click(self.PROCEED_BTN)     # ouvre le panneau latéral
        self.click(self.VALIDATE_BTN)    # valide les documents

        # le KYC validé doit quitter la file d'attente
        self.wait.until(lambda d: email not in self._pending_emails())
        return email
