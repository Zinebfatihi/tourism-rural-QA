"""
Page Object du portefeuille hôte (/host/wallet).

La page affiche un écran « Chargement… » tant que les données ne sont pas
arrivées, puis le titre « Mon portefeuille », le « Solde disponible » (montant
en MAD), un bouton « Demander un retrait » et la section « Mes demandes de
retrait ». On attend donc le titre, qui n'apparaît qu'une fois chargé.
"""

from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class HostWalletPage(BasePage):
    PATH = "/host/wallet"

    TITLE = (By.XPATH, "//h1[contains(., 'portefeuille')]")
    BALANCE_LABEL = (By.XPATH, "//p[contains(text(), 'Solde disponible')]")
    WITHDRAW_BTN = (By.XPATH, "//button[contains(., 'Demander un retrait')]")
    WITHDRAWALS_SECTION = (By.XPATH, "//h2[contains(., 'demandes de retrait')]")

    def load(self):
        self.open(self.PATH)
        self.find(self.TITLE)          # attend la fin du « Chargement… »
        return self

    def is_loaded(self) -> bool:
        return self.is_visible(self.TITLE) and self.is_visible(self.BALANCE_LABEL)

    def has_withdraw_button(self) -> bool:
        return self.is_visible(self.WITHDRAW_BTN)

    def has_withdrawals_section(self) -> bool:
        return self.is_visible(self.WITHDRAWALS_SECTION)
