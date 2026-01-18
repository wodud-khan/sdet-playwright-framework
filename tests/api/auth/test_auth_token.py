import allure
import pytest
from api.endpoints.auth_api import AuthAPI


@allure.feature("API Authentication")
@allure.story("Valid Token Generation")
@pytest.mark.api
def test_auth_token_success():
    auth = AuthAPI()
    response = auth.login(
        "test.user@example.com",
        "password123"
    )

    assert response.status_code == 200
    assert "access_token" in response.json()
