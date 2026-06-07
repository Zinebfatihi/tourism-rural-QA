"""
Page Object des réservations reçues par l'hôte (/host/reservations).

Le titre « Mes réservations » est toujours rendu ; en dessous s'affiche soit un
tableau de réservations, soit le message « Aucune réservation trouvée. ».
Le test reste donc déterministe quelle que soit la présence de données.
"""

from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class HostReservationsPage(BasePage):
    PATH = "/host/reservations"

    TITLE = (By.XPATH, "//h1[contains(., 'Mes réservations')]")
    TABLE = (By.CSS_SELECTOR, "table")
    EMPTY = (By.XPATH, "//*[contains(text(), 'Aucune réservation')]")

    def load(self):
        self.open(self.PATH)
        self.find(self.TITLE)
        return self

    def is_loaded(self) -> bool:
        return self.is_visible(self.TITLE)

    def has_results_or_empty_state(self) -> bool:
        """Vrai dès qu'un tableau OU le message de liste vide est présent."""
        self.wait.until(
            lambda d: d.find_elements(*self.TABLE) or d.find_elements(*self.EMPTY)
        )
        return True
