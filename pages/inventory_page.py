from pages.base_page import BasePage
from playwright.sync_api import Page


class InventoryPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

    def is_loaded(self) -> bool:
        return self.page.locator(".inventory_list").is_visible()

    def get_title(self) -> str:
        return self.page.locator(".title").inner_text()

    def add_item(self, item_name: str):
        self.page.locator(
            f"//div[text()='{item_name}']/ancestor::div[@class='inventory_item']//button"
        ).click()

    def cart_count(self) -> int:
        badge = self.page.locator(".shopping_cart_badge")
        return int(badge.inner_text()) if badge.is_visible() else 0

    def get_all_prices(self):
        prices = self.page.locator(".inventory_item_price").all_inner_texts()
        return [float(p.replace("$", "")) for p in prices]
