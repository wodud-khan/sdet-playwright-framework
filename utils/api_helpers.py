def is_json_response(response):
    return response.headers.get("Content-Type", "").startswith("application/json")
