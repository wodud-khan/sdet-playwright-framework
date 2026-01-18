import pytest
import allure

from api.endpoints.user_api import UserAPI


@allure.feature("API Users")
@allure.story("Create User Contract Validation")
@pytest.mark.api
def test_user_create_contract():
    api = UserAPI()

    payload = {
        "name": "John Doe",
        "email": "john@example.com"
    }

    response = api.create_user(payload)

    assert response.status_code == 201

    body = response.json()
    assert "id" in body
    assert body["name"] == payload["name"]
