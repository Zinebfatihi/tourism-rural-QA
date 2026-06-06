"""
Page Object de la page de connexion (/login).

Les locators correspondent au vrai composant React de l'application :
- le champ e-mail est un <input type="email">
- le champ mot de passe est un <input type="password">
- le formulaire ne contient qu'un seul <button> (« Se connecter »)
- en cas d'échec, un <p class="text-red-600"> affiche le message d'erreur

Après une connexion réussie, l'application stocke le token JWT dans
localStorage sous la clé « token » : c'est notre preuve de connexion.
"""

from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class LoginPage(BasePage):
    PATH = "/login"

    # --- Locators ---
    EMAIL_INPUT = (By.CSS_SELECTOR, "input[type='email']")
    PASSWORD_INPUT = (By.CSS_SELECTOR, "input[type='password']")
    SUBMIT_BUTTON = (By.CSS_SELECTOR, "form button")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "p.text-red-600")

    # --- Actions ---
    def load(self):
        """Ouvre la page de connexion et la renvoie (chaînage possible)."""
        self.open(self.PATH)
        return self

    def is_loaded(self) -> bool:
        """True si le formulaire de connexion est bien affiché."""
        return self.is_visible(self.EMAIL_INPUT) and self.is_visible(self.SUBMIT_BUTTON)

    def login(self, email: str, password: str):
        """Remplit le formulaire et valide."""
        self.type(self.EMAIL_INPUT, email)
        self.type(self.PASSWORD_INPUT, password)
        self.click(self.SUBMIT_BUTTON)

    def get_error_message(self) -> str:
        return self.get_text(self.ERROR_MESSAGE)

    def is_error_displayed(self) -> bool:
        return self.is_visible(self.ERROR_MESSAGE, timeout=5)

    def get_token(self):
        """Renvoie le token JWT stocké après connexion (ou None)."""
        return self.get_local_storage_item("token")
