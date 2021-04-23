import csv
import codecs
from functools import reduce
from typing import List, Dict, Any

from fastapi import UploadFile, File


def dot_to_json(a):
    output = {}
    for key, value in a.items():
        path = key.split('.')
        target = reduce(lambda d, k: d.setdefault(k, {}), path[:-1], output)
        target[path[-1]] = value
    return output


def do_file_upload(customers_file: UploadFile) -> List[Dict[str, Any]]:
    data = []
    lines = csv.reader(codecs.iterdecode(customers_file.file, 'utf-8'), delimiter=',')
    header = next(lines)
    for log_line in lines:
        data.append(dot_to_json(dict(zip(header, log_line))))

    return data
