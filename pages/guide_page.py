"""
Page Objects de l'espace guide.

L'espace guide est le miroir de l'espace hôte : on réutilise donc par héritage
les pages portefeuille et réservations de l'hôte, en changeant simplement le
chemin. Le tableau de bord et la liste des circuits ont leurs propres repères.
"""

from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from pages.host_wallet_page import HostWalletPage
from pages.host_reservations_page import HostReservationsPage


class GuidePage(BasePage):
    DASHBOARD_PATH = "/guide"
    CIRCUITS_PATH = "/guide/circuits"

    DASHBOARD_TITLE = (By.XPATH, "//h1[contains(., 'Tableau de bord Guide')]")
    CIRCUITS_TITLE = (By.XPATH, "//h1[contains(., 'Mes circuits')]")

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


class GuideWalletPage(HostWalletPage):
    """Même page portefeuille que l'hôte, sur le chemin du guide."""
    PATH = "/guide/wallet"


class GuideReservationsPage(HostReservationsPage):
    """Mêmes réservations reçues que l'hôte, sur le chemin du guide."""
    PATH = "/guide/reservations"
