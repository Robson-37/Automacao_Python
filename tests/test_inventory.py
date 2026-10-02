# 01 - Importa as bibliotecas para relatórios Allure e fixture do pytest.
import allure
import pytest

# 02 - Importa as páginas necessárias para autenticação e catálogo de produtos.
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage


# 03 - Agrupa os testes do módulo de produtos em uma classe.
@allure.epic("Automação Web - Selenium")
@allure.feature("Módulo de Produtos")
class TestInventory:

    # 04 - Define a URL base da aplicação usada em todos os testes desta classe.
    URL_TESTE = "https://www.saucedemo.com/"

    # 05 - Fixture executada antes de cada teste para logar e abrir a tela de produtos.
    @pytest.fixture(autouse=True)
    def setup_produtos(self, driver):
        self.login_page = LoginPage(driver)
        self.login_page.open_login_page(self.URL_TESTE)
        self.login_page.login("standard_user", "secret_sauce")
        self.inventory_page = InventoryPage(driver)

    # 06 - Teste que valida a funcionalidade de adicionar um produto ao carrinho.
    @allure.story("Adicionar produto ao carrinho")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_adicionar_produto_ao_carrinho(self):
        with allure.step("Adicionar o produto 'Sauce Labs Backpack' ao carrinho"):
            self.inventory_page.add_product_to_cart("Sauce Labs Backpack")

        with allure.step("Validar contador do carrinho"):
            assert self.inventory_page.get_cart_count() == "1", "O carrinho não foi atualizado corretamente."

    # 07 - Teste que valida a ordenação dos produtos por preço crescente.
    @allure.story("Ordenar produtos por preço crescente")
    @allure.severity(allure.severity_level.NORMAL)
    def test_ordenar_produtos_por_preco_crescente(self):
        with allure.step("Selecionar ordenação por preço do menor para o maior"):
            self.inventory_page.sort_by_price_low_to_high()

        with allure.step("Validar a ordem dos preços exibidos"):
            precos = self.inventory_page.get_product_prices()
            assert precos == sorted(precos, key=float), "A ordenação por preço não foi aplicada corretamente."
