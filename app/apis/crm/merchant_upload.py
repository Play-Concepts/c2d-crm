import csv
import codecs

from app.models.core import CreatedCount

from fastapi import UploadFile


def do_merchant_file_upload(merchants_file: UploadFile) -> CreatedCount:
    created_merchants: int = 0
    lines = csv.reader(codecs.iterdecode(merchants_file.file, 'utf-8'), delimiter=',')
    header = next(lines)
    for line in lines:
        created_merchants += 1

    return CreatedCount(count=created_merchants)
