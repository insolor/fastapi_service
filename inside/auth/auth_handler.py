import time
from typing import Dict

import jwt
from decouple import config


JWT_SECRET = config("secret")
JWT_ALGORITHM = config("algorithm")


def token_response(token: str):
    return {
        "token": token
    }


def sign_jwt(user_id: str) -> Dict[str, str]:
    payload = {
        "user_id": user_id,
        "expires": time.time() + 600
    }
    token = jwt.encode(payload, JWT_SECRET, JWT_ALGORITHM)

    return token_response


def decode_jwt(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return decoded_token if decoded_token["expires"] >= time.time() else None
    except:
        return {}
