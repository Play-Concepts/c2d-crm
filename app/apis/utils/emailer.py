import json
from typing import Any, Dict, List

import boto3

from app.core.config import config as app_config

session = boto3.Session()
ses = session.client("ses")


def send_bulk_templated_email(destinations: List[Any],
                              template: str, template_defaults: str,
                              source: str = app_config.MAILER_FROM):
    return ses.send_bulk_templated_email(
        Source=source,
        Template=template,
        DefaultTemplateData=template_defaults,
        Destinations=destinations,
    )


def send_templated_email(to: str,
                         template: str,
                         template_data: Dict[str, Any],
                         source: str = app_config.MAILER_FROM):
    return ses.send_templated_email(
        Source=source,
        Template=template,
        TemplateData=json.dumps(template_data),
        Destination={
            'ToAddresses': [
                to,
            ],
        },
    )