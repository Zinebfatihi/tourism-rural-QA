"""
Page Object de la liste des événements (/events) — touriste.

Chaque carte a un lien "Voir le détail →" vers /events/{id}. Un filtre par
type (Tous / Informative / Ticketed) est disponible ; seuls les événements
"Ticketed" sont réservables (bannière d'information sur la page).
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from pages.base_page import BasePage


class EventsPage(BasePage):
    PATH = "/events"

    TITLE = (By.XPATH, "//h1[contains(., 'Explorer les événements')]")
    TYPE_FILTER = (By.ID, "typeFilter")
    DETAIL_LINKS = (By.XPATH, "//a[contains(., 'Voir le détail')]")
    EMPTY_MESSAGE = (By.XPATH, "//p[contains(text(), 'Aucun événement trouvé')]")
    LOADING = (By.XPATH, "//span[contains(text(), 'Chargement des données')]")

    def load(self):
        self.open(self.PATH)
        self.find(self.TITLE)
        self.wait_results_settled()
        return self

    def wait_results_settled(self):
        """Attend la fin du chargement : des cartes OU le message « vide »,
        et l'absence du spinner de chargement (évite de lire le DOM pendant
        un refetch React Query déclenché par le changement de filtre)."""
        self.wait.until(
            lambda d: not d.find_elements(*self.LOADING)
            and (d.find_elements(*self.DETAIL_LINKS) or d.find_elements(*self.EMPTY_MESSAGE))
        )

    def filter_ticketed(self):
        Select(self.find(self.TYPE_FILTER)).select_by_value("TICKETED")
        self.wait_results_settled()

    def detail_hrefs(self):
        return [a.get_attribute("href") for a in self.driver.find_elements(*self.DETAIL_LINKS)]
