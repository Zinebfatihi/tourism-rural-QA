"""
Page Object du formulaire de nouvelle réservation d'événement
(/reservations/new/{eventId}) — touriste.

À la soumission, l'application crée d'abord la réservation (statut PENDING,
1er appel API) PUIS enchaîne sur une session de paiement Stripe (2e appel,
domaine externe). Le test n'a pas besoin que ce 2e appel aboutisse : la
réservation existe déjà en base dès que le 1er appel a répondu. En
pratique, l'appel Stripe peut rester bloqué plusieurs dizaines de secondes
dans cet environnement (clé de test probablement factice) sans jamais
rediriger ni afficher d'erreur — on ne dépend donc pas de cette
redirection pour continuer.
"""

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from pages.base_page import BasePage


class NewReservationPage(BasePage):
    TITLE = (By.XPATH, "//h1[contains(., 'Nouvelle réservation')]")
    SLOT_SELECT = (By.TAG_NAME, "select")
    QTY_INPUT = (By.CSS_SELECTOR, "input[type='number']")
    SUBMIT_BTN = (By.XPATH, "//button[contains(., 'Réserver & Payer')]")

    def is_loaded(self) -> bool:
        return self.is_visible(self.TITLE)

    def has_available_slot(self) -> bool:
        # Le <select> contient toujours l'option désactivée "-- Choisir --" ;
        # il faut donc au moins 2 <option> pour qu'un vrai créneau existe.
        options = self.find(self.SLOT_SELECT).find_elements(By.TAG_NAME, "option")
        return len(options) > 1

    def select_first_slot(self):
        Select(self.find(self.SLOT_SELECT)).select_by_index(1)

    def set_quantity(self, qty: int):
        self.type(self.QTY_INPUT, str(qty))

    def submit_and_wait_redirect(self, fallback_wait: int = 5):
        """Soumet le formulaire. Si la redirection Stripe démarre bien,
        tant mieux (preuve immédiate et rapide). Sinon, on laisse un
        court délai fixe pour que le 1er appel (création réelle de la
        réservation) ait eu le temps de se terminer, sans dépendre du
        2e appel (Stripe) qui peut ne jamais aboutir dans cet
        environnement."""
        import time as _time

        url_before = self.current_url
        self.click(self.SUBMIT_BTN)
        try:
            self.wait.until(lambda d: d.current_url != url_before)
        except TimeoutException:
            _time.sleep(fallback_wait)
