"""
Page Object des pages d'administration générales (tableau de bord, utilisateurs).

La barre latérale de l'espace admin est toujours présente : le lien
« Tableau de bord » sert de repère fiable pour confirmer qu'on est bien
authentifié en admin et dans l'espace d'administration.
"""

from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class AdminPage(BasePage):
    DASHBOARD_PATH = "/admin"
    USERS_PATH = "/admin/users"

    SIDEBAR_DASHBOARD = (By.XPATH, "//a[contains(., 'Tableau de bord')]")
    TABLE = (By.CSS_SELECTOR, "table")

    def open_dashboard(self):
        self.open(self.DASHBOARD_PATH)
        return self

    def is_dashboard_loaded(self) -> bool:
        return self.is_visible(self.SIDEBAR_DASHBOARD)

    def open_users(self):
        self.open(self.USERS_PATH)
        return self

    def is_users_table_loaded(self) -> bool:
        return self.is_visible(self.TABLE)
