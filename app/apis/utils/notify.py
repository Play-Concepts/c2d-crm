import json
import os
import requests

from typing import Any, Dict, List
from app.core.global_config import config as app_config

is_test = os.environ.get("TEST")


class Notify():
    def __init__(self):
        self.headers = {
            'Authorization': 'Token ' + app_config.NOTIFY_TOKEN,
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
        self.prefix = app_config.NOTIFY_API

    def send_email(
        self,
        to: List,
        template: str,
        variables: Dict[str, Any]
    ):
        if(is_test):
            return
        data = {"to": to, "variables": variables}
        requests.post(self.prefix + "/v1/mail/datapassport/{}".format(template), json.dumps(data) , headers=self.headers)

    def send_sms(
        self,
        to: List,
        template: str,
        variables: Dict[str, Any] = {}
    ):
        if(is_test):
            return
        return
