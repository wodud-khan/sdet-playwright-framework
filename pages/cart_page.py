from pages.base_page import BasePage
from playwright.sync_api import Page


class CartPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

    def open(self):
        self.page.locator(".shopping_cart_link").click()

    def item_exists(self, item_name: str) -> bool:
        return self.page.locator(
            f"//div[@class='inventory_item_name' and text()='{item_name}']"
        ).is_visible()

    def get_item_price(self, item_name: str) -> float:
        price_text = self.page.locator(
            f"//div[text()='{item_name}']/ancestor::div[@class='cart_item']//div[@class='inventory_item_price']"
        ).inner_text()
        return float(price_text.replace("$", ""))

    def checkout(self):
        self.page.locator("#checkout").click()
