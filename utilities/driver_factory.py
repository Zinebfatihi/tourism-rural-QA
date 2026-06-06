"""
Driver factory.

Seul endroit du framework qui SAIT comment créer et configurer le navigateur
Selenium. Tous les tests passent par ici, donc changer une option (taille de
fenêtre, mode headless, navigateur) se fait à un seul endroit.

Selenium 4 télécharge automatiquement le bon driver via « Selenium Manager » :
pas besoin d'installer chromedriver/geckodriver à la main.
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions

from config.config import config
from utilities.logger import get_logger

log = get_logger("driver")


def create_driver():
    """Crée un WebDriver selon la configuration et le renvoie."""
    browser = config.BROWSER
    log.info("Lancement du navigateur : %s (headless=%s)", browser, config.HEADLESS)

    if browser == "chrome":
        options = ChromeOptions()
        if config.HEADLESS:
            options.add_argument("--headless=new")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--no-sandbox")            # utile en CI (Linux)
        options.add_argument("--disable-dev-shm-usage")  # utile en CI (Linux)
        driver = webdriver.Chrome(options=options)

    elif browser == "firefox":
        options = FirefoxOptions()
        if config.HEADLESS:
            options.add_argument("--headless")
        options.add_argument("--width=1920")
        options.add_argument("--height=1080")
        driver = webdriver.Firefox(options=options)

    else:
        raise ValueError(f"Navigateur non supporté : {browser!r} (chrome ou firefox)")

    driver.set_page_load_timeout(config.PAGE_LOAD_TIMEOUT)
    return driver
