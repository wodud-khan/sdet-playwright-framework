import pytest
import allure

from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from pages.checkout_overview_page import CheckoutOverviewPage
from pages.checkout_complete_page import CheckoutCompletePage


@pytest.mark.ui
@pytest.mark.regression
@allure.feature("End-to-End")
@allure.story("User completes full purchase flow")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.ui
def test_e2e_purchase_flow(page):

    login = LoginPage(page)
    inventory = InventoryPage(page)
    cart = CartPage(page)
    checkout = CheckoutPage(page)
    overview = CheckoutOverviewPage(page)
    complete = CheckoutCompletePage(page)

    with allure.step("Login with valid user"):
        login.open()
        login.login("standard_user", "secret_sauce")
        assert inventory.is_loaded()

    with allure.step("Add product to cart"):
        inventory.add_item("Sauce Labs Backpack")
        assert inventory.cart_count() == 1

    with allure.step("Open cart and proceed to checkout"):
        cart.open()
        item_price = cart.get_item_price("Sauce Labs Backpack")
        cart.checkout()

    with allure.step("Enter checkout information"):
        checkout.enter_details("John", "Doe", "12345")
        checkout.continue_checkout()

    with allure.step("Validate pricing and totals"):
        item_total = overview.get_item_total()
        tax = overview.get_tax()
        total = overview.get_total()

        assert item_total == item_price
        assert tax > 0
        assert total == item_total + tax

    with allure.step("Complete the order"):
        overview.finish_checkout()

    with allure.step("Verify order confirmation"):
        assert complete.is_order_successful()
        assert complete.get_header_text() == "Thank you for your order!"
