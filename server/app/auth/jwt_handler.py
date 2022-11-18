# This file is responsible for signing, encoding, decoding and returning JWTs.

import time
import jwt
from decouple import config
from jwt import exceptions

JWT_SECRET = config("secret")
JWT_ALGORITHM = config("algorithm")


# Function returns generated tokens (JWTs)
def token_response(token: str):
    return {
        "access token": token
    }


# Function sign JWT token - ecode token and returns signed token
def sign_jwt(user_id: str):
    payload = {
        "user_id": user_id,
        "exp": time.time() + 600,
    }
    encoded_token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token_response(encoded_token)


# Function decode JWT then returns decoded token
def decode_jwt(token: str):
    try:
        decode_token = jwt.decode(token, JWT_SECRET, algorithms=JWT_ALGORITHM)
    except jwt.ExpiredSignatureError:
        msg = 'Signature has expired.'
        raise exceptions.ExpiredSignatureError(msg)
    except jwt.DecodeError:
        msg = 'Error decoding signature.'
        raise exceptions.DecodeError(msg)
    except jwt.InvalidTokenError:
        raise exceptions.InvalidTokenError()

    return decode_token
