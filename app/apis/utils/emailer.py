from typing import List, Any

import boto3


def send_bulk_templated_email(destinations: List[Any],
                              template: str, template_defaults: str,
                              source: str = 'systems.@dataswift.dev'):
    ses = boto3.client("ses")
    return ses.send_bulk_templated_email(
        Source='systems@dataswift.dev',
        Template="test-welcome",
        DefaultTemplateData='{ "name": "", "link": "https://google.com?search="}',
        Destinations=[
            {
                'Destination': {
                    'ToAddresses': [
                        'terry.lee@dataswift.io',
                    ]
                },
                'ReplacementTemplateData': '{ "name": "Terry", "link": "https://google.com?search=Terry"}'
            },
            {
                'Destination': {
                    'ToAddresses': [
                        'terry.lee.m@gmail.com',
                    ]
                },
                'ReplacementTemplateData': '{ "name": "Terry", "link": "https://google.com?search=Terry"}'
            }
        ]
    )
