"""
Page Object de la page d'accueil publique (/).

Volontairement minimaliste pour l'instant : on enrichira cette classe quand on
écrira les tests du catalogue et de la navigation (semaines 3-4).
"""

from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class HomePage(BasePage):
    PATH = "/"

    # Le <body> est toujours présent : sert de simple repère « la page a chargé ».
    BODY = (By.TAG_NAME, "body")

    def load(self):
        self.open(self.PATH)
        return self

    def is_loaded(self) -> bool:
        return self.is_visible(self.BODY)
