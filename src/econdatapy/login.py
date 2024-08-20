import os
import requests
from econdatapy import dialogue

def helper(env):
    if "ECONDATA_CREDENTIALS" in os.environ:
        credentials = os.environ["ECONDATA_CREDENTIALS"].split(";")
        if len(credentials) != 2:
            raise Exception("Error reading EconData credentials")
        response = requests.post(env.auth_url + "/"  + env.auth_path,
                                 data = {"grant_type": "client_credentials",
                                         "client_id": credentials[0],
                                         "client_secret": credentials[1]})
        if not response.ok:
            raise Exception(response.json())
        token = "Bearer " + response.json()["access_token"]
    else:
        token = "Bearer " + dialogue.econdata_credentials()
    return(token)
