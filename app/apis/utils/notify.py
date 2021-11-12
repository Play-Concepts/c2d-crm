import json
import os
from typing import Any, Dict, List
from requests import Session
from app.core.global_config import config as app_config

is_test = os.environ.get("TEST")

class Notify(Session):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.headers.update({'Authorization': app_config.NOTIFY_TOKEN})
        self.prefix_url = app_config.NOTIFY_API

    def send_email(
      self,
      to: str,
      template: str,
      variables: Dict[str, Any]
    ): 
      if(is_test):
        return 
      if(isinstance(to, Dict)):
          to = ', '.join(str(v) for v in to.values())
      self.post("/v1/mail/datapassport/{}".format(template), { to, variables })

    def send_sms(
        self,
        to: str,
        template: str,
        variables: Dict[str, Any]
      ): 
      return 

# def send_notification_email_to_marketing(
#     merchant_email: str,
#     to: str,
#     source: str = app_config.MAILER_FROM,
# ):
#     charset = "UTF-8"
#     html_body = """<html>
#                     <head></head>
#                     <body>
#                       <p>
#                         New Merchant with email address {} is now active.
#                       </p>
#                     </body>
#                     </html>
#             """.format(
#         merchant_email
#     )
#     text_body = "New Merchant with email address {} is now active.".format(
#         merchant_email
#     )
#     return (
#         None
#         if is_test
#         else ses.send_email(
#             Source=source,
#             Destination={
#                 "ToAddresses": [email.strip() for email in to.split(",")],
#             },
#             Message={
#                 "Body": {
#                     "Html": {
#                         "Charset": charset,
#                         "Data": html_body,
#                     },
#                     "Text": {
#                         "Charset": charset,
#                         "Data": text_body,
#                     },
#                 },
#                 "Subject": {
#                     "Charset": charset,
#                     "Data": "[{}] New Merchant active".format(
#                         app_config.APPLICATION_NAME
#                     ),
#                 },
#             },
#         )
#     )


# def send_email_to_marketing(
#     email_content: str,
#     email_subject: str,
#     to: str = app_config.NOTIFY_MARKETING_EMAIL,
#     source: str = app_config.MAILER_FROM,
# ):
#     charset = "UTF-8"
#     return (
#         None
#         if is_test
#         else ses.send_email(
#             Source=source,
#             Destination={
#                 "ToAddresses": [email.strip() for email in to.split(",")],
#             },
#             Message={
#                 "Body": {
#                     "Html": {
#                         "Charset": charset,
#                         "Data": email_content,
#                     },
#                 },
#                 "Subject": {
#                     "Charset": charset,
#                     "Data": "[{}] {}".format(
#                         app_config.APPLICATION_NAME, email_subject
#                     ),
#                 },
#             },
#         )
#     )
