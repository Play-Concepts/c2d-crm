# Validates a token and return the pda url.
import json
from typing import List, Dict, Any

import requests


def write_data(pda_url: str, token: str, namespace: str, data_path: str, payload: List[Dict[str, Any]]) -> Any:
    headers = {
        'x-auth-token': token,
        'content-type': 'application/json'
    }
    data_write_url = "https://{}/api/v2.6/data/{}/{}".format(pda_url, namespace, data_path)
    response = requests.post(data_write_url, data=json.dumps(payload), headers=headers)
    return response.json()
