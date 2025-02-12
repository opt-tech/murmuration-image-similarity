import os


def is_running_on_cloudrun() -> bool:
    return os.getenv("K_SERVICE") is not None
