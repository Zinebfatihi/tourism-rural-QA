"""
Page Object de la fiche détail d'un événement (/events/{id}) — touriste.

La liste des dates disponibles est précédée du titre "Dates disponibles" ;
si aucune date n'existe, un message "Aucune date disponible..." s'affiche
à la place. Le bouton "Réserver" est toujours rendu (même sans date), donc
on vérifie explicitement la présence d'au moins une date avant de l'utiliser.
"""

from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class EventDetailPage(BasePage):
    TITLE = (By.XPATH, "//h1")
    DATE_ITEMS = (By.XPATH, "//h2[contains(., 'Dates disponibles')]/following-sibling::ul/li")
    RESERVE_BTN = (By.XPATH, "//button[normalize-space()='Réserver']")

    def is_loaded(self) -> bool:
        return self.is_visible(self.TITLE)

    def has_available_dates(self) -> bool:
        return len(self.driver.find_elements(*self.DATE_ITEMS)) > 0

    def has_reserve_button(self) -> bool:
        return len(self.driver.find_elements(*self.RESERVE_BTN)) > 0

    def click_reserve(self):
        self.click(self.RESERVE_BTN)
