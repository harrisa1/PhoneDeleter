#!/usr/bin/env python

import base64
import getpass
import json
from rest import REST

__author__ = 'evanellis'

"""
An OAuth Client can be used to log in under any org in the entire environment.
If you wish to create a new one in order to either tie it to an org you own
or access a different environment, please utilize the 'create_client' function.
Please don't create a client for every org you own,
just a 'primary' one in each environment you require access to.

NOTE: Creating a new client in stage or prod is NOT recommended unless it is absolutely necessary.
Please talk to someone on the API team about it to verify you need access and discuss potential alternatives.
As a general rule of thumb, if you can't VPN into that environment you most likely don't need a client there.
"""


class OAuthClient(object):
    """Logs in a user with OAuth2 and creates new clients if needed"""
    def __init__(self, org_id, session, env):
        self.env = env
        self.org_id = org_id
        self.session = session

    # Creates http headers
    @staticmethod
    def make_headers(encoded_client=None):
        if encoded_client is not None:
            headers = {'Authorization': 'Basic ' + encoded_client, 'Content-Type': 'application/x-www-form-urlencoded'}
        else:
            headers = {'content-type': 'application/json'}
        return headers

    # Creates a new OAuth2 client if one is needed
    def new_client(self):
        url = 'http://auth-api.us-east-1.inin' + self.env + '.com/v1/clients'
        data = {'organizationId': self.org_id,
                'name': 'Test Client',
                'description': 'Test Client',
                'scoped': True,
                'authorizedGrantTypes': ['code', 'token', 'password'],
                'registeredRedirectUri': ['http://localhost:8085/oauth/callback'],
                'accessTokenValiditySeconds': 14400,
                'refreshTokenValiditySeconds': 7200,
                'autoApprove': True
                }
        headers = self.make_headers()
        result = self.session.post(url, data, headers, app_json=True)
        return result

    # Gets an existing OAuth client for the org
    def id_get(self):
        url = 'http://auth-api.us-east-1.inin' + self.env + '.com/v1/clients?organizationId=' + self.org_id
        result = self.session.get(url)
        client_id = json.loads(result.text)[0]['id']
        url2 = 'http://auth-api.us-east-1.inin' + self.env + '.com/v1/clients/' + client_id
        result2 = self.session.get(url2)
        secret = json.loads(result2.text)['secret']
        return client_id, secret

    # Logs in with an existing client
    def client_login(self, encoded_client, username, password):
        url = 'https://login.inin' + self.env + '.com/token'
        headers = self.make_headers(encoded_client)
        data = 'grant_type=password&username=' + username + '&password=' + password
        result = self.session.post(url, data, headers)
        return result


# Sets up credentials and logs in
def login(env, username=None, password=None, encoded_client=None, rest_session=None):
    # If no username and/or password are provided in the parameters, prompt for them here
    # (this is more secure, but less automation friendly)
    if username is not None:
        pass
    else:
        username = raw_input('Username:')

    if password is not None:
        pass
    else:
        password = getpass.getpass()

    if rest_session is None:
        rest_session = REST('oauth_session')

    org = 'null'
    auth = OAuthClient(org, rest_session, env)

    token_response = auth.client_login(encoded_client, username, password)
    token = token_response['access_token']

    return token


# Assists in the generation of a new Client
# Returns the ready to use base64 encoded version
# This operation requires a connection to the specified environment's VPN!
def create_client(env, username=None, password=None):
    rest_session = REST('main_session')
    admin_object = rest_session.get('http://configuration.us-east-1.inin' + env + '.com/configurations/v1/users?username=' + username)
    org_id = json.loads(admin_object.text)['content'][0]['organizationId']
    auth = OAuthClient(org_id, rest_session, env)
    auth.new_client()
    client_id, client_secret = auth.id_get()
    encoded_client = base64.b64encode(client_id + ':' + client_secret)

    return encoded_client