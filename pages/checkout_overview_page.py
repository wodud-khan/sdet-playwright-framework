from pages.base_page import BasePage
from playwright.sync_api import Page


class CheckoutOverviewPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

    def get_item_total(self) -> float:
        text = self.page.locator(".summary_subtotal_label").inner_text()
        return float(text.replace("Item total: $", ""))

    def get_tax(self) -> float:
        text = self.page.locator(".summary_tax_label").inner_text()
        return float(text.replace("Tax: $", ""))

    def get_total(self) -> float:
        text = self.page.locator(".summary_total_label").inner_text()
        return float(text.replace("Total: $", ""))

    def finish_checkout(self):
        self.page.locator("#finish").click()
