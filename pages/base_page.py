# 01 - Importa módulos para trabalhar com caminhos de arquivo, data, buffer de imagem e logs.
from pathlib import Path
from datetime import datetime
import io
import logging
import time

# 02 - Importa a biblioteca diretamente para gerar relatórios Allure.
import allure

# 03 - Importa a biblioteca do Pillow para capturar a tela inteira do computador.
from PIL import ImageGrab

# 04 - Importa utilitários do Selenium para esperas explícitas e condições de visibilidade.
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException

# 05 - Cria um logger específico para essa classe base.
logger = logging.getLogger(__name__)


# 06 - Classe base para todos os Page Objects do projeto.
class BasePage:
    """
    Classe base para o padrão Page Object Model (POM) utilizando Selenium WebDriver.
    Encapsula esperas explícitas, interações com elementos da tela, captura de evidências e registro de logs.
    """

    # 07 - Inicializa o driver e define o tempo padrão de espera.
    def __init__(self, driver, timeout: int = 10):
        self.driver = driver
        self.timeout = timeout
        self.wait = WebDriverWait(driver, timeout)

    # 08 - Abre uma URL no navegador e retorna a própria instância para encadear ações.
    @allure.step("Navegando para a URL: {url}")
    def open(self, url: str):
        """Abre a URL especificada no navegador."""
        logger.info(f"Navegando para URL: {url}")
        try:
            self.driver.get(url)
            return self
        except Exception as e:
            logger.error(f"Falha ao abrir a URL '{url}': {e}")
            self.take_screenshot("falha_abrir_url")
            raise e

    # 09 - Procura um elemento no DOM, sem necessariamente exigir visibilidade imediata.
    @allure.step("Localizando elemento no DOM: {by} = '{value}'")
    def find(self, by, value: str):
        """Aguardar a presença do elemento no DOM."""
        logger.info(f"Localizando elemento no DOM: {by}='{value}'")
        try:
            return self.wait.until(EC.presence_of_element_located((by, value)))
        except TimeoutException:
            logger.error(f"Elemento não localizado no DOM após {self.timeout}s: {by}='{value}'")
            self.take_screenshot(f"erro_find_{value}")
            raise

    # 10 - Espera até que o elemento esteja visível antes de tentar manipular.
    @allure.step("Localizando elemento visível: {by} = '{value}'")
    def find_visible(self, by, value: str):
        """Aguardar até que o elemento esteja visível na interface gráfica."""
        logger.info(f"Aguardando visibilidade do elemento: {by}='{value}'")
        try:
            return self.wait.until(EC.visibility_of_element_located((by, value)))
        except TimeoutException:
            logger.error(f"Elemento não ficou visível após {self.timeout}s: {by}='{value}'")
            self.take_screenshot(f"erro_visibilidade_{value}")
            raise

    # 11 - Clica em um elemento e usa fallback em JavaScript se o clique nativo for bloqueado.
    @allure.step("Clicando no elemento: {by} = '{value}'")
    def click(self, by, value: str) -> bool:
        """Aguardar o elemento ficar clicável e realiza o clique, com fallback em JavaScript."""
        logger.info(f"Clicando no elemento: {by}='{value}'")
        try:
            element = self.wait.until(EC.element_to_be_clickable((by, value)))
            try:
                element.click()
            except ElementClickInterceptedException:
                logger.warning(f"Clique nativo interceptado para {by}='{value}'. Usando fallback em JavaScript.")
                self.driver.execute_script("arguments[0].click();", element)
            return True
        except TimeoutException:
            logger.error(f"Elemento não ficou clicável após {self.timeout}s: {by}='{value}'")
            self.take_screenshot(f"erro_clique_{value}")
            raise

    # 12 - Preenche um campo de texto com o valor informado.
    @allure.step("Preenchendo o campo {by} = '{value}' com o texto: '{text}'")
    def fill(self, by, value: str, text: str) -> bool:
        """Localiza o campo de texto, limpa seu conteúdo atual e insere o novo texto."""
        logger.info(f"Preenchendo campo {by}='{value}' com o valor: '{text}'")
        try:
            element = self.find_visible(by, value)
            element.clear()
            element.send_keys(text)
            return True
        except Exception as e:
            logger.error(f"Falha ao preencher campo {by}='{value}': {e}")
            self.take_screenshot(f"erro_preenchimento_{value}")
            raise e

    # 13 - Lê o texto visível de um elemento.
    @allure.step("Obtendo texto do elemento: {by} = '{value}'")
    def get_text(self, by, value: str) -> str:
        """Retorna o texto visível contido no elemento."""
        logger.info(f"Obtendo texto do elemento {by}='{value}'")
        try:
            element = self.find_visible(by, value)
            text = element.text
            logger.info(f"Texto obtido: '{text}'")
            return text
        except Exception as e:
            logger.error(f"Falha ao obter texto de {by}='{value}': {e}")
            self.take_screenshot(f"erro_get_text_{value}")
            raise e

    # 14 - Verifica se um elemento está visível em um timeout menor e retorna booleano.
    @allure.step("Verificando se o elemento está visível: {by} = '{value}'")
    def is_displayed(self, by, value: str, custom_timeout: int = 3) -> bool:
        """Verifica se um elemento está visível na tela dentro de um timeout reduzido."""
        logger.info(f"Verificando visibilidade do elemento: {by}='{value}' (timeout={custom_timeout}s)")
        try:
            custom_wait = WebDriverWait(self.driver, custom_timeout)
            element = custom_wait.until(EC.visibility_of_element_located((by, value)))
            return element.is_displayed()
        except (TimeoutException, NoSuchElementException):
            logger.info(f"Elemento {by}='{value}' não está visível.")
            return False

    # 15 - Faz uma pausa curta para dar tempo da tela renderizar antes de capturar.
    @staticmethod
    def wait_for_screen_load(seconds: float = 1.0):
        """Aguarda um tempo curto para a página/renderização ficar estável antes da captura."""
        time.sleep(seconds)

    # 16 - Captura a tela do computador inteira e anexa ao Allure.
    @allure.step("Capturando evidência de tela: {name}")
    def take_screenshot(self, name: str = "evidencia", folder: str = "geral") -> str:
        """Captura a tela inteira do monitor, salva em disco na pasta img/<folder>/ e anexa ao Allure Report."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        file_label = f"{timestamp}_{name}"

        try:
            self.wait_for_screen_load(0.8)
            img_dir = Path("img") / folder
            img_dir.mkdir(parents=True, exist_ok=True)
            filepath = img_dir / f"{file_label}.png"

            screenshot = ImageGrab.grab(all_screens=True)
            screenshot.save(filepath)

            buffer = io.BytesIO()
            screenshot.save(buffer, format="PNG")
            allure.attach(
                buffer.getvalue(),
                name=file_label,
                attachment_type=allure.attachment_type.PNG
            )
            logger.info(f"Evidência da tela do computador salva em '{filepath}' e anexada ao Allure Report.")
            return str(filepath)
        except Exception as e:
            logger.warning(f"Falha ao capturar a tela inteira do monitor: {e}. Tentando fallback no navegador.")
            try:
                fallback_dir = Path("img") / folder
                fallback_dir.mkdir(parents=True, exist_ok=True)
                fallback_path = fallback_dir / f"{file_label}.png"
                if hasattr(self.driver, "save_screenshot"):
                    self.driver.save_screenshot(str(fallback_path))
                    allure.attach(
                        self.driver.get_screenshot_as_png(),
                        name=file_label,
                        attachment_type=allure.attachment_type.PNG
                    )
                    logger.info(f"Fallback do navegador salvo em '{fallback_path}'.")
                    return str(fallback_path)
            except Exception as fallback_error:
                logger.error(f"Falha também no fallback do navegador: {fallback_error}")
            return ""
