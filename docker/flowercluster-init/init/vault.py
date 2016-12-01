#!/usr/bin/env python

import logging
from os.path import join

import requests

from config import site_config, vault

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

checkout = site_config['git-checkout']


class Vault(object):
    """ Vault class, scoped to interactions with a single Vault token. """

    api_url = vault['url']

    def __init__(self, token):
        self.header = {'X-Vault-Token': token}

        validity = self.validate_token(token)
        if validity.status_code != 200:
            raise StandardError('token validation failed: ' + validity.text)

    def url(self, api_endpoint):
        return self.api_url + api_endpoint

    def validate_token(self, token):
        """ Look up the token information, anticipating a 200 response code. """

        logger.info('validating token')

        url = self.url('/auth/token/lookup-self')
        return requests.get(url, headers=self.header)

    def update_policy(self, policy, path):
        """ Update a policy in Vault. Uses relative paths from the git checkout. """

        logger.info("updating policy '{}'".format(policy))

        url = self.url('/sys/policy/' + policy)
        with open(join(checkout, path), 'r') as f:
            data = {'rules': f.read()}

        return requests.post(url, json=data, headers=self.header)

    def update_approle(self, role, config):
        """ Create or update an existing AppRole. Uses default arguments. """

        logger.info("updating AppRole '{}'".format(role))

        defaults = vault['approles']['defaults']

        url = self.url('/auth/approle/role/' + role)
        data = {
            'role_name': role,
            'policies': role,
        }

        data.update(defaults)
        data.update(config)

        return requests.post(url, json=data, headers=self.header)

    def update_approles(self):
        """ Update all Vault AppRoles in configuration. """

        for role, role_config in vault['approles'].iteritems():
            if role == 'defaults':
                continue

            # create associated policy
            self.update_policy(role, role_config['path'])

            # create AppRole
            self.update_approle(role, role_config['config'])

    def update_policies(self):
        """ Update all Vault policies in configuration. """

        for policy, path in vault['policies'].iteritems():
            self.update_policy(policy, path)
