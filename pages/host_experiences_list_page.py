"""
Page Object de la liste « Mes expériences » (/host/experiences).

La liste est paginée par 5, sans tri garanti : pour retrouver une expérience
précise (par son titre unique), on parcourt les pages une à une. La publication
se fait via l'interrupteur (Radix Switch = <button role="switch">) de la ligne ;
après clic, la liste se rafraîchit et le badge passe à « Publié ».

L'édition se fait via le lien crayon de la ligne (href contient « /edit »),
qui ouvre le formulaire de modification (voir HostEditExperiencePage).
"""

from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class HostExperiencesListPage(BasePage):
    PATH = "/host/experiences"

    NEXT_BUTTON = (By.XPATH, "//span[contains(normalize-space(.), 'Page')]/following-sibling::button[1]")
    PAGE_NUMBER = (By.XPATH, "//span[contains(normalize-space(.), 'Page')]/b")

    # --- locators dynamiques (dépendent du titre) ---
    def _row(self, title):
        return (By.XPATH, f"//td[contains(normalize-space(.), \"{title}\")]/ancestor::tr")

    def _switch(self, title):
        return (By.XPATH, f"//td[contains(normalize-space(.), \"{title}\")]"
                          f"/ancestor::tr//button[@role='switch']")

    def _status(self, title):
        return (By.XPATH, f"//td[contains(normalize-space(.), \"{title}\")]"
                          f"/ancestor::tr//span[contains(text(),'Publié') "
                          f"or contains(text(),'Brouillon') or contains(text(),'Inactif')]")

    def _edit_link(self, title):
        return (By.XPATH, f"//td[contains(normalize-space(.), \"{title}\")]"
                          f"/ancestor::tr//a[contains(@href, '/edit')]")

    def _price_cell(self, title):
        return (By.XPATH, f"//td[contains(normalize-space(.), \"{title}\")]/ancestor::tr/td[5]")

    # --- pagination interne ---
    def _current_page(self):
        els = self.driver.find_elements(*self.PAGE_NUMBER)
        return els[0].text if els else "1"

    def _search_pages(self, title: str, on_found) -> bool:
        """Parcourt les pages jusqu'à trouver `title`, puis exécute `on_found`.

        Renvoie True si trouvée (et `on_found` exécuté), False sinon.
        """
        self.open(self.PATH)
        self.find((By.TAG_NAME, "table"))

        for _ in range(50):                       # garde-fou anti boucle infinie
            if self.driver.find_elements(*self._row(title)):
                on_found()
                return True

            next_btns = self.driver.find_elements(*self.NEXT_BUTTON)
            if next_btns and next_btns[0].is_enabled():
                current = self._current_page()
                next_btns[0].click()
                self.wait.until(lambda d: self._current_page() != current)
            else:
                return False
        return False

    # --- actions ---
    def find_and_publish(self, title: str) -> bool:
        """Cherche l'expérience à travers les pages et la publie. True si trouvée."""
        def publish():
            self.click(self._switch(title))
            self.wait.until(lambda d: self.is_published(title))

        return self._search_pages(title, on_found=publish)

    def open_edit(self, title: str) -> bool:
        """Cherche l'expérience à travers les pages et ouvre son formulaire de modification."""
        return self._search_pages(title, on_found=lambda: self.click(self._edit_link(title)))

    def find_experience(self, title: str) -> bool:
        """Cherche l'expérience à travers les pages, sans action. True si trouvée."""
        return self._search_pages(title, on_found=lambda: None)

    def is_published(self, title: str) -> bool:
        els = self.driver.find_elements(*self._status(title))
        return any("Publié" in e.text for e in els)

    def get_price(self, title: str) -> str:
        """Lit le texte de la cellule Prix pour la ligne correspondant à `title`."""
        els = self.driver.find_elements(*self._price_cell(title))
        return els[0].text if els else ""
