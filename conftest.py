# 01 - Importa módulos do Python usados para manipulação de arquivos, logs e tempo.
import os
import logging
import shutil
from datetime import datetime

# 02 - Importa bibliotecas de teste e automação.
import pytest
import allure
from selenium import webdriver


# 03 - Define a pasta base do projeto para localizar os relatórios e imagens.
BASE_DIR = os.path.dirname(__file__)
ALLURE_RESULTS_DIR = os.path.join(BASE_DIR, "allure-results")
ALLURE_REPORT_DIR = os.path.join(BASE_DIR, "allure-report")
IMG_DIR = os.path.join(BASE_DIR, "img")

# 04 - Limpa as pastas de resultados antes de cada execução para evitar dados antigos.
for directory in [ALLURE_RESULTS_DIR, ALLURE_REPORT_DIR, IMG_DIR]:
    if os.path.exists(directory):
        for item in os.listdir(directory):
            full_path = os.path.join(directory, item)
            if os.path.isdir(full_path):
                shutil.rmtree(full_path, ignore_errors=True)
            else:
                os.remove(full_path)
    else:
        os.makedirs(directory, exist_ok=True)

# 05 - Garante que as pastas principais existam antes do próximo passo.
os.makedirs(ALLURE_RESULTS_DIR, exist_ok=True)
os.makedirs(ALLURE_REPORT_DIR, exist_ok=True)
os.makedirs(IMG_DIR, exist_ok=True)

# 06 - Cria subpastas específicas para logs e screenshots de login/produtos/falhas.
BASE_DIR = os.path.dirname(__file__)
LOGS_DIR = os.path.join(BASE_DIR, "logs")
IMG_DIR = os.path.join(BASE_DIR, "img")
FALHAS_DIR = os.path.join(IMG_DIR, "falhas")
LOGIN_DIR = os.path.join(IMG_DIR, "login")
PRODUTOS_DIR = os.path.join(IMG_DIR, "produtos")

for folder in [LOGS_DIR, IMG_DIR, FALHAS_DIR, LOGIN_DIR, PRODUTOS_DIR]:
    os.makedirs(folder, exist_ok=True)

# 07 - Remove arquivos antigos da pasta img para evitar acúmulo de evidências antigas.
for item in os.listdir(IMG_DIR):
    full_path = os.path.join(IMG_DIR, item)
    if os.path.isdir(full_path):
        shutil.rmtree(full_path, ignore_errors=True)
    else:
        os.remove(full_path)

for folder in [FALHAS_DIR, LOGIN_DIR, PRODUTOS_DIR]:
    os.makedirs(folder, exist_ok=True)

# 08 - Configura o logging global para registrar eventos do teste em arquivo e terminal.
log_filename = os.path.join(LOGS_DIR, f"execution_{datetime.now().strftime('%Y%m%d')}.log")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
    handlers=[
        logging.FileHandler(log_filename, encoding="utf-8"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("QA_Selenium")


# 09 - Adiciona uma flag opcional para rodar testes em modo headless.
def pytest_addoption(parser):
    """Adiciona opção de linha de comando para rodar em modo headless."""
    parser.addoption(
        "--headless",
        action="store_true",
        default=False,
        help="Executar testes em modo headless (sem interface gráfica)"
    )


# 10 - Fixture principal do Selenium: abre o navegador antes de cada teste e fecha depois.
@pytest.fixture(scope="function")
def driver(request):
    """
    Fixture responsável pela inicialização e finalização do WebDriver do Selenium.
    O webdriver-manager baixa o driver compatível automaticamente.
    """
    logger.info("Iniciando a sessão do Selenium WebDriver...")

    # 11 - Cria as opções do Chrome para reduzir interferências visuais e avisos.
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-features=PasswordManagerOnboarding")
    options.add_argument("--disable-password-manager-onboarding")
    options.add_argument("--disable-save-password-bubble")
    options.add_argument("--disable-notifications")

    # 12 - Desativa pop-ups de notificação e senha do navegador.
    prefs = {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,
        "profile.default_content_setting_values.notifications": 2,
    }
    options.add_experimental_option("prefs", prefs)

    # 13 - Se o teste rodar em modo headless, a janela do navegador não aparece.
    if request.config.getoption("--headless"):
        options.add_argument("--headless=new")
        logger.info("Executando em modo Headless (sem janela visual).")

    # 14 - Inicializa o navegador com essas opções.
    browser = webdriver.Chrome(options=options)
    browser.implicitly_wait(5)

    # 15 - Guarda a referência do navegador no item do teste para uso na captura de falha.
    request.node.driver = browser

    # 16 - Entrega o navegador para o teste.
    yield browser

    # 17 - Fecha a sessão do navegador após o teste terminar.
    logger.info("Encerando a sessão do Selenium WebDriver...")
    browser.quit()


# 18 - Hook do pytest para capturar screenshot e anexar ao relatório em caso de falha.
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Hook do PyTest que intercepta o resultado da execução de cada teste.
    Em caso de falha, tira print da tela do navegador, salva em 'logs/' e anexa ao Allure Report.
    """
    outcome = yield
    report = outcome.get_result()

    # 19 - Só ativa a captura quando a falha acontece na fase de execução do teste.
    if report.when == "call" and report.failed:
        web_driver = getattr(item, "driver", None)
        if web_driver:
            try:
                # 20 - Cria nome do arquivo com data e nome do teste.
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                test_name = item.name
                filename = f"{timestamp}_FAIL_{test_name}.png"
                filepath = os.path.join(FALHAS_DIR, filename)

                # 21 - Salva a imagem física no disco para análise posterior.
                web_driver.save_screenshot(filepath)
                logger.error(f"Teste '{test_name}' FALHOU. Evidência salva em: {filepath}")

                # 22 - Anexa a imagem ao Allure para visualização do relatório.
                screenshot_bytes = web_driver.get_screenshot_as_png()
                allure.attach(
                    screenshot_bytes,
                    name=f"Evidência de Falha - {test_name}",
                    attachment_type=allure.attachment_type.PNG
                )

                # 23 - Anexa também o texto do erro para facilitar a leitura no relatório.
                allure.attach(
                    f"Falha detectada no teste: {test_name}\nErro: {report.longreprtext}",
                    name="Log de Erro",
                    attachment_type=allure.attachment_type.TEXT
                )

            except Exception as e:
                # 24 - Se não conseguir salvar o print, registra a falha de evidência.
                logger.error(f"Erro ao tentar capturar evidência de falha: {e}")
