# 01 - Importa módulos para logs e interações específicas da tela de produtos.
import logging

# 02 - Importa seletores e utilitários do Selenium.
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

# 03 - Importa a base comum para todos os POMs.
from pages.base_page import BasePage

# 04 - Cria o logger do módulo.
logger = logging.getLogger(__name__)


# 05 - Classe que representa a página de produtos da SauceDemo.
class InventoryPage(BasePage):
    """Page Object para a tela de catálogo de produtos da SauceDemo."""

    # 06 - Seletores usados para localizar itens, seleção e badge do carrinho.
    INVENTORY_ITEMS = (By.CLASS_NAME, "inventory_item")
    SORT_DROPDOWN = (By.CLASS_NAME, "product_sort_container")
    SHOPPING_CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")

    # 07 - Inicializa a página da mesma forma que a base.
    def __init__(self, driver, timeout=10):
        super().__init__(driver, timeout=timeout)

    # 08 - Adiciona um produto ao carrinho pelo nome exibido na lista.
    def add_product_to_cart(self, product_name: str) -> None:
        """Adiciona um produto ao carrinho pelo nome exibido na página."""
        logger.info(f"Adicionando produto ao carrinho: {product_name}")

        # 09 - Busca o botão do produto em questão dentro da lista de itens.
        def find_product_button(driver):
            for product in driver.find_elements(*self.INVENTORY_ITEMS):
                try:
                    if product.find_element(By.CLASS_NAME, "inventory_item_name").text == product_name:
                        button = product.find_element(By.TAG_NAME, "button")
                        if button.is_displayed():
                            return button
                except Exception:
                    continue
            return None

        # 10 - Espera até que o botão do produto esteja disponível para clique.
        button = WebDriverWait(self.driver, 10).until(
            find_product_button,
            message=f"Botão do produto '{product_name}' não ficou disponível para clique."
        )

        # 11 - Executa o clique no botão do produto escolhido.
        button.click()

        # 12 - Valida se o carrinho foi atualizado após o clique, observando badge ou estado do botão.
        def cart_updated(driver):
            badge = driver.find_elements(*self.SHOPPING_CART_BADGE)
            if badge:
                badge_text = badge[0].text.strip()
                if badge_text == "1":
                    return True

            for current_product in driver.find_elements(*self.INVENTORY_ITEMS):
                try:
                    current_title = current_product.find_element(By.CLASS_NAME, "inventory_item_name").text
                    if current_title == product_name:
                        current_button = current_product.find_element(By.TAG_NAME, "button")
                        if current_button.text.strip().lower() == "remove":
                            return True
                except Exception:
                    continue
            return False

        # 13 - Espera o carrinho mostrar alteração real antes de continuar.
        WebDriverWait(self.driver, 10).until(
            cart_updated,
            message=f"Carrinho não foi atualizado após adicionar '{product_name}'."
        )
        logger.info(f"Produto '{product_name}' adicionado com sucesso.")

    # 14 - Ordena os produtos do menor preço para o maior.
    def sort_by_price_low_to_high(self) -> None:
        """Ordena os produtos pelo menor preço."""
        logger.info("Ordenando produtos por preço crescente.")
        select = Select(self.driver.find_element(*self.SORT_DROPDOWN))
        select.select_by_value("lohi")

    # 15 - Coleta os preços atuais da página em ordem de exibição.
    def get_product_prices(self) -> list[str]:
        """Retorna a lista de preços dos produtos em ordem atual da página."""
        prices = []
        products = self.driver.find_elements(*self.INVENTORY_ITEMS)

        for product in products:
            price_text = product.find_element(By.CLASS_NAME, "inventory_item_price").text
            prices.append(float(price_text.replace("$", "")))

        logger.info(f"Preços da página de produtos: {prices}")
        return prices

    # 16 - Lê o valor do badge do carrinho, se existir.
    def get_cart_count(self) -> str:
        """Retorna o número exibido no badge do carrinho ou 0 se o carrinho estiver vazio."""
        try:
            badge = self.driver.find_elements(*self.SHOPPING_CART_BADGE)
            if badge:
                count = badge[0].text.strip()
                logger.info(f"Badge do carrinho: '{count}'")
                return count or "0"

            logger.info("Carrinho vazio, sem badge de contador.")
            return "0"
        except (NoSuchElementException, Exception):
            logger.info("Carrinho vazio, sem badge de contador.")
            return "0"
