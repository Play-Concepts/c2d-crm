import json
from typing import Any

import requests
from pydantic.types import Json


def write_pda_data(
    pda_url: str, token: str, namespace: str, data_path: str, payload: Json
) -> Any:
    headers = {"x-auth-token": token, "content-type": "application/json"}
    data_write_url = "https://{}/api/v2.6/data/{}/{}".format(
        pda_url, namespace, data_path
    )
    response = requests.post(data_write_url, json.dumps(payload), headers=headers)
    return response.json()
