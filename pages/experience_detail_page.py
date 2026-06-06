"""
Page Object de la page détail d'une expérience (/experiences/{id}).

Sélecteurs tirés du vrai composant React :
- un titre <h1> (le nom de l'expérience)
- un prix affiché avec « MAD »
- une section <h2> « Dates disponibles » (le bloc de réservation)
"""

from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class ExperienceDetailPage(BasePage):
    # --- Locators ---
    TITLE = (By.CSS_SELECTOR, "h1")
    PRICE = (By.XPATH, "//span[contains(., 'MAD')]")
    DATES_SECTION = (By.XPATH, "//h2[contains(., 'Dates disponibles')]")

    def is_loaded(self) -> bool:
        """Vrai si on est bien sur une page détail (URL + titre affiché)."""
        return "/experiences/" in self.current_url and self.is_visible(self.TITLE)

    def get_title(self) -> str:
        return self.get_text(self.TITLE)

    def is_price_displayed(self) -> bool:
        return self.is_visible(self.PRICE)

    def is_booking_section_displayed(self) -> bool:
        return self.is_visible(self.DATES_SECTION)
