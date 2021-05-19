from flask import Flask, jsonify, request
import json
import logging
import os
import requests
import msal
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)


app = Flask(__name__)


@app.route('/')
def hello_world():
    print("testing env file")
    print(os.environ.get("TECHNICAL_USER")) #works
    return 'Hello World!'


@app.route('/meetingRoom', methods=["GET"])
def get_meeting_room():
    with open('parameters_client_secret.json') as p:
        params = json.load(p)

    result = get_token_for_graph_api(params)

    if "access_token" in result:
        meeting_name = request.args.get('subject')
        if meeting_name is None:
            return jsonify({"error": "No subject found in request"}), 400
        # Calling graph endpoint using the access token
        body = {"subject": meeting_name}
        graph_data = requests.post(  # Use token to call downstream service
            params["endpoint"],
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

    return jsonify(joinURL=graph_data['joinUrl']), 201


def get_token_for_graph_api(config):
    # Client credential based auth for testing
    app_instance = msal.ConfidentialClientApplication(
        config["client_id"], authority=config["authority"],
        client_credential=config["secret"],
    )

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

    result = None

    # Look up a token from cache for current app and not end user (that's why account=None)
    result = app_instance.acquire_token_silent(config["scope"], account=None)
    if not result:
        logging.info(
            "No suitable token exists in cache. Let's get a new one from AAD.")
        result = app_instance.acquire_token_for_client(scopes=config["scope"])

    return result

class User():
    user = os.environ.get("TECHNICAL_USER")

    def generate_auth_token(self, expiration=600):
        s = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': self.user})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None    # valid token, but expired
        except BadSignature:
            return None    # invalid token
        user = User.query.get(data['id'])
        return user


# @auth.verify_password
# def verify_password(username_or_token, password):
#     # first try to authenticate by token
#     user = User.verify_auth_token(username_or_token)
#     if not user:
#         # try to authenticate with username/password
#         user = User.query.filter_by(username=username_or_token).first()
#         if not user or not user.verify_password(password):
#             return False
#     g.user = user
#     return True



if __name__ == '__main__':
    app.run()
