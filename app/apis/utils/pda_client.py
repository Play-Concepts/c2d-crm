import json
from functools import reduce
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
    return [response.status_code, response.json()]


def read_pda_data(pda_url: str, token: str, namespace: str, data_path: str) -> Any:
    headers = {"x-auth-token": token, "content-type": "application/json"}
    data_read_url = "https://{}/api/v2.6/data/{}/{}".format(
        pda_url, namespace, data_path
    )
    response = requests.get(data_read_url, headers=headers)
    return [response.status_code, response.json()]


# Function to translate .dot notation string to dict
# for ease of writing to PDA
def dot_to_dict(a):
    output = {}
    for key, value in a.items():
        pre_path, *data_type = key.split("/")
        path = pre_path.split(".")
        val = value
        if len(data_type) == 1:
            if data_type[0] == "int":
                val = int(value)
            if data_type[0] == "float":
                val = float(value)
        target = reduce(lambda d, k: d.setdefault(k, {}), path[:-1], output)
        target[path[-1]] = val

    return output


def delete_pda_record(
    pda_url: str,
    token: str,
    recordId: str,
) -> Any:
    headers = {"x-auth-token": token, "content-type": "application/json"}
    data_write_url = "https://{}/api/v2.6/data?records={}".format(pda_url, recordId)
    response = requests.delete(data_write_url, headers=headers)
    return response.status_code
