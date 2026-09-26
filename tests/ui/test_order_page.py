"""Focused browser behavior for the controlled order UI."""

from __future__ import annotations

import pytest
from playwright.sync_api import Page, Route, expect

from test_framework.config import Settings
from test_framework.diagnostics import BrowserEvidence
from test_framework.pages.order_page import OrderPage


@pytest.mark.ui
@pytest.mark.smoke
def test_order_page_exposes_critical_controls(
    page: Page,
    ui_settings: Settings,
) -> None:
    order_page = OrderPage(page, ui_settings.app_base_url)

    order_page.open()
    order_page.expect_loaded()


@pytest.mark.ui
def test_customer_name_is_required_before_submission(
    page: Page,
    ui_settings: Settings,
) -> None:
    order_page = OrderPage(page, ui_settings.app_base_url)
    order_page.open()

    order_page.submit.click()

    expect(order_page.customer_name).to_be_focused()
    expect(order_page.result).to_be_hidden()


@pytest.mark.ui
def test_mocked_order_failure_shows_feedback(
    page: Page, ui_settings: Settings, browser_evidence: BrowserEvidence
) -> None:
    order_page = OrderPage(page, ui_settings.app_base_url)
    order_page.open()

    def reject_create(route: Route) -> None:
        route.fulfill(
            status=503, content_type="application/json", body='{"detail":"Try again later"}'
        )

    page.route("**/api/orders", reject_create)
    browser_evidence.expect_http_error("POST", "/api/orders", 503)
    order_page.customer_name.fill("Ada Lovelace")
    order_page.item_name.fill("Quality Notebook")
    order_page.quantity.fill("1")
    order_page.submit.click()

    expect(order_page.form_status).to_have_text("Order could not be created: Try again later")
    expect(order_page.result).to_be_hidden()
