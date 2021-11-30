import json
import os
import requests

from typing import Any, Dict, List, Union
from app.core.global_config import config as app_config

is_test = os.environ.get("TEST")

class Notify():
    def __init__(self):
        self.headers = {'Authorization': 'Token ' + app_config.NOTIFY_TOKEN}
        self.prefix = app_config.NOTIFY_API


    def send_email(
      self,
      to: Union[str, List],
      template: str,
      variables: Dict[str, Any]
    ): 
      if(is_test):
        return 

      # if(isinstance(to, Dict)):
      # to = ', '.join(str(v) for v in to.values())

      data = json.dumps({ "to": to, "variables": variables })
      print(data)

      response = requests.post(self.prefix + "/v1/mail/datapassport/{}".format(template), json=data , headers=self.headers)
      print(response.content)

    def send_sms(
        self,
        to: Union[str, Dict, Any],
        template: str,
        variables: Dict[str, Any] = {}
      ): 
      return 
