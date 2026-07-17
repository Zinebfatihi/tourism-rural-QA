"""
Page Object — gestion des comptes bancaires (admin).

Opération réelle : ajouter un compte bancaire (RIB, bénéficiaire, banque), le
retrouver dans la liste, puis le supprimer.

Intérêt métier : sans aucun compte bancaire configuré, aucun touriste ne peut
réserver (voir anomalie ANO-05). Ce test automatise donc l'opération qui lève ce
blocage.
"""
import time

from selenium.webdriver.common.by import By

from pages.base_page import BasePage



class AdminBankAccountsPage(BasePage):
    PATH = "/admin/bank-accounts"

    TITLE = (By.XPATH, "//h2[contains(., 'Comptes bancaires')]")
    ADD_BTN = (By.XPATH, "//button[contains(., 'Ajouter un compte')]")
    # Champs du formulaire, repérés par leur libellé (pas d'id ni de name)
    RIB_INPUT = (By.XPATH, "//div[./label[contains(normalize-space(), 'RIB')]]/input")
    BENEF_INPUT = (By.XPATH, "//div[./label[contains(normalize-space(), 'Bénéficiaire')]]/input")
    BANK_INPUT = (By.XPATH, "//div[./label[contains(normalize-space(), 'Banque')]]/input")
    SAVE_BTN = (By.XPATH, "//button[@type='submit']")

    def load(self):
        self.open(self.PATH)
        self.find(self.TITLE)
        return self

    def is_loaded(self) -> bool:
        return self.is_visible(self.TITLE)

    # --- locators dépendant du RIB (unique) ---
    def _row_cell(self, rib):
        return (By.XPATH, f"//td[normalize-space()=\"{rib}\"]")

    def _delete_btn(self, rib):
        return (By.XPATH,
                f"//tr[.//td[normalize-space()=\"{rib}\"]]"
                f"//button[contains(@class,'text-red-600')]")

    # --- opérations ---
    def create_account(self, rib: str, beneficiary: str, bank: str):
        """Remplit les trois champs et enregistre.
        """
        if not self.is_visible(self.RIB_INPUT, timeout=2):
            self.click(self.ADD_BTN)
        self.type(self.RIB_INPUT, rib)
        self.type(self.BENEF_INPUT, beneficiary)
        self.type(self.BANK_INPUT, bank)
        self.click(self.SAVE_BTN)

        # Laisse le temps à la requête POST de partir avant de recharger
        time.sleep(1)
        self.driver.refresh()
        self.find(self.TITLE)

    def has_account(self, rib: str, timeout: int = 10) -> bool:
        return self.is_visible(self._row_cell(rib), timeout=timeout)

    def delete_account(self, rib: str):
        """Supprime le compte identifié par son RIB et attend sa disparition.

        """
        self.click(self._delete_btn(rib))
        time.sleep(1)
        self.driver.refr  esh()
        self.find(self.TITLE)
        self.wait.until(lambda d: not d.find_elements(*self._row_cell(rib)))

    def is_account_absent(self, rib: str) -> bool:
        return len(self.driver.find_elements(*self._row_cell(rib))) == 0
