"""Focused browser behavior for the controlled order UI."""

from __future__ import annotations

import pytest
from playwright.sync_api import Page, expect

from test_framework.config import Settings
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
