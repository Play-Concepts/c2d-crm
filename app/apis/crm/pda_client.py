# Validates a token and return the pda url.
import base64
import json
from typing import List, Dict, Any

import requests


def validate(token: str) -> str:
    pda_url = _get_pda_url(token)
    # pda_public_key = _get_pda_public_key(pda_url)
    return pda_url


def write_data(pda_url: str, token: str, namespace: str, data_path: str, payload: List[Dict[str, Any]]) -> Any:
    headers = {
        'x-auth-token': token,
        'content-type': 'application/json'
    }
    data_write_url = "https://{}/api/v2.6/data/{}/{}".format(pda_url, namespace, data_path)
    response = requests.post(data_write_url, data=json.dumps(payload), headers=headers)
    return response.json()


def _get_pda_url(token: str) -> str:
    encoded_payload = token.split(".")[1]
    payload_str = base64.b64decode(encoded_payload + '===').decode("utf-8")
    payload = json.loads(payload_str)
    return payload['iss']


def _get_pda_public_key(pda_url: str) -> str:
    return requests.get(f"https://{pda_url}/publickey").text
