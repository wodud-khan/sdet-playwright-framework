import pytest
from api.endpoints.auth_api import AuthAPI


@pytest.mark.api
def test_auth_invalid_credentials():
    auth = AuthAPI()
    response = auth.login(
        "wrong@example.com",
        "wrongpass"
    )

    assert response.status_code == 200
    assert response.json()["detail"] == "Invalid credentials"
