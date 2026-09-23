import os
import logging
from pathlib import Path
from time import sleep
from dotenv import load_dotenv

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# -------------------------------------------------
# Configurações (podem ser sobrescritas via .env)
# -------------------------------------------------
load_dotenv()  # .env na raiz ou na pasta config/

BASE_URL = os.getenv("BASE_URL", "https://the-internet.herokuapp.com")
LOGIN_URL = os.getenv("LOGIN_URL", f"{BASE_URL}/login")
EXPORT_URL = os.getenv("EXPORT_URL", f"{BASE_URL}/download")  # exemplo genérico
USERNAME = os.getenv("USERNAME", "tomsmith")  # credencial de teste do site
PASSWORD = os.getenv("PASSWORD", "SuperSecretPassword!")  # credencial de teste
DOWNLOAD_DIR = os.getenv(
    "DOWNLOAD_DIR",
    str(Path(__file__).resolve().parents[2] / "data" / "raw")
)

# -------------------------------------------------
# Logger simples
# -------------------------------------------------
logger = logging.getLogger(__name__)
if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)


def init_driver(headless: bool = True) -> webdriver.Chrome:
    """Inicializa ChromeDriver via Selenium‑Manager."""
    options = webdriver.ChromeOptions()
    if headless:
        options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    # configura download automático
    prefs = {
        "download.default_directory": DOWNLOAD_DIR,
        "download.prompt_for_download": False,
        "profile.default_content_setting_values.automatic_downloads": 1,
    }
    options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(service=ChromeService(), options=options)
    driver.set_page_load_timeout(30)
    logger.info("ChromeDriver iniciado (headless=%s)", headless)
    return driver


def login(driver: webdriver.Chrome, user: str, pwd: str) -> None:
    """Realiza login na página de teste."""
    driver.get(LOGIN_URL)
    logger.info("Acessando página de login: %s", LOGIN_URL)
    try:
        wait = WebDriverWait(driver, 15)
        user_el = wait.until(EC.presence_of_element_located((By.ID, "username")))
        pwd_el = driver.find_element(By.ID, "password")
        submit_el = driver.find_element(By.CSS_SELECTOR, "button.radius")
        user_el.clear()
        user_el.send_keys(user)
        pwd_el.clear()
        pwd_el.send_keys(pwd)
        submit_el.click()
        # verifica sucesso (mensagem de boas‑vindas)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.flash.success")))
        logger.info("Login efetuado com sucesso.")
    except Exception as e:
        logger.error("Falha no login: %s", e)
        driver.quit()
        raise


def export_csv(driver: webdriver.Chrome) -> Path:
    """Simula a exportação de um CSV.
    No site de teste usamos a página “File Download” como exemplo.
    O método pode ser adaptado para o endpoint real da aplicação.
    """
    driver.get(EXPORT_URL)
    logger.info("Navegando para página de download: %s", EXPORT_URL)
    try:
        wait = WebDriverWait(driver, 15)
        # exemplo: clicar no primeiro link que contém .txt
        link = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, '.txt')]"))
        )
        link.click()
        logger.info("Iniciada a requisição de download.")
        file_path = Path(DOWNLOAD_DIR) / "some-file.txt"
        timeout = 30
        elapsed = 0
        while not file_path.exists() and elapsed < timeout:
            sleep(1)
            elapsed += 1
        if not file_path.exists():
            raise FileNotFoundError("Arquivo de download não apareceu.")
        logger.info("Download concluído: %s", file_path)
        return file_path
    except Exception as e:
        logger.error("Falha ao exportar CSV: %s", e)
        raise


def coletar_dados(headless: bool = True) -> Path:
    """Orquestra o fluxo completo:
    1. inicia driver
    2. faz login
    3. realiza exportação (simulada)
    4. encerra driver e devolve caminho do CSV baixado
    """
    driver = init_driver(headless=headless)
    try:
        login(driver, USERNAME, PASSWORD)
        csv_path = export_csv(driver)
        return csv_path
    finally:
        driver.quit()
        logger.info("Driver encerrado.")

if __name__ == "__main__":
    # Execução rápida para depuração
    path = coletar_dados(headless=False)
    print(f"Arquivo salvo em: {path}")
