"""Web automation module for SmartLicense RPA.

Provides :func:`extract_users_from_portal` which uses Selenium to log into the local Flask
mock server (http://127.0.0.1:5000) and extracts the user table present on the
dashboard page.

The function expects the Flask server defined in ``mock_server/app.py`` to be
running beforehand. It returns a list of dictionaries, each containing the
keys ``nome``, ``email`` and ``status``.
"""

from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def extract_users_from_portal() -> list[dict[str, str]]:
    """Log into the Flask portal and scrape the user table.

    Steps:
    1. Open Chrome via ``webdriver.Chrome()``.
    2. Navigate to ``http://127.0.0.1:5000/login``.
    3. Wait for the username field (id="usuario") to be present.
    4. Fill in credentials (admin / 1234) and submit.
    5. Wait for the dashboard table (id="tabela-usuarios").
    6. Extract each row from ``<tbody>`` into a dict with keys ``nome``,
       ``email`` and ``status``.
    7. Return the list of dicts.

    Raises:
        RuntimeError: If login fails, the error element appears, or the
        table never becomes visible.
    """
    driver = None
    try:
        driver = webdriver.Chrome()
        driver.get("http://127.0.0.1:5000/login")

        wait = WebDriverWait(driver, 10)
        # Wait for the login form fields
        usuario_input = wait.until(EC.presence_of_element_located((By.ID, "usuario")))
        senha_input = driver.find_element(By.ID, "senha")
        botao_entrar = driver.find_element(By.ID, "btn-entrar")

        usuario_input.send_keys("admin")
        senha_input.send_keys("1234")
        botao_entrar.click()

        # After submit, either an error message appears or the dashboard loads
        # Wait for either the error element or the table
        try:
            wait.until(EC.presence_of_element_located((By.ID, "tabela-usuarios")))
        except Exception:
            # Check if the error element is present
            erro_elem = driver.find_elements(By.ID, "erro")
            if erro_elem and erro_elem[0].is_displayed():
                raise RuntimeError("Falha ao autenticar no portal: credenciais inválidas.")
            # If no table and no explicit error, re‑raise the original timeout
            raise RuntimeError("Falha ao autenticar no portal: tabela não encontrada.")

        tabela = driver.find_element(By.ID, "tabela-usuarios")
        linhas = tabela.find_elements(By.XPATH, "./tbody/tr")
        usuarios = []
        for linha in linhas:
            colunas = linha.find_elements(By.TAG_NAME, "td")
            if len(colunas) >= 3:
                usuarios.append({
                    "nome": colunas[0].text.strip(),
                    "email": colunas[1].text.strip(),
                    "status": colunas[2].text.strip(),
                })
        return usuarios
    except (TimeoutException, NoSuchElementException) as exc:
        # Wrap any Selenium/timeout errors in a clear RuntimeError
        raise RuntimeError(str(exc)) from exc
    finally:
        if driver:
            driver.quit()


if __name__ == "__main__":
    # NOTE: Ensure ``mock_server/app.py`` is running (python mock_server/app.py)
    # in another terminal before executing this script.
    try:
        usuarios = extract_users_from_portal()
        print(usuarios)
    except RuntimeError as e:
        print(f"Erro: {e}")
