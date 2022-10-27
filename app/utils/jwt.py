import datetime

import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidSignatureError

from app.config_reader import config

TTL_AT = config.TTL_ACCESS_TOKEN
TTL_RT = config.TTL_REFRESH_TOKEN


async def create_token(user_id: int, type_token: str):
    access_token = jwt.encode(payload={"user_id": user_id,
                                       "exp": datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(
                                           minutes=TTL_AT if type_token == "access" else TTL_RT)
                                       },
                              key=config.SECRET_KEY,
                              headers={"type": "access_jwt" if type_token == "access" else "refresh_jwt",
                                       "alg": "HS256"},
                              algorithm="HS256")
    return access_token


async def check_token(token: str):
    try:
        if token is None:
            raise InvalidSignatureError
        payload = jwt.decode(jwt=token, key=config.SECRET_KEY, algorithms="HS256",
                             verify_signature=True, leeway=10)
    except InvalidSignatureError:
        return {"status": "error", "message": "invalid token"}
    except ExpiredSignatureError:
        return {"status": "error", "message": "token has expired"}
    else:
        return {"status": "ok", "message": "correct token", "payload": payload}


async def decode_token(token: str):
    payload = jwt.decode(jwt=token, key=config.SECRET_KEY, algorithms="HS256",
                         verify_signature=True, leeway=10)
