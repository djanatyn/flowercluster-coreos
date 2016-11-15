#!/usr/bin/env python

import string
from functools import wraps

import yaml
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
def unseal():
    """ Unseal the vault using keys specified by the user at deploy time. """

    for key in configuration['unseal_keys']:
        with hide('running', 'stdout', 'stderr'):
            run('vault unseal ' + key)


@roles('flowercluster')
@vault_task
def init_roles():
    """ Update vault AppRoles and policies. """

    auth_vault()

    # update policies
    for policy, path in vault_config['policies'].iteritems():
        run("vault policy-write {0} {1}".format(policy, path))

    # update roles and their policies
    defaults = vault_config['approles']['defaults']
    for role, role_config in vault_config['approles'].iteritems():
        # skip default role
        if role == 'defaults':
            continue

        # update policy
        run("vault policy-write {0} {1}".format(role, role_config['path']))

        # update AppRole
        approle_args = ["vault write auth/approle/role/{}".format(role)]

        # append keys and values for each AppRole init argument
        for arg in defaults.keys():
            if arg in role_config:
                value = role_config[arg]
            else:
                value = defaults[arg]

            approle_args.append("{0}={1}".format(arg, value))

        run(string.join(approle_args))


@roles('flowercluster')
@vault_task
def build_token():
    """ Generate and return a build token. """

    auth_vault()

    token_args = ['vault token-create -format=yaml -policy=build-token']

    for arg, value in vault_config['build-token'].iteritems():
        token_args.append("-{0}={1}".format(arg, value))

    token = yaml.load(run(string.join(token_args)))

    return token
