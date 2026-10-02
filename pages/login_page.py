# 01 - Importa módulos para logs, relatórios e seletores do Selenium.
import logging
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from pages.base_page import BasePage

# 02 - Cria logger específico dessa página.
logger = logging.getLogger(__name__)


# 03 - Classe responsável por representar a página de login da SauceDemo.
class LoginPage(BasePage):
    """
    Page Object responsável pelo mapeamento dos elementos e pelas ações da Tela de Login.
    Herda os métodos de espera explícita e interação com o Selenium da classe BasePage.
    """

    # 04 - URL padrão da aplicação de testes.
    DEFAULT_URL = "https://www.saucedemo.com/"

    # 05 - Seletores dos campos e botões da página de login.
    USERNAME_INPUT = (By.ID, "user-name")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")
    SUCCESS_TITLE = (By.CLASS_NAME, "title")
    INVENTORY_ITEMS = (By.CLASS_NAME, "inventory_item")
    ERROR_CONTAINER = (By.CSS_SELECTOR, "[data-test='error']")

    # 06 - Construtor da página; reutiliza a lógica base da classe BasePage.
    def __init__(self, driver, timeout=10):
        super().__init__(driver, timeout=timeout)

    # 07 - Abre a página inicial de login e registra a evidência.
    @allure.step("Navegando até a página de login")
    def open_login_page(self, url: str = None) -> "LoginPage":
        """Abre a página de login informada ou a URL padrão."""
        target_url = url or self.DEFAULT_URL
        logger.info(f"Acessando a URL de login: {target_url}")
        self.open(target_url)
        self.wait_for_screen_load(1.2)
        self.take_screenshot("login_page_aberta", folder="login")
        return self

    # 08 - Preenche o campo de usuário.
    @allure.step("Preenchendo o nome de usuário: '{username}'")
    def enter_username(self, username: str) -> "LoginPage":
        """Preenche o campo de usuário."""
        logger.info(f"Preenchendo usuário: {username}")
        self.fill(*self.USERNAME_INPUT, text=username)
        self.wait_for_screen_load(1.0)
        self.take_screenshot(f"usuario_{username}", folder="login")
        return self

    # 09 - Preenche o campo de senha.
    @allure.step("Preenchendo o campo de senha")
    def enter_password(self, password: str) -> "LoginPage":
        """Preenche o campo de senha."""
        logger.info("Preenchendo campo de senha...")
        self.fill(*self.PASSWORD_INPUT, text=password)
        self.wait_for_screen_load(1.0)
        self.take_screenshot("senha_digitada", folder="login")
        return self

    # 10 - Clica no botão de login e registra a tela logo após o clique.
    @allure.step("Clicando no botão de Login")
    def click_login_button(self) -> None:
        """Clica no botão de submissão do formulário de login."""
        logger.info("Clicando no botão de login...")
        self.click(*self.LOGIN_BUTTON)
        self.wait_for_screen_load(1.2)

    # 11 - Executa o fluxo completo de autenticação com validação condicional.
    @allure.step("Efetuando login completo com o usuário: '{username}'")
    def login(self, username: str, password: str) -> None:
        """
        Executa a sequência completa de autenticação:
        1. Preenche usuário
        2. Preenche senha
        3. Clica no botão de login
        4. Espera a página de produtos ou a mensagem de erro aparecer
        """
        logger.info(f"Iniciando tentativa de login para o usuário '{username}'...")
        self.enter_username(username)
        self.enter_password(password)
        self.click_login_button()

        # 12 - Espera a tela de produtos ou, em caso de erro, espera o container de erro.
        try:
            self.wait.until(EC.visibility_of_element_located(self.INVENTORY_ITEMS))
        except TimeoutException:
            self.wait.until(EC.visibility_of_element_located(self.ERROR_CONTAINER))

    # 13 - Confirma se o login foi bem-sucedido pela presença do título da página principal.
    @allure.step("Verificando se o login foi efetuado com sucesso")
    def is_login_successful(self) -> bool:
        """Verifica se o título da página principal ('Products') é exibido."""
        logger.info("Validando sucesso na autenticação...")
        result = self.is_displayed(*self.SUCCESS_TITLE)
        if result:
            self.wait_for_screen_load(1.3)
            self.take_screenshot("login_sucesso", folder="login")
        return result

    # 14 - Retorna a mensagem de erro exibida por falha de autenticação.
    @allure.step("Obtendo mensagem de erro exibida na tela")
    def get_error_message(self) -> str:
        """Retorna o texto da mensagem de erro informada na tela de login."""
        logger.info("Obtendo texto da mensagem de erro...")
        return self.get_text(*self.ERROR_CONTAINER)
