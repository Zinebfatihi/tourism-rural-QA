"""
Page Object — gestion des catégories (admin).

Permet une opération CRUD réelle : créer une catégorie via le panneau latéral,
vérifier sa présence dans la liste, puis la supprimer.

La suppression déclenche une boîte de confirmation native (window.confirm). Pour
fiabiliser le test, on neutralise cette confirmation par injection JavaScript
(window.confirm renvoie toujours true) avant de cliquer — technique classique
pour automatiser les confirmations natives.
"""

from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class AdminCategoriesPage(BasePage):
    PATH = "/admin/categories"

    TITLE = (By.XPATH, "//h1[contains(., 'Catégories')]")
    ADD_BTN = (By.XPATH, "//button[contains(., 'Ajouter une catégorie')]")
    # Champs du panneau (repérés par le libellé, car pas d'id ni de name)
    NAME_INPUT = (By.XPATH, "//label[.//span[contains(., 'Nom')]]//input")
    ICON_INPUT = (By.XPATH, "//label[.//span[contains(., 'Icône')]]//input")
    SAVE_BTN = (By.XPATH, "//button[contains(., 'Enregistrer')]")

    def load(self):
        self.open(self.PATH)
        self.find(self.TITLE)
        return self

    def is_loaded(self) -> bool:
        return self.is_visible(self.TITLE)

    # --- locators dépendant d'un nom ---
    def _row_cell(self, name):
        return (By.XPATH, f"//td[normalize-space()=\"{name}\"]")

    def _delete_btn(self, name):
        return (By.XPATH,
                f"//tr[.//td[normalize-space()=\"{name}\"]]//button[@title='Supprimer']")

    # --- opérations ---
    def create_category(self, name: str, icon: str = ""):
        """Ouvre le panneau, saisit le nom (et l'icône), puis enregistre."""
        self.click(self.ADD_BTN)
        self.type(self.NAME_INPUT, name)
        if icon:
            self.type(self.ICON_INPUT, icon)
        self.click(self.SAVE_BTN)

    def has_category(self, name: str, timeout: int = 10) -> bool:
        return self.is_visible(self._row_cell(name), timeout=timeout)

    def delete_category(self, name: str):
        """Supprime la catégorie nommée et attend sa disparition de la liste."""
        # neutralise la confirmation native pour automatiser sans boîte de dialogue
        self.driver.execute_script("window.confirm = function () { return true; };")
        self.click(self._delete_btn(name))
        self.wait.until(lambda d: not d.find_elements(*self._row_cell(name)))

    def is_category_absent(self, name: str) -> bool:
        return len(self.driver.find_elements(*self._row_cell(name))) == 0
