import requests


class AuthAPI:
    def __init__(self, base_url="http://localhost:8001"):
        self.base_url = base_url

    def login(self, email: str, password: str):
        return requests.post(
            f"{self.base_url}/auth/login",
            json={"email": email, "password": password},
            timeout=5
        )
