#general functions used several times

import inspect
#import required packages
import json
import logging
import os
import io
from io import open
import pandas as pd
import requests
import numpy as np

logger = logging.getLogger(__name__)

#get path of this file
dataops_path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))


def test_function():
    print('hello dataops people!')
###################################################################################################################
########################################## Intercom ###############################################################
###################################################################################################################

def message_tool_register(email,sender_account='api.dataops'):
    with open(dataops_path + '/credentials/credentials.json', encoding="utf-8") as f:
        cred = json.load(f)
    token=cred['message_tool'][sender_account]['token']

    url='https://messages.prod.stuart-apps.solutions/api/users/register/api'
    headers = {'Authorization': 'Bearer ' + token, 'Accept': 'application/json', 'Content-Type': 'application/json'}
    data={"email": email,
          "password": (''.join(e for e in email.split('@')[0] if e.isalnum())).title()+str(1)+'*'}
    response = requests.post(url, data=json.dumps(data), headers=headers)
    if json.loads(response.content)['ok']==True:
        token=json.loads(response.content)['message']['token']['message']['token']
        return {email.split('@')[0]: {
                "email": email,
                "password": (''.join(e for e in email.split('@')[0] if e.isalnum())).title()+str(1)+'*',
                "token": token
                }
            }
    else:
        return response.text
