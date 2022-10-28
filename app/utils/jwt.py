import datetime

import jwt
from calendar import timegm
from jwt.exceptions import ExpiredSignatureError, InvalidSignatureError, DecodeError

from app.config_reader import config

TTL_AT = config.TTL_ACCESS_TOKEN
TTL_RT = config.TTL_REFRESH_TOKEN


async def create_token(user_id: int, type_token: str):
    exp = timegm((datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(
        minutes=TTL_AT if type_token == "access" else TTL_RT)).utctimetuple())
    token = jwt.encode(payload={"user_id": user_id,
                                "exp": exp},
                       key=config.SECRET_KEY,
                       headers={"type": "JWT",
                                "type_token": type_token,
                                "alg": "HS256"},
                       algorithm="HS256")
    return token, exp


async def check_token(token: str):
    try:
        if token is None:
            raise InvalidSignatureError
        data = jwt.decode(jwt=token, key=config.SECRET_KEY, algorithms="HS256",
                          verify_signature=True, leeway=10)
    except (InvalidSignatureError, DecodeError):
        return {"status": "error", "message": "invalid token"}
    except ExpiredSignatureError:
        return {"status": "error", "message": "token has expired"}
    else:
        return {"status": "ok", "message": "correct token", "data": data}
