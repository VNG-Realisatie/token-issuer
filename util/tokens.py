import time

import jwt


# todo: payload = {"exp": datetime.datetime.utcnow() + datetime.timedelta(days=7)}
def create_token(identifier: str, secret: str):
    payload = {
        "iss": identifier,
        "iat": int(time.time()),
        "client_id": identifier,
    }

    headers = {"client_identifier": identifier}
    return jwt.encode(payload, key=secret, headers=headers, algorithm="HS256")
