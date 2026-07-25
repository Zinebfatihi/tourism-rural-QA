"""
Page Object de la gestion des retraits admin (/admin/withdrawals).

Par défaut, l'onglet affiché est « En attente » (PENDING). Chaque ligne a
deux boutons d'action : ✓ (approuver, vert) et ✗ (refuser, rouge), qui ouvrent
tous deux la même modale (CommentModal) avec un textarea de commentaire
optionnel et un bouton « Confirmer ».

Comme il n'y a pas d'identifiant visible par ligne, on identifie une demande
par le couple (Montant, Banque) — colonnes 2 et 3 du tableau — de la même
manière que le KYC identifie ses lignes par email.

Contrairement aux comptes bancaires, ici l'invalidation de query côté
frontend est correcte (préfixe "withdrawals" complet) : la liste se
rafraîchit en temps réel après approbation/refus, pas besoin de recharger la
page.
"""

from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class AdminWithdrawalsPage(BasePage):
    PATH = "/admin/withdrawals"

    TITLE = (By.XPATH, "//h1[contains(., 'Gestion des retraits')]")
    ROWS = (By.CSS_SELECTOR, "table tbody tr")
    APPROVE_BTN = (By.CSS_SELECTOR, "table tbody tr button.bg-emerald-600")
    REJECT_BTN = (By.CSS_SELECTOR, "table tbody tr button.bg-rose-600")
    COMMENT_INPUT = (By.XPATH, "//textarea[contains(@placeholder, 'Commentaire')]")
    CONFIRM_BTN = (By.XPATH, "//button[normalize-space()='Confirmer']")

    def load(self):
        self.open(self.PATH)
        self.find(self.TITLE)
        return self

    def is_loaded(self) -> bool:
        return self.is_visible(self.TITLE)

    def has_pending(self) -> bool:
        return len(self.driver.find_elements(*self.APPROVE_BTN)) > 0

    def _pending_identities(self):
        """Liste des (montant, banque) actuellement affichés (onglet En attente)."""
        identities = []
        for row in self.driver.find_elements(*self.ROWS):
            cells = row.find_elements(By.TAG_NAME, "td")
            if len(cells) >= 3:
                identities.append((cells[1].text.strip(), cells[2].text.strip()))
        return identities

    def approve_first_pending(self, comment: str = "Validé QA") -> tuple:
        """Approuve la première demande en attente. Renvoie (montant, banque)."""
        identities_before = self._pending_identities()
        if not identities_before:
            raise ValueError("Aucune demande en attente à valider.")
        target = identities_before[0]

        self.click(self.APPROVE_BTN)
        self.type(self.COMMENT_INPUT, comment)
        self.click(self.CONFIRM_BTN)

        self.wait.until(lambda d: target not in self._pending_identities())
        return target

    def reject_first_pending(self, comment: str = "Refusé QA") -> tuple:
        """Rejette la première demande en attente. Renvoie (montant, banque)."""
        identities_before = self._pending_identities()
        if not identities_before:
            raise ValueError("Aucune demande en attente à rejeter.")
        target = identities_before[0]

        self.click(self.REJECT_BTN)
        self.type(self.COMMENT_INPUT, comment)
        self.click(self.CONFIRM_BTN)

        self.wait.until(lambda d: target not in self._pending_identities())
        return target
