#!/usr/bin/env python

import yaml
from functools import wraps

from load_config import config
from fabric.api import task, prefix, hide, run


def vault_task(f):
    """ Decorator for exporting VAULT environmental variables. """

    @wraps(f)
    def wrapper(*args, **kwargs):
        addr_prefix = prefix('export VAULT_ADDR=' + config['VAULT_ADDR'])

        with addr_prefix:
            return f(*args, **kwargs)

    return task(wrapper)


@vault_task
def unseal_vault():
    """ Unseal the vault using keys specified by the user at deploy time. """

    for key in config['unseal_keys']:
        with hide('running', 'stdout', 'stderr'):
            run('vault unseal ' + key)


@vault_task
def auth_vault():
    """ Authorize with vault API client. """

    with hide('running', 'stdout', 'stderr'):
        run('vault auth ' + config['token'])


@task
def vault_policies():
    """ Update vault policies. """

    policies = yaml.load(open('policy.yml'))

    for name, policy in policies.iteritems():
        pass
