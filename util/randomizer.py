import random
import string


def create_random_id(prefix) -> str:
    return f"{prefix}-{create_random_string(size=12)}"


def create_random_string(size=12):
    return "".join(
        random.SystemRandom().choice(string.ascii_letters + string.digits)
        for _ in range(size)
    )
