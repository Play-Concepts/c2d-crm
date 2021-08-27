import json
import os
from typing import Any, Dict, List

import boto3

from app.core.global_config import config as app_config

session = boto3.Session()
ses = session.client("ses")

is_test = os.environ.get("TEST")


def send_bulk_templated_email(
    destinations: List[Any],
    template: str,
    template_defaults: str,
    source: str = app_config.MAILER_FROM,
):
    return (
        None
        if is_test
        else ses.send_bulk_templated_email(
            Source=source,
            Template=template,
            DefaultTemplateData=template_defaults,
            Destinations=destinations,
        )
    )


def send_templated_email(
    to: str,
    template: str,
    template_data: Dict[str, Any],
    source: str = app_config.MAILER_FROM,
):
    return (
        None
        if is_test
        else ses.send_templated_email(
            Source=source,
            Template=template,
            TemplateData=json.dumps(template_data),
            Destination={
                "ToAddresses": [
                    to,
                ],
            },
        )
    )


def send_notification_email_to_marketing(
    merchant_email: str,
    to: str,
    source: str = app_config.MAILER_FROM,
):
    charset = "UTF-8"
    html_body = """<html>
                    <head></head>
                    <body>
                      <p>
                        New Merchant with email address {} is now active.
                      </p>
                    </body>
                    </html>
            """.format(
        merchant_email
    )
    text_body = "New Merchant with email address {} is now active.".format(
        merchant_email
    )
    return (
        None
        if is_test
        else ses.send_templated_email(
            Source=source,
            Destination={
                "ToAddresses": [
                    to,
                ],
            },
            Message={
                "Body": {
                    "Html": {
                        "Charset": charset,
                        "Data": html_body,
                    },
                    "Text": {
                        "Charset": charset,
                        "Data": text_body,
                    },
                },
                "Subject": {
                    "Charset": charset,
                    "Data": "[Elyria Data Passport] New Merchant active",
                },
            },
        )
    )
