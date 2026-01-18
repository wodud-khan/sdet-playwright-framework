from pages.base_page import BasePage
from playwright.sync_api import Page


class CheckoutCompletePage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

    def get_header_text(self) -> str:
        return self.page.locator(".complete-header").inner_text()

    def get_confirmation_text(self) -> str:
        return self.page.locator(".complete-text").inner_text()

    def back_to_home(self):
        self.page.locator("#back-to-products").click()

    def is_order_successful(self) -> bool:
        return self.page.locator(".complete-header").is_visible()
