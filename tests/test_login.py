# 01 - Importa as bibliotecas para relatório e fixtures do pytest.
import allure
import pytest

# 02 - Importa a página de login para usar seus métodos.
from pages.login_page import LoginPage


# 03 - Agrupa todos os testes de autenticação em uma classe.
@allure.epic("Automação Web - Selenium")
@allure.feature("Módulo de Autenticação")
class TestLogin:

    # 04 - Define a URL base do sistema de teste.
    URL_TESTE = "https://www.saucedemo.com/"

    # 05 - Fixture executada antes de cada teste para abrir a página de login.
    @pytest.fixture(autouse=True)
    def setup_pagina(self, driver):
        """Fixture que é executada antes de cada teste para inicializar e abrir a página de login."""
        self.login_page = LoginPage(driver)
        self.login_page.open_login_page(self.URL_TESTE)

    # 06 - Teste de login bem-sucedido.
    @allure.story("Login com Sucesso")
    @allure.severity(allure.severity_level.BLOCKER)
    @allure.description("Valida se um usuário com credenciais válidas consegue se autenticar com sucesso.")
    def test_login_com_sucesso(self):
        with allure.step("Efetuar login com credenciais válidas"):
            self.login_page.login("standard_user", "secret_sauce")

        with allure.step("Validar redirecionamento e exibição da página de produtos"):
            assert self.login_page.is_login_successful(), "O login falhou. A página principal de produtos não foi carregada."

    # 07 - Teste de login com senha incorreta.
    @allure.story("Login com Senha Incorreta")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("Valida se a mensagem de erro apropriada é exibida ao informar uma senha incorreta.")
    def test_login_senha_incorreta(self):
        with allure.step("Tentar login com senha incorreta"):
            self.login_page.login("standard_user", "senha_errada")

        with allure.step("Validar mensagem de erro na tela"):
            mensagem_erro = self.login_page.get_error_message()
            assert "Username and password do not match" in mensagem_erro, f"Mensagem de erro inesperada: '{mensagem_erro}'"

    # 08 - Teste de login com usuário bloqueado.
    @allure.story("Login com Usuário Bloqueado")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.description("Valida o bloqueio de acesso para usuários desativados no sistema.")
    def test_login_usuario_bloqueado(self):
        with allure.step("Tentar login com usuário bloqueado"):
            self.login_page.login("locked_out_user", "secret_sauce")

        with allure.step("Validar mensagem de usuário bloqueado"):
            mensagem_erro = self.login_page.get_error_message()
            assert "Sorry, this user has been locked out" in mensagem_erro, f"Mensagem de erro inesperada: '{mensagem_erro}'"

    # 09 - Teste de campos vazios no formulário.
    @allure.story("Login com Campos Vazios")
    @allure.severity(allure.severity_level.MINOR)
    @allure.description("Valida a validação de campos obrigatórios ao tentar submeter o formulário em branco.")
    def test_login_campos_vazios(self):
        with allure.step("Clicar no botão de login sem preencher usuário e senha"):
            self.login_page.click_login_button()

        with allure.step("Validar mensagem de exigência do nome de usuário"):
            mensagem_erro = self.login_page.get_error_message()
            assert "Username is required" in mensagem_erro, f"Mensagem de erro inesperada: '{mensagem_erro}'"
