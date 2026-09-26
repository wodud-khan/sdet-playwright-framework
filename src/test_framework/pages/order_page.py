"""Order-page behavior expressed through semantic Playwright locators."""

from __future__ import annotations

from typing import Any

from playwright.sync_api import Page, expect


class OrderPage:
    """Focused interaction boundary for the controlled order UI."""

    def __init__(self, page: Page, base_url: str) -> None:
        self.page = page
        self.base_url = base_url.rstrip("/")
        self.customer_name = page.get_by_label("Customer name")
        self.item_name = page.get_by_label("Item name")
        self.quantity = page.get_by_label("Quantity")
        self.submit = page.get_by_role("button", name="Create order")
        self.result = page.get_by_role("region", name="Order created")
        self.order_id = page.get_by_test_id("order-id")
        self.order_status = page.get_by_test_id("order-status")
        self.order_total = page.get_by_test_id("order-total")
        self.form_status = page.get_by_role("status")

    def open(self) -> None:
        self.page.goto(self.base_url)
        expect(self.page).to_have_title("Order Lab")

    def expect_loaded(self) -> None:
        expect(self.page.get_by_role("heading", name="Order Lab")).to_be_visible()
        expect(self.customer_name).to_be_visible()
        expect(self.item_name).to_be_visible()
        expect(self.quantity).to_be_visible()
        expect(self.submit).to_be_enabled()

    def submit_order(
        self, customer_name: str, item_name: str, quantity: int
    ) -> tuple[int, dict[str, Any]]:
        """Capture the response before the caller checks the resulting UI."""
        self.customer_name.fill(customer_name)
        self.item_name.fill(item_name)
        self.quantity.fill(str(quantity))

        with self.page.expect_response(
            lambda response: (
                response.url.endswith("/api/orders") and response.request.method == "POST"
            )
        ) as response_info:
            self.submit.click()

        response = response_info.value
        body: dict[str, Any] = response.json()
        return response.status, body

    def expect_order_saved(self, order_id: str, expected_total_cents: int) -> None:
        """Check displayed values against the test's independent expectation."""
        expect(self.result).to_be_visible()
        expect(self.order_id).to_have_text(order_id)
        expect(self.order_status).to_have_text("created")
        expect(self.order_total).to_have_text(
            f"${expected_total_cents // 100}.{expected_total_cents % 100:02d}"
        )
        expect(self.form_status).to_have_text("Order saved.")
