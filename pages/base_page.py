from utils.logger import get_logger

logger = get_logger("ui.page")


class BasePage:
    def __init__(self, page):
        self.page = page

    def goto(self, url: str):
        logger.info(f"Navigating to URL: {url}")
        self.page.goto(url)

    def click(self, selector: str):
        logger.info(f"Clicking element: {selector}")
        self.page.click(selector)

    def fill(self, selector: str, value: str):
        logger.info(f"Filling element: {selector} with value: {value}")
        self.page.fill(selector, value)

    def wait_for_selector(self, selector: str):
        logger.info(f"Waiting for selector: {selector}")
        self.page.wait_for_selector(selector)

    def get_text(self, selector: str) -> str:
        logger.info(f"Getting text from selector: {selector}")
        return self.page.inner_text(selector)
