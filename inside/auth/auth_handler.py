import binascii
import os
import time
from typing import Optional

import jwt
from decouple import config

JWT_SECRET = config("JWT_SECRET", default=binascii.hexlify(os.urandom(24)).decode())
JWT_ALGORITHM = config("JWT_ALGORITHM", default="HS256")


def sign_jwt(user_id: str) -> str:
    payload = {
        "user_id": user_id,
        "expires": time.time() + 600,
    }
    return jwt.encode(payload, JWT_SECRET, JWT_ALGORITHM)


def decode_jwt(token: str) -> Optional[dict]:
    try:
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        if decoded_token["expires"] >= time.time():
            return decoded_token
    except Exception:
        pass

    return None
