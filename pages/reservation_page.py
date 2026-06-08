"""
Page Object de la page d'initialisation de réservation (par virement).
URL : /wire-reservations/new/experience/{id}?slot={slotId}

Étapes : choisir une quantité (1 par défaut), sélectionner une banque, puis
cliquer « Obtenir le RIB ». En cas de succès, le bon de virement s'affiche
(« Étape suivante : effectuez le virement »).
"""

from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class ReservationPage(BasePage):
    TITLE = (By.XPATH, "//h1[contains(., 'Réserver')]")
    BANK_OPTIONS = (By.XPATH, "//button[.//img]")          # un bouton-logo par banque
    GET_RIB_BTN = (By.XPATH, "//button[contains(., 'Obtenir le RIB')]")
    SUCCESS = (By.XPATH, "//h2[contains(., 'Étape suivante')] "
                          "| //button[contains(., 'effectué le virement')]")
    PROOF_BTN = (By.XPATH, "//button[contains(., 'effectué le virement')]")

    def is_loaded(self) -> bool:
        return self.is_visible(self.TITLE)

    def has_bank_options(self) -> bool:
        return self.is_visible(self.BANK_OPTIONS, timeout=8)

    def select_first_bank(self):
        self.click(self.BANK_OPTIONS)

    def submit(self):
        self.click(self.GET_RIB_BTN)

    def is_reservation_created(self) -> bool:
        return self.is_visible(self.SUCCESS, timeout=10)

    def proceed_to_proof(self):
        """Clique « J'ai effectué le virement » → page d'upload du justificatif."""
        self.click(self.PROOF_BTN)
        self.wait.until(lambda d: "/proof" in d.current_url)
