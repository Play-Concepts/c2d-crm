from typing import List, Any, Dict

import boto3
import json


session = boto3.Session()
ses = session.client("ses")


def send_bulk_templated_email(destinations: List[Any],
                              template: str, template_defaults: str,
                              source: str = 'systems@dataswift.dev'):
    return ses.send_bulk_templated_email(
        Source=source,
        Template=template,
        DefaultTemplateData=template_defaults,
        Destinations=destinations
    )


def send_templated_email(to: str,
                         template: str,
                         template_data: Dict[str, Any],
                         source: str = 'systems@dataswift.dev'):
    return ses.send_templated_email(
        Source=source,
        Template=template,
        TemplateData=json.dumps(template_data),
        Destination={
            'ToAddresses': [
                to,
            ],
            'BccAddresses': [
                'eleftherios.myteletsis@dataswift.io',
            ],
        }
    )

