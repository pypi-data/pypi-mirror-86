from datetime import datetime
from guillotina.utils import get_jwk_key
from jwcrypto import jwe
from jwcrypto.common import json_encode

import logging
import orjson
import time


logger = logging.getLogger("guillotina.email_validation")


async def generate_validation_token(data, ttl=3660):
    data = data or {}
    claims = {
        "iat": int(time.time()),
        "exp": int(time.time() + ttl),
    }
    claims.update(data)
    payload = orjson.dumps(claims)
    jwetoken = jwe.JWE(payload, json_encode({"alg": "A256KW", "enc": "A256CBC-HS512"}))
    jwetoken.add_recipient(get_jwk_key())
    token = jwetoken.serialize(compact=True)

    last_time = time.time() + ttl
    last_date = datetime.fromtimestamp(last_time).isoformat()
    return token, last_date


async def extract_validation_token(jwt_token):
    try:
        jwetoken = jwe.JWE()
        jwetoken.deserialize(jwt_token)
        jwetoken.decrypt(get_jwk_key())
        payload = jwetoken.payload
    except jwe.InvalidJWEOperation:
        logger.warn(f"Invalid operation", exc_info=True)
        return
    except jwe.InvalidJWEData:
        logger.warn(f"Error decrypting JWT token", exc_info=True)
        return
    json_payload = orjson.loads(payload)
    if json_payload["exp"] <= int(time.time()):
        logger.warning(f"Expired token {jwt_token}", exc_info=True)
        return
    return json_payload
