"""
Page Objects de l'espace guide.

L'espace guide est le miroir de l'espace hôte : on réutilise donc par héritage
les pages portefeuille et réservations de l'hôte, en changeant simplement le
chemin. Le tableau de bord et la liste des circuits ont leurs propres repères.

Liste des circuits : cartes (pas un tableau), 3 par page. Chaque carte a un
titre (h2), un badge de statut, et — au survol — 2 ou 3 boutons d'action
(publier/dépublier, éditer, supprimer). Ni éditer ni supprimer n'ont
d'attribut aria-label ; on les repère donc par position : dans le conteneur
d'actions, le bouton "éditer" est en réalité un lien (<a>), donc parmi les
<button> restants, le dernier est toujours "supprimer".

La suppression déclenche une boîte de dialogue navigateur native
(window.confirm), qu'on doit accepter via Selenium (switch_to.alert).
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage
from pages.host_wallet_page import HostWalletPage
from pages.host_reservations_page import HostReservationsPage


class GuidePage(BasePage):
    DASHBOARD_PATH = "/guide"
    CIRCUITS_PATH = "/guide/circuits"

    DASHBOARD_TITLE = (By.XPATH, "//h1[contains(., 'Tableau de bord Guide')]")
    CIRCUITS_TITLE = (By.XPATH, "//h1[contains(., 'Mes circuits')]")
    NEXT_BTN = (By.XPATH, "//button[contains(., 'Suiv.')]")
    PAGE_NUMBER = (By.XPATH, "//span[contains(., 'Page')]")

    def open_dashboard(self):
        self.open(self.DASHBOARD_PATH)
        return self

    def is_dashboard_loaded(self) -> bool:
        return self.is_visible(self.DASHBOARD_TITLE)

    def open_circuits(self):
        self.open(self.CIRCUITS_PATH)
        return self

    def is_circuits_loaded(self) -> bool:
        return self.is_visible(self.CIRCUITS_TITLE)

    # --- locators dynamiques (dépendent du titre du circuit) ---
    def _card(self, title: str):
        return (By.XPATH, f"//div[contains(@class,'group') and .//h2[normalize-space()=\"{title}\"]]")

    def _delete_btn(self, title: str):
        return (
            By.XPATH,
            f"//div[contains(@class,'group') and .//h2[normalize-space()=\"{title}\"]]"
            f"//div[contains(@class,'opacity-0')]/button[last()]",
        )

    def _current_page_text(self) -> str:
        els = self.driver.find_elements(*self.PAGE_NUMBER)
        return els[0].text if els else ""

    # --- actions ---
    def find_circuit(self, title: str) -> bool:
        """Cherche un circuit par titre à travers les pages de la liste."""
        self.open(self.CIRCUITS_PATH)
        self.find(self.CIRCUITS_TITLE)

        for _ in range(20):  # garde-fou anti boucle infinie
            if self.driver.find_elements(*self._card(title)):
                return True
            next_btns = self.driver.find_elements(*self.NEXT_BTN)
            if next_btns and next_btns[0].is_enabled():
                current = self._current_page_text()
                next_btns[0].click()
                self.wait.until(lambda d: self._current_page_text() != current)
            else:
                return False
        return False

    def delete_circuit(self, title: str):
        """Supprime le circuit (confirmation navigateur native) et attend sa
        disparition. Suppose que `title` est déjà visible sur la page
        courante (appeler find_circuit juste avant).

        Le bouton est en opacity-0 par défaut (visible seulement au survol
        via group-hover) : Selenium considère ces éléments comme "non
        affichés" et element_to_be_clickable n'aboutit jamais. On localise
        donc juste sa présence, puis on clique via JavaScript, qui ignore
        la visibilité CSS.
        """
        btn = self.find(self._delete_btn(title))
        self.driver.execute_script("arguments[0].click();", btn)
        self.wait.until(EC.alert_is_present())
        self.driver.switch_to.alert.accept()
        self.wait.until(lambda d: not d.find_elements(*self._card(title)))


class GuideWalletPage(HostWalletPage):
    """Même page portefeuille que l'hôte, sur le chemin du guide."""
    PATH = "/guide/wallet"


class GuideReservationsPage(HostReservationsPage):
    """Mêmes réservations reçues que l'hôte, sur le chemin du guide."""
    PATH = "/guide/reservations"
