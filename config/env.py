import os


class Env:
    BASE_URL = os.getenv("BASE_URL", "https://www.saucedemo.com")
    API_URL = os.getenv("API_URL", "https://api.saucedemo.fake")
    AUTH_TOKEN = os.getenv("AUTH_TOKEN", "")
