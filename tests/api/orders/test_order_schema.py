import pytest
import allure
from api.client.api_client import ApiClient
from utils.schema_validator import validate_schema
import json

with open("contracts/user_schema.json") as f:
    USER_SCHEMA = json.load(f)


@allure.feature("API Schema")
@allure.story("User Contract Validation")
@pytest.mark.api
def test_user_schema():
    client = ApiClient()
    response = client.get("/users/1")

    assert response.status_code == 200
    validate_schema(response.json(), USER_SCHEMA)
