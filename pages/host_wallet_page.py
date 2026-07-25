"""
Page Object du portefeuille hôte/guide (/host/wallet).

La page affiche un écran « Chargement… » tant que les données ne sont pas
arrivées, puis le titre « Mon portefeuille », le « Solde disponible » (montant
en MAD), un bouton « Demander un retrait » et la section « Mes demandes de
retrait ». On attend donc le titre, qui n'apparaît qu'une fois chargé.

Le clic sur « Demander un retrait » ouvre une modale (WithdrawalModal) avec
4 champs : Montant, Banque (liste déroulante fixe), Bénéficiaire, RIB.
Le tableau des demandes n'affiche que Date / Montant / Banque / Statut /
Commentaire — ni bénéficiaire ni RIB n'y apparaissent, donc on identifie une
demande précise par la combinaison (banque, montant).

Note : la création n'invalide que la query "wallet" (le solde) côté
frontend, pas "withdrawals" (la liste) — la liste ne se met donc pas à jour
en temps réel après création (anomalie constatée). On force un
rafraîchissement de page après création pour contourner ce point. En
revanche, l'annulation invalide correctement la liste : pas besoin de refresh
après cancel_withdrawal.
"""

import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from pages.base_page import BasePage


class HostWalletPage(BasePage):
    PATH = "/host/wallet"

    TITLE = (By.XPATH, "//h1[contains(., 'portefeuille')]")
    BALANCE_LABEL = (By.XPATH, "//p[contains(text(), 'Solde disponible')]")
    WITHDRAW_BTN = (By.XPATH, "//button[contains(., 'Demander un retrait')]")
    WITHDRAWALS_SECTION = (By.XPATH, "//h2[contains(., 'demandes de retrait')]")

    # --- modale de création ---
    AMOUNT_INPUT = (By.XPATH, "//div[./label[contains(normalize-space(), 'Montant')]]/input")
    BANK_SELECT = (By.XPATH, "//div[./label[contains(normalize-space(), 'Banque')]]/select")
    BENEFICIARY_INPUT = (By.XPATH, "//div[./label[contains(normalize-space(), 'Bénéficiaire')]]/input")
    RIB_INPUT = (By.XPATH, "//div[./label[contains(normalize-space(), 'RIB')]]/input")
    CONFIRM_BTN = (By.XPATH, "//button[normalize-space()='Confirmer']")

    # --- modale d'annulation ---
    CONFIRM_CANCEL_BTN = (By.XPATH, "//button[normalize-space()='Oui, annuler']")

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

    def get_balance(self) -> float:
        """Lit le solde affiché (ex. '0,00 MAD' -> 0.0)."""
        el = self.find(self.BALANCE_LABEL)
        # Le montant est dans l'élément juste après le label, dans le même conteneur.
        container = el.find_element(By.XPATH, "./..")
        text = container.text.replace("Solde disponible", "").strip()
        # Garde uniquement les chiffres, la virgule et le point.
        digits = "".join(c for c in text if c.isdigit() or c in ",.")
        return float(digits.replace(",", ".")) if digits else 0.0

    # --- locators dynamiques (dépendent de banque + montant) ---
    def _amount_str(self, amount) -> str:
        # Format affiché par toLocaleString("fr-MA", {style:"currency"}) :
        # virgule décimale, ex. "512,00". On reste sous 1000 dans les tests
        # pour éviter tout séparateur de milliers dans le formatage.
        return f"{amount:.2f}".replace(".", ",")

    def _row(self, bank: str, amount):
        amount_str = self._amount_str(amount)
        return (
            By.XPATH,
            f"//tr[.//td[contains(., \"{bank}\")] and .//td[contains(., '{amount_str}')]]",
        )

    def _cancel_btn(self, bank: str, amount):
        amount_str = self._amount_str(amount)
        return (
            By.XPATH,
            f"//tr[.//td[contains(., \"{bank}\")] and .//td[contains(., '{amount_str}')]]"
            f"//button[@aria-label='Annuler']",
        )

    def _status_cell(self, bank: str, amount):
        amount_str = self._amount_str(amount)
        return (
            By.XPATH,
            f"//tr[.//td[contains(., \"{bank}\")] and .//td[contains(., '{amount_str}')]]/td[4]",
        )

    # --- actions ---
    def create_withdrawal(self, amount, bank: str, beneficiary: str, rib: str):
        """Ouvre la modale, remplit les 4 champs et confirme."""
        self.click(self.WITHDRAW_BTN)
        self.type(self.AMOUNT_INPUT, str(amount))
        Select(self.find(self.BANK_SELECT)).select_by_visible_text(bank)
        self.type(self.BENEFICIARY_INPUT, beneficiary)
        self.type(self.RIB_INPUT, rib)
        self.click(self.CONFIRM_BTN)

        # Contournement de l'anomalie de rafraîchissement (voir docstring).
        time.sleep(1)
        self.driver.refresh()
        self.find(self.TITLE)

    def has_withdrawal(self, bank: str, amount) -> bool:
        return len(self.driver.find_elements(*self._row(bank, amount))) > 0

    def get_withdrawal_status(self, bank: str, amount) -> str:
        els = self.driver.find_elements(*self._status_cell(bank, amount))
        return els[0].text.strip() if els else ""

    def cancel_withdrawal(self, bank: str, amount):
        """Annule la demande (banque, montant) et attend sa disparition."""
        self.click(self._cancel_btn(bank, amount))
        self.click(self.CONFIRM_CANCEL_BTN)
        self.wait.until(lambda d: not d.find_elements(*self._row(bank, amount)))
