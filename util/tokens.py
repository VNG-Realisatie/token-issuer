import time

import jwt


def create_token(identifier: str, secret: str):
    payload = {
        "iss": identifier,
        "iat": int(time.time()),
        "client_id": identifier,
        "user_id": "",
        "user_representation": "",
    }

    headers = {"client_identifier": identifier}
    return jwt.encode(payload, key=secret, headers=headers, algorithm="HS256")
