from fastapi import Depends, HTTPException, APIRouter, status
from typing import Dict, Any
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from .auth import Token
import requests
import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidSignatureError
import json
import base64
import binascii
from app.core.config import config as app_config

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/pda_token")
router = APIRouter()


def http_exception(detail: str):
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=detail,
        headers={"WWW-Authenticate": "Bearer"}
    )


invalid_application = http_exception("Credentials are not for this application")
credentials_exception = http_exception("Credentials could not be validated.")
expired_signature_exception = http_exception("Credentials have expired.")
invalid_signature_exception = http_exception("Credentials are invalid.")


async def get_current_pda_user(token: str = Depends(oauth2_scheme)):
    try:
        return validate(token)
    except (IndexError, binascii.Error):
        raise credentials_exception


def validate(token: str) -> [Dict[str, Any], str]:
    pda_url = _get_pda_url(token)
    pda_public_key = _get_pda_public_key(pda_url)
    try:
        decoded = jwt.decode(token, pda_public_key,
                             options={"verify_signature": True, "verify_exp": True},
                             algorithms=["RS256"])
    except ExpiredSignatureError:
        raise expired_signature_exception
    except InvalidSignatureError:
        raise invalid_signature_exception

    if decoded['application'] != app_config.APPLICATION_ID:
        raise invalid_application
    return decoded, token


def _get_pda_url(token: str) -> str:
    encoded_payload = token.split(".")[1]
    payload_str = base64.b64decode(encoded_payload + '===').decode("utf-8")
    payload = json.loads(payload_str)
    return payload['iss']


def _get_pda_public_key(pda_url: str) -> str:
    return requests.get(f"https://{pda_url}/publickey").text


@router.post("/pda_token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    return Token(access_token=form_data.username, token_type="bearer")
