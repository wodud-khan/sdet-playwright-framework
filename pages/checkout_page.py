from pages.base_page import BasePage
from playwright.sync_api import Page


class CheckoutPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

    def enter_details(self, first_name: str, last_name: str, postal_code: str):
        self.page.fill("#first-name", first_name)
        self.page.fill("#last-name", last_name)
        self.page.fill("#postal-code", postal_code)

    def continue_checkout(self):
        self.page.locator("#continue").click()

    def get_error_message(self) -> str:
        error = self.page.locator("[data-test='error']")
        return error.inner_text() if error.is_visible() else ""
