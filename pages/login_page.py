class LoginPage:
    URL = "https://www.saucedemo.com/"

    def __init__(self, page):
        self.page = page

    def open(self):
        self.page.goto(self.URL)

    def login(self, username, password):
        self.page.fill("#user-name", username)
        self.page.fill("#password", password)
        self.page.click("#login-button")

    def is_logged_in(self):
        return self.page.url.endswith("inventory.html")

    def get_error_message(self) -> str:
        error = self.page.locator("[data-test='error']")
        return error.inner_text() if error.is_visible() else ""
