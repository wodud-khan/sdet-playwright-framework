"""Wait for an HTTP readiness endpoint with a bounded timeout."""

from __future__ import annotations

import argparse
import time
from urllib.error import HTTPError, URLError
from urllib.request import urlopen


def wait_for_url(url: str, timeout_seconds: float, interval_seconds: float = 0.25) -> None:
    """Poll an HTTP endpoint until it succeeds or the bounded timeout expires."""
    deadline = time.monotonic() + timeout_seconds
    last_error = "no response"

    while time.monotonic() < deadline:
        try:
            with urlopen(url, timeout=min(2, timeout_seconds)) as response:
                if 200 <= response.status < 300:
                    return
                last_error = f"HTTP {response.status}"
        except (HTTPError, URLError, TimeoutError) as error:
            last_error = str(error)
        time.sleep(interval_seconds)

    raise TimeoutError(f"{url} was not ready within {timeout_seconds}s: {last_error}")


def main() -> None:
    """Parse command-line options and wait for service readiness."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--url",
        default="http://127.0.0.1:8000/health",
        help="Readiness URL to poll",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=30,
        help="Maximum number of seconds to wait",
    )
    arguments = parser.parse_args()
    wait_for_url(arguments.url, arguments.timeout)
    print(f"Ready: {arguments.url}")


if __name__ == "__main__":
    main()
