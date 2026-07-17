"""
Page Object du formulaire de modification d'expérience (/host/experiences/{id}/edit).

Formulaire identique à celui de création (mêmes noms `name`, même schéma Zod) :
seuls le titre et le prix sont modifiés ici pour vérifier qu'une mise à jour
réelle est bien prise en compte côté serveur et reflétée dans la liste
« Mes expériences ». Les autres champs (description, ville, créneaux...)
restent pré-remplis tels quels par le formulaire.
"""

from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class HostEditExperiencePage(BasePage):
    TITLE_INPUT = (By.CSS_SELECTOR, "input[name='title']")
    PRICE_INPUT = (By.CSS_SELECTOR, "input[name='price']")
    SUBMIT = (By.XPATH, "//button[contains(., 'Enregistrer')]")
    SUCCESS_TOAST = (By.XPATH, "//*[contains(text(), 'Expérience mise à jour')]")
    ERROR_TOAST = (By.XPATH, "//*[contains(text(), 'Erreur de sauvegarde')]")

    def is_loaded(self) -> bool:
        return self.is_visible(self.TITLE_INPUT, timeout=8)

    def update_title_and_price(self, new_title: str, new_price: int):
        """Vide puis remplit le titre et le prix, sans toucher aux autres champs."""
        self.type(self.TITLE_INPUT, new_title)
        self.type(self.PRICE_INPUT, str(new_price))
        self.click(self.SUBMIT)

        # La sauvegarde redirige vers /host/experiences en cas de succès ;
        # on attend soit le toast de succès, soit celui d'erreur, pour ne
        # jamais rester bloqué en cas d'échec silencieux.
        if not self.is_visible(self.SUCCESS_TOAST, timeout=8):
            if self.is_visible(self.ERROR_TOAST, timeout=2):
                raise AssertionError("La sauvegarde de l'expérience a échoué (toast d'erreur).")
            raise AssertionError("Aucune confirmation de sauvegarde reçue (ni succès ni erreur).")
