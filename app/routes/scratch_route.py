from fastapi import APIRouter
import boto3

router = APIRouter()
router.prefix = "/api/scratch"


@router.get("/email", tags=["scratch"])
async def test_email():
    return do_test_email()


def do_test_email():
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
