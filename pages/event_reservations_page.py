"""
Page Object de la liste des réservations d'événements (/reservations) —
touriste. Système distinct de la réservation par virement (voir
TouristReservationsPage / /wire-reservations) : colonnes ID | Événement |
Date | Qté | Statut | Actions.

Comme les réservations n'ont pas de libellé unique qu'on contrôle (titre de
l'événement réutilisé), on identifie la nôtre par son ID (auto-incrément) :
on relève le plus grand ID existant avant création, puis on retrouve la
nouvelle réservation comme celle dont l'ID est supérieur à cette référence.

L'annulation déclenche une confirmation navigateur native (window.confirm),
à accepter via Selenium (switch_to.alert). Après annulation, la page se
met à jour en temps réel (état React local, pas besoin de recharger).
"""

import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage


class EventReservationsPage(BasePage):
    PATH = "/reservations"

    TITLE = (By.XPATH, "//h1[contains(., 'Mes réservations')]")
    ID_CELLS = (By.CSS_SELECTOR, "table tbody tr td:first-child")

    def load(self):
        self.open(self.PATH)
        self.find(self.TITLE)
        # Ce composant charge ses données via un simple useEffect, sans
        # aucun indicateur de chargement visible dans le DOM (le tableau
        # est juste vide au tout premier rendu). Faute de signal fiable à
        # attendre, on laisse un court délai fixe pour l'appel API initial.
        time.sleep(1.5)
        return self

    def is_loaded(self) -> bool:
        return self.is_visible(self.TITLE)

    def max_id(self) -> int:
        ids = [int(c.text.strip()) for c in self.driver.find_elements(*self.ID_CELLS) if c.text.strip().isdigit()]
        return max(ids) if ids else 0

    def _row(self, rid: int):
        return (By.XPATH, f"//tr[td[1][normalize-space()='{rid}']]")

    def status_of(self, rid: int) -> str:
        row = self.find(self._row(rid))
        cells = row.find_elements(By.TAG_NAME, "td")
        return cells[4].text.strip()  # colonne Statut

    def cancel(self, rid: int):
        row = self.find(self._row(rid))
        btn = row.find_element(By.XPATH, ".//button[contains(., 'Annuler')]")
        btn.click()
        self.wait.until(EC.alert_is_present())
        self.driver.switch_to.alert.accept()

    def cancel_all_pending(self):
        """Annule toutes les réservations PENDING existantes.

        Nettoyage de précaution en DÉBUT de test : si une exécution
        précédente a échoué avant d'atteindre l'étape d'annulation, une
        réservation PENDING reste orpheline sur un créneau. Le backend
        refuse alors toute nouvelle réservation sur ce même créneau pour
        le même compte ("Vous avez déjà une réservation pour ce
        créneau."), ce qui bloquerait indéfiniment les runs suivants sans
        ce nettoyage préalable.
        """
        while True:
            target = None
            for row in self.driver.find_elements(*(By.CSS_SELECTOR, "table tbody tr")):
                cells = row.find_elements(By.TAG_NAME, "td")
                if len(cells) >= 5 and cells[4].text.strip() == "PENDING":
                    target = int(cells[0].text.strip())
                    break
            if target is None:
                break
            self.cancel(target)
            self.wait_status_not(target, "PENDING")

    def wait_status_not(self, rid: int, not_expected: str, timeout: int = 10):
        self.wait.until(lambda d: self.status_of(rid) != not_expected)
