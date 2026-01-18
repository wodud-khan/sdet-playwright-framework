import pytest
import allure

from pages.login_page import LoginPage
from utils.logger import get_logger

logger = get_logger(__name__)


@pytest.mark.negative
@pytest.mark.smoke
@allure.feature("Authentication")
@allure.story("Invalid Login Scenarios")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.ui
@pytest.mark.parametrize(
    "username,password,expected_error",
    [
        ("invalid_user", "secret_sauce", "Username and password do not match"),
        ("standard_user", "wrong_password", "Username and password do not match"),
        ("", "secret_sauce", "Username is required"),
        ("standard_user", "", "Password is required"),
        ("locked_out_user", "secret_sauce", "Sorry, this user has been locked out"),
    ]
)
def test_invalid_login(page, username, password, expected_error):

    login = LoginPage(page)

    with allure.step("Open login page"):
        login.open()

    with allure.step(f"Attempt login with username='{username}'"):
        login.login(username, password)

    with allure.step("Verify correct error message is displayed"):
        actual_error = login.get_error_message()
        logger.info(f"Login error displayed: {actual_error}")
        assert expected_error in actual_error
        # assert "INTENTIONAL FAILURE" in actual_error
