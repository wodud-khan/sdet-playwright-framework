"""
Documents known limitations of third-party APIs used for testing.
This prevents false failures and communicates intent clearly.
"""

API_CAPABILITIES = {
    "jsonplaceholder": {
        "stateful": False,
        "supports_auth": False,
        "supports_crud": "simulated",
        "notes": "POST/PUT/DELETE return success but do not persist data"
    }
}
