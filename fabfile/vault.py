#!/usr/bin/env python

import yaml
from functools import wraps

from load_config import configuration
from fabric.api import task, prefix, hide, run, roles


vault_config = configuration['vault']


def auth_vault():
    """ Authorize with vault API client. """

    with hide('running', 'stdout', 'stderr'):
        run('vault auth ' + configuration['token'])


def vault_task(f):
    """ Decorator for exporting VAULT environmental variables. """

    @wraps(f)
    def wrapper(*args, **kwargs):
        addr_prefix = prefix('export VAULT_ADDR=' + vault_config['VAULT_ADDR'])

        with addr_prefix:
            return f(*args, **kwargs)

    return task(wrapper)


@roles('flowercluster')
@vault_task
def unseal_vault():
    """ Unseal the vault using keys specified by the user at deploy time. """

    for key in configuration['unseal_keys']:
        with hide('running', 'stdout', 'stderr'):
            run('vault unseal ' + key)


@roles('flowercluster')
@vault_task
def init_policies():
    """ Update vault policies. """

    policies = yaml.load(open('policies.yml'))

    auth_vault()
    for policy, path in policies.iteritems():
        run("vault policy-write {0} {1}".format(policy, path))
