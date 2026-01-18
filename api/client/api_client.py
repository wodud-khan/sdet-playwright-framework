import requests
from utils.logger import get_logger
from api.client.api_config import BASE_URL, TIMEOUT

logger = get_logger(__name__)


class ApiClient:
    def __init__(self, token=None):
        self.session = requests.Session()
        self.session.headers.update({"Content-Type": "application/json"})

        if token:
            self.session.headers.update(
                {"Authorization": f"Bearer {token}"}
            )

        self.session.hooks["response"] = [self._log_response]

    def _log_response(self, response, *args, **kwargs):
        logger.info(
            f"{response.request.method} {response.url} "
            f"[{response.status_code}]"
        )
        return response

    def get(self, endpoint):
        return self.session.get(
            f"{BASE_URL}{endpoint}", timeout=TIMEOUT
        )

    def post(self, endpoint, payload):
        return self.session.post(
            f"{BASE_URL}{endpoint}", json=payload, timeout=TIMEOUT
        )

    def put(self, endpoint, payload):
        return self.session.put(
            f"{BASE_URL}{endpoint}", json=payload, timeout=TIMEOUT
        )

    def delete(self, endpoint):
        return self.session.delete(
            f"{BASE_URL}{endpoint}", timeout=TIMEOUT
        )
