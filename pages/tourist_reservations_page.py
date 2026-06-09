"""
Page Object des réservations du touriste (/wire-reservations).

États possibles :
- « Chargement… » pendant le chargement
- « Aucune réservation par virement. » si la liste est vide
- sinon : titre « Mes réservations par virement » + un tableau dont chaque ligne
  porte un badge de statut (PENDING, RECEIVED, CONFIRMED, REJECTED, CANCELLED).
"""

from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class TouristReservationsPage(BasePage):
    PATH = "/wire-reservations"

    TABLE = (By.CSS_SELECTOR, "table")
    ROWS = (By.CSS_SELECTOR, "table tbody tr")
    EMPTY = (By.XPATH, "//*[contains(text(), 'Aucune réservation par virement')]")
    STATUS_BADGE = (By.XPATH,
        "//table//span[contains(text(),'PENDING') or contains(text(),'RECEIVED') "
        "or contains(text(),'CONFIRMED') or contains(text(),'REJECTED') "
        "or contains(text(),'CANCELLED')]")

    # --- avis (n'apparaît que si la présence a été marquée) ---
    AVIS_BTN = (By.XPATH, "//button[contains(., 'Avis')]")
    REVIEW_TEXTAREA = (By.CSS_SELECTOR, "textarea")
    REVIEW_SUBMIT = (By.XPATH, "//button[contains(., 'Envoyer')]")

    def load(self):
        self.open(self.PATH)
        # on attend la fin du « Chargement… » : tableau OU message de liste vide
        self.wait.until(
            lambda d: d.find_elements(*self.TABLE) or d.find_elements(*self.EMPTY)
        )
        return self

    def has_reservations(self) -> bool:
        return len(self.driver.find_elements(*self.ROWS)) > 0

    def is_empty_state(self) -> bool:
        return self.is_visible(self.EMPTY, timeout=3)

    def has_status_badge(self) -> bool:
        return self.is_visible(self.STATUS_BADGE, timeout=5)

    def has_review_button(self) -> bool:
        return len(self.driver.find_elements(*self.AVIS_BTN)) > 0

    def leave_review(self, comment: str):
        """Ouvre la modale d'avis, saisit un commentaire (note 5/5 par défaut)
        et envoie. Le succès est confirmé par la fermeture de la fenêtre."""
        self.click(self.AVIS_BTN)
        self.type(self.REVIEW_TEXTAREA, comment)
        self.click(self.REVIEW_SUBMIT)
        self.wait.until(lambda d: not d.find_elements(*self.REVIEW_TEXTAREA))
