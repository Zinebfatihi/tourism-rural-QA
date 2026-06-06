"""
Page Object du catalogue d'expériences (/experiences).

Sélecteurs tirés du vrai composant React :
- un titre <h1> « Expériences authentiques »
- une barre de filtres avec deux menus déroulants (région puis ville)
- une grille de cartes ; chaque carte contient un lien vers /experiences/{id}
- un message « Aucune expérience... » quand le catalogue est vide

Note : le catalogue est chargé en asynchrone. La méthode wait_results_settled()
attend la fin du chargement (apparition des cartes OU du message « vide »).
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from pages.base_page import BasePage


class ExperiencesPage(BasePage):
    PATH = "/experiences"

    # --- Locators ---
    TITLE = (By.XPATH, "//h1[contains(., 'Expériences authentiques')]")
    REGION_SELECT = (By.XPATH, "//select[.//option[contains(., 'Toutes les régions')]]")
    CITY_SELECT = (By.XPATH, "//select[.//option[contains(., 'Toutes les villes')]]")
    EXPERIENCE_CARDS = (By.CSS_SELECTOR, "a[href^='/experiences/']")
    EMPTY_MESSAGE = (By.XPATH, "//p[contains(., 'Aucune expérience')]")

    # --- Navigation ---
    def load(self):
        self.open(self.PATH)
        self.find(self.TITLE)          # attend que la page soit affichée
        self.wait_results_settled()
        return self

    def is_loaded(self) -> bool:
        return self.is_visible(self.TITLE)

    def is_filter_bar_present(self) -> bool:
        """True si le filtre région (toujours présent) est dans la page."""
        return len(self.driver.find_elements(*self.REGION_SELECT)) > 0

    # --- Résultats ---
    def wait_results_settled(self):
        """Attend la fin du chargement : des cartes OU le message « vide »."""
        self.wait.until(
            lambda d: d.find_elements(*self.EXPERIENCE_CARDS)
            or d.find_elements(*self.EMPTY_MESSAGE)
        )

    def get_experience_count(self) -> int:
        return len(self.driver.find_elements(*self.EXPERIENCE_CARDS))

    def has_results(self) -> bool:
        return self.get_experience_count() > 0

    def is_empty_state_displayed(self) -> bool:
        return len(self.driver.find_elements(*self.EMPTY_MESSAGE)) > 0

    def open_first_experience(self):
        """Clique sur la première carte du catalogue."""
        self.driver.find_elements(*self.EXPERIENCE_CARDS)[0].click()

    # --- Filtres ---
    def get_available_regions(self) -> list[str]:
        """Liste des régions proposées (hors option « Toutes les régions »)."""
        select = Select(self.find(self.REGION_SELECT))
        return [o.text for o in select.options if "Toutes" not in o.text]

    def select_region(self, region: str):
        Select(self.find(self.REGION_SELECT)).select_by_visible_text(region)
        self.wait_results_settled()
