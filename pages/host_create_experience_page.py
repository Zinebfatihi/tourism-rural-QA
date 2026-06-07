"""
Page Object du formulaire de création d'expérience (/host/experiences/new).

Le formulaire React Hook Form expose chaque champ via son attribut `name`,
ce qui donne des sélecteurs simples et robustes. Le champ date/heure
(datetime-local) est rempli en JavaScript car son format de saisie dépend de
la langue du navigateur — on injecte directement la valeur ISO et on déclenche
les évènements pour que le formulaire la prenne en compte.

Règles de validation (côté front) à respecter pour que l'envoi parte :
- titre >= 4 caractères, description >= 20 caractères
- prix et capacité strictement positifs
- au moins un créneau avec date, capacité et prix valides
"""

import re
import time
from datetime import datetime, timedelta

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage


class HostCreateExperiencePage(BasePage):
    PATH = "/host/experiences/new"

    # --- Locators (par attribut name) ---
    TITLE = (By.CSS_SELECTOR, "input[name='title']")
    PRICE = (By.CSS_SELECTOR, "input[name='price']")
    DESCRIPTION = (By.CSS_SELECTOR, "textarea[name='description']")
    CAPACITY = (By.CSS_SELECTOR, "input[name='capacity']")
    CITY = (By.CSS_SELECTOR, "input[name='city']")
    REGION = (By.CSS_SELECTOR, "input[name='region']")
    LATITUDE = (By.CSS_SELECTOR, "input[name='latitude']")
    LONGITUDE = (By.CSS_SELECTOR, "input[name='longitude']")
    MAP = (By.CSS_SELECTOR, ".leaflet-container")
    MAP_MARKER = (By.CSS_SELECTOR, ".leaflet-marker-icon")
    SLOT_DATETIME = (By.CSS_SELECTOR, "input[name='slots.0.startDateTime']")
    SLOT_PRICE = (By.CSS_SELECTOR, "input[name='slots.0.price']")
    SUBMIT = (By.XPATH, "//button[contains(., 'Enregistrer')]")
    ERROR_TOAST = (By.XPATH, "//*[contains(text(), 'Erreur lors de la création')]")

    def load(self):
        self.open(self.PATH)
        self.find(self.TITLE)
        return self

    def fill(self, title: str, description: str, price: int = 300, capacity: int = 10):
        self.type(self.TITLE, title)
        self.type(self.DESCRIPTION, description)
        self.type(self.PRICE, str(price))
        self.type(self.CAPACITY, str(capacity))
        self.type(self.CITY, "Essaouira")
        self.type(self.REGION, "Marrakech-Safi")

        # Localisation : un clic sur la carte appelle directement la fonction
        # React qui enregistre latitude & longitude (le vrai geste utilisateur).
        self._pick_location_on_map()

        # créneau : date future tapée au CLAVIER, segment par segment
        # (format d'affichage FR : jour, mois, année, puis heure, minute).
        future = datetime.now() + timedelta(days=20)
        self._type_datetime(self.SLOT_DATETIME, future)
        self.type(self.SLOT_PRICE, str(price))
        return self

    def submit(self):
        self.click(self.SUBMIT)

    def get_value(self, locator) -> str:
        """Lit la valeur actuelle d'un champ (utile pour diagnostiquer)."""
        return self.find(locator).get_attribute("value") or ""

    def wait_result(self, timeout: int = 12) -> str:
        """
        Attend l'issue de la soumission et la classe :
        - 'created' : redirection vers la page images (succès)
        - 'error'   : toast d'erreur affiché (la requête a échoué côté serveur)
        - 'blocked' : ni l'un ni l'autre (validation du formulaire bloquée)
        """
        end = time.time() + timeout
        while time.time() < end:
            if "/images" in self.current_url:
                return "created"
            if self.driver.find_elements(*self.ERROR_TOAST):
                return "error"
            time.sleep(0.3)
        return "blocked"

    def get_created_id(self):
        """Récupère l'id de l'expérience depuis l'URL /host/experiences/{id}/images."""
        match = re.search(r"/host/experiences/(\d+)/images", self.current_url)
        return match.group(1) if match else None

    # --- helper : choisir la localisation en cliquant sur la carte ---
    def _pick_location_on_map(self):
        """Clique au centre de la carte ; Leaflet renvoie les coordonnées que
        React enregistre via setValue. Le marqueur qui apparaît confirme l'action."""
        map_el = self.wait.until(EC.element_to_be_clickable(self.MAP))
        ActionChains(self.driver).move_to_element(map_el).click().perform()
        self.wait.until(EC.presence_of_element_located(self.MAP_MARKER))

    # --- helper : taper une date dans un champ datetime-local au clavier ---
    def _type_datetime(self, locator, dt):
        """
        Tape la date segment par segment. L'ordre suit l'affichage local du
        navigateur (français : jour, mois, année). On force le passage à l'heure
        avec une flèche droite car le segment « année » ne change pas tout seul.
        """
        element = self.find(locator)
        element.click()
        element.send_keys(Keys.ARROW_LEFT * 5)   # revenir au 1er segment (jour)
        element.send_keys(dt.strftime("%d"))      # jour
        element.send_keys(dt.strftime("%m"))      # mois
        element.send_keys(dt.strftime("%Y"))      # année
        element.send_keys(Keys.ARROW_RIGHT)       # passer à l'heure
        element.send_keys(dt.strftime("%H"))      # heure
        element.send_keys(dt.strftime("%M"))      # minute
