"""
Page Object du formulaire de création/édition de circuit (guide).

Chemin de création : /guide/circuits/new
Après la première sauvegarde, l'application navigue automatiquement vers
/guide/circuits/{id}/edit (même formulaire, pré-rempli, avec en plus les
sections image de couverture et tracé GPS) — cette redirection sert de
preuve que la création a réussi côté backend.

Champs du formulaire : Titre, Description, Difficulté (select), Durée (h),
Prix (MAD), Capacité, Date & heure de départ (pré-remplie à "maintenant",
laissée telle quelle). Bouton « Enregistrer ».

Hors scope volontaire : le tracé du circuit (dessin de points GPS sur une
carte) et l'upload d'image de couverture, qui n'apparaissent qu'une fois le
circuit créé et demanderaient une interaction canvas/carte plus lourde à
automatiser de façon fiable. Ce Page Object couvre la création des
informations, l'essentiel du parcours métier.
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from pages.base_page import BasePage


class GuideCircuitFormPage(BasePage):
    NEW_PATH = "/guide/circuits/new"

    TITLE_INPUT = (By.XPATH, "//label[normalize-space()='Titre']/following-sibling::input")
    DESCRIPTION_INPUT = (By.XPATH, "//label[normalize-space()='Description']/following-sibling::textarea")
    DIFFICULTY_SELECT = (By.XPATH, "//label[normalize-space()='Difficulté']/following-sibling::select")
    DURATION_INPUT = (By.XPATH, "//label[contains(., 'Durée')]/following-sibling::input")
    PRICE_INPUT = (By.XPATH, "//label[contains(., 'Prix')]/following-sibling::input")
    CAPACITY_INPUT = (By.XPATH, "//label[normalize-space()='Capacité']/following-sibling::input")
    SUBMIT_BTN = (By.XPATH, "//button[contains(., 'Enregistrer')]")

    def load(self):
        self.open(self.NEW_PATH)
        self.find(self.TITLE_INPUT)
        return self

    def fill_and_submit(
        self,
        title: str,
        description: str,
        difficulty: str = "EASY",
        duration: int = 2,
        price: float = 150,
        capacity: int = 8,
    ):
        """Remplit les infos du circuit et soumet. Ne touche pas à la date de
        départ (déjà pré-remplie avec la date/heure actuelle, ce qui est
        valide)."""
        self.type(self.TITLE_INPUT, title)
        self.type(self.DESCRIPTION_INPUT, description)
        Select(self.find(self.DIFFICULTY_SELECT)).select_by_value(difficulty)
        self.type(self.DURATION_INPUT, str(duration))
        self.type(self.PRICE_INPUT, str(price))
        self.type(self.CAPACITY_INPUT, str(capacity))
        self.click(self.SUBMIT_BTN)

    def wait_created(self):
        """Attend la redirection vers /guide/circuits/{id}/edit, preuve que
        la création a réussi côté backend. Lève TimeoutException sinon."""
        self.wait.until(lambda d: "/edit" in d.current_url)
