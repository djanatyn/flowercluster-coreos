#!/usr/bin/env python

import logging

import requests

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def validate_token(token, vault):
    """ Look up a token, anticipating a 200 response code.

    If the token is invalid, raise StandardError with debug info.
    If the token is valid, return information about it.
    """

    logger.info('validating token')

    url = vault + '/auth/token/lookup-self'
    params = {
        'headers': {'X-Vault-Token': token}
    }

    response = requests.get(url, **params)
    if response.status_code != 200:
        raise StandardError('token validation failed: ' + response.text)
    else:
        return response.text


class Policy(object):
    """ A Vault policy; takes a path and loads the rules document. """

    def __init__(self, name, path):
        self.name = name

        with open(path, 'r') as f:
            self.rules = f.read()

    def write(self, token, vault):
        """ Write the policy to a Vault instance. """

        logger.info("updating policy '{}'".format(self.name))

        url = vault + '/sys/policy/' + self.name
        params = {
            'json': {'rules': self.rules},
            'headers': {'X-Vault-Token': token},
        }

        response = requests.post(url, **params)

        if response.status_code != 204:
            logger.critical('Policy update failed: ' + response.text)

        return response


class AppRole(object):
    """ A Vault AppRole, with a dictionary of init arguments. """

    def __init__(self, name, secret_id_wrap_ttl, args):
        self.name = name
        self.wrap_ttl = secret_id_wrap_ttl
        self.args = args

    def write(self, token, vault):
        """ Write the AppRole to a Vault instance. """

        logger.info("updating AppRole '{}'".format(self.name))

        data = self.args.copy()
        data.update({'role_name': self.name})

        url = vault + '/auth/approle/role/' + self.name
        params = {
            'json': data,
            'headers': {'X-Vault-Token': token},
        }

        response = requests.post(url, **params)
        if response.status_code != 204:
            logger.critical('AppRole update failed: ' + response.text)

        return response

    def role_id(self, token, vault):
        """ Return the RoleID for an AppRole. """

        logger.info("fetching RoleID for '{}'".format(self.name))

        url = vault + '/auth/approle/role/' + self.name + '/role-id'
        params = {
            'headers': {'X-Vault-Token': token},
        }

        response = requests.get(url, **params)
        if response.status_code == 200:
            return response.json()['data']['role_id']
        else:
            logger.critical('failed to fetch RoleID: ' + response.text)
            return None

    def wrapped_secret_id(self, token, vault):
        """ Returns a Response-Wrapped SecretID token, or None if unsuccessful. """

        logger.info("fetching SecretID for '{}'".format(self.name))

        url = vault + '/auth/approle/role/' + self.name + '/secret-id'
        params = {
            'headers': {
                'X-Vault-Wrap-TTL': self.wrap_ttl,
                'X-Vault-Token': token,
            }
        }

        response = requests.post(url, **params)
        if response.status_code == 200:
            return response.json()['wrap_info']['token']
        else:
            logger.critical('failed to fetch SecretID Wrap Token: ' + response.text)
            return None
