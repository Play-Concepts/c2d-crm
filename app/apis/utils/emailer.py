from typing import List, Any

import boto3


def send_bulk_templated_email(destinations: List[Any],
                              template: str, template_defaults: str,
                              source: str = 'systems@dataswift.dev'):
    ses = boto3.client("ses")
    return ses.send_bulk_templated_email(
        Source=source,
        Template=template,
        DefaultTemplateData=template_defaults,
        Destinations=destinations
    )
