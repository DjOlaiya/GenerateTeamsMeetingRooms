from flask import Flask
import json
import logging

import requests
import msal

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/meetingRoom')
def get_meeting_room():

    with open('parameters_client_secret.json') as params:
        config = json.load(params)

    # Certificate based auth for production
    # Create a preferably long-lived app instance which maintains a token cache.
    # app_instance = msal.ConfidentialClientApplication(
    #     config["client_id"], authority=config["authority"],
    #     client_credential={"thumbprint": config["thumbprint"], "private_key": open(
    #         config['private_key_file']).read()},
    #     # token_cache=...  # Default cache is in memory only.
    #     # You can learn how to use SerializableTokenCache from
    #     # https://msal-python.rtfd.io/en/latest/#msal.SerializableTokenCache
    # )

    # Client credential based auth for testing
    app_instance = msal.ConfidentialClientApplication(
        config["client_id"], authority=config["authority"],
        client_credential=config["secret"],
    )

    # The pattern to acquire a token looks like this.
    result = None

    # Firstly, looks up a token from cache
    # Since we are looking for token for the current app, NOT for an end user,
    # notice we give account parameter as None.
    result = app_instance.acquire_token_silent(config["scope"], account=None)
    if not result:
        logging.info(
            "No suitable token exists in cache. Let's get a new one from AAD.")
        result = app_instance.acquire_token_for_client(scopes=config["scope"])
    if "access_token" in result:
        # Calling graph endpoint using the access token
        body = {
            "subject": "TEST TEST"
        }
        graph_data = requests.post(  # Use token to call downstream service
            config["endpoint"],
            headers={'Authorization': 'Bearer ' + result['access_token'],
                     'Content-type': 'application/json',
                     },
            json=body
        ).json()
        print("Graph API call result: ")
        print(json.dumps(graph_data, indent=2))
    else:
        print(result.get("error"))
        print(result.get("error_description"))
        # You may need this when reporting a MS bug
        print(result.get("correlation_id"))

    return graph_data['joinUrl']


if __name__ == '__main__':
    app.run()
