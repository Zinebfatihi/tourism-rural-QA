"""
Page Object de la page de vérification d'identité (KYC) — hôte ou guide.
Chemin : /host/kyc (le composant est le même sur /guide/kyc).

Chaque document requis (Carte d'identité recto/verso, selfie, + licence pour
le guide) apparaît comme une carte avec un badge de statut (« À déposer »,
« En cours », « Validé », « Refusé ») et, uniquement si le statut est « À
déposer » ou « Refusé », un bouton « Importer » qui pilote un input file
caché en CSS.

Le champ fichier est caché (hidden), mais comme pour le justificatif de
virement (voir ProofUploadPage), Selenium peut lui envoyer un chemin de
fichier via send_keys en le localisant par présence plutôt que visibilité.

Note : l'invalidation de query ("kycDocs") après upload est correcte côté
frontend — la mise à jour est en temps réel, pas besoin de recharger la page.
"""

from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class HostKycPage(BasePage):
    PATH = "/host/kyc"

    TITLE = (By.XPATH, "//h1[contains(., 'identité')]")
    # Si le KYC est déjà entièrement approuvé, l'appli affiche un tout autre
    # composant (KycVerifiedPage) au lieu du formulaire de dépôt.
    VERIFIED_TITLE = (By.XPATH, "//h1[contains(., 'réussie')]")

    def load(self):
        self.open(self.PATH)
        # Attend l'un OU l'autre écran, sans supposer lequel s'affichera.
        self.wait.until(
            lambda d: d.find_elements(*self.TITLE) or d.find_elements(*self.VERIFIED_TITLE)
        )
        return self

    def is_loaded(self) -> bool:
        return len(self.driver.find_elements(*self.TITLE)) > 0

    def is_already_verified(self) -> bool:
        """True si le compte est déjà entièrement vérifié (rien à soumettre)."""
        return len(self.driver.find_elements(*self.VERIFIED_TITLE)) > 0

    # --- locators dynamiques (dépendent du libellé du document, ex. "Recto") ---
    def _label_span(self, label_fragment: str):
        return (By.XPATH, f"//span[contains(text(), \"{label_fragment}\")]")

    def _badge(self, label_fragment: str):
        # Le badge de statut est le premier <span> frère du libellé (même conteneur).
        return (By.XPATH, f"//span[contains(text(), \"{label_fragment}\")]/parent::div/span[1]")

    def _file_input(self, label_fragment: str):
        return (
            By.XPATH,
            f"//span[contains(text(), \"{label_fragment}\")]"
            f"/ancestor::div[contains(@class,'justify-between')]//input[@type='file']",
        )

    def status_of(self, label_fragment: str) -> str:
        """Texte du badge : 'À déposer', 'En cours', 'Validé' ou 'Refusé'."""
        return self.find(self._badge(label_fragment)).text.strip()

    def can_upload(self, label_fragment: str) -> bool:
        """True si un input file est présent pour ce document (statut À déposer/Refusé)."""
        return len(self.driver.find_elements(*self._file_input(label_fragment))) > 0

    def upload(self, label_fragment: str, file_path: str):
        self.find(self._file_input(label_fragment)).send_keys(file_path)

    def wait_status(self, label_fragment: str, expected: str, timeout: int = 10):
        self.wait.until(lambda d: self.status_of(label_fragment) == expected)
