import allure
import pytest

from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from utils.data_factory import UserFactory
from utils.logger import get_logger

logger = get_logger(__name__)


@allure.feature("Authentication")
@allure.story("Valid User Login")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.ui
def test_valid_login(page):
    """
    Verify that a valid user can log in and reach the inventory page.
    """

    # Arrange
    user = UserFactory.valid_user()
    login_page = LoginPage(page)
    inventory_page = InventoryPage(page)

    with allure.step("Navigate to SauceDemo login page"):
        login_page.open()
        logger.info("Opened login page")

    with allure.step("Login using valid credentials"):
        login_page.login(
            username=user["username"],
            password=user["password"]
        )
        logger.info(f"Entered credentials for user: {user['username']}")

    with allure.step("Verify inventory page is loaded"):
        assert inventory_page.is_loaded(), "Inventory page did not load"
        logger.info("Inventory page loaded successfully")

    with allure.step("Verify inventory page title"):
        assert inventory_page.get_title() == "Products", "Incorrect inventory page title"
        logger.info("Inventory page title validated successfully")
