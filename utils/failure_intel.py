def analyze_failure(exception):
    if "Timeout" in str(exception):
        return "TIMEOUT_FAILURE"
    if "401" in str(exception):
        return "AUTH_FAILURE"
    return "UNKNOWN_FAILURE"
