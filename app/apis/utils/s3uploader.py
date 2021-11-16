import os

import boto3

from app.core.global_config import config as app_config

session = boto3.Session()
s3 = session.resource("s3")

is_test = os.environ.get("TEST")


def put_file_for_preview(file, filename: str) -> int:
    result = s3.meta.client.put_object(
        Body=file, Key=filename, Bucket=app_config.BUCKET_PRIVATE
    )
    res = result.get("ResponseMetadata")
    return res.get("HTTPStatusCode")
