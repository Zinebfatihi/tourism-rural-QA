"""
Page Object de l'upload du justificatif de virement.
URL : /wire-reservations/{reservationId}/proof

Le champ fichier (input#proof) est caché par CSS, mais Selenium peut quand même
y envoyer un chemin de fichier (cas particulier des champs type=file). On le
localise donc par PRÉSENCE et non par visibilité.
"""

from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class ProofUploadPage(BasePage):
    TITLE = (By.XPATH, "//h1[contains(., 'justificatif')]")
    FILE_INPUT = (By.ID, "proof")
    SUBMIT = (By.XPATH, "//button[contains(., 'Envoyer la preuve')]")
    SUCCESS = (By.XPATH, "//*[contains(text(), 'Preuve envoyée')]")

    def is_loaded(self) -> bool:
        return self.is_visible(self.TITLE)

    def upload(self, file_path: str):
        # input type=file : send_keys fonctionne même si l'élément est caché
        self.find(self.FILE_INPUT).send_keys(file_path)

    def submit(self):
        self.click(self.SUBMIT)

    def is_uploaded(self) -> bool:
        return self.is_visible(self.SUCCESS, timeout=10)
