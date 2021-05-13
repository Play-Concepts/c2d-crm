import csv
import codecs
from functools import reduce
from typing import List, Dict, Any

from fastapi import UploadFile
from .pda_client import validate, write_data


def do_file_upload(customers_file: UploadFile,
                   token: str,
                   namespace: str,
                   data_path: str) -> Any:
    payload = _construct_payload(customers_file)
    pda_url = validate(token)['iss']
    response = write_data(pda_url, token, namespace, data_path, payload)

    return response


def _construct_payload(customers_file: UploadFile) -> List[Dict[str, Any]]:
    data = []
    lines = csv.reader(codecs.iterdecode(customers_file.file, 'utf-8'), delimiter=',')
    header = next(lines)
    for log_line in lines:
        data.append(_dot_to_dict(dict(zip(header, log_line))))

    return data


def _dot_to_dict(a):
    output = {}
    for key, value in a.items():
        pre_path, *data_type = key.split('/')
        path = pre_path.split('.')
        val = value
        if len(data_type) == 1:
            if data_type[0] == 'int':
                val = int(value)
            if data_type[0] == 'float':
                val = float(value)
        target = reduce(lambda d, k: d.setdefault(k, {}), path[:-1], output)
        target[path[-1]] = val

    return output
