#!/usr/bin/env python

import string
import os
from functools import wraps

import yaml
from load_config import configuration
from fabric.api import task, prefix, hide, run, roles
from fabric.colors import green

vault_config = configuration['vault']
token_file = os.path.join('out', 'build-token')


@roles('flowercluster')
def vault_task(f):
    """ Decorator for exporting VAULT environmental variables. """

    @wraps(f)
    def wrapper(*args, **kwargs):
        addr_prefix = prefix('export VAULT_ADDR=' + vault_config['VAULT_ADDR'])

        with addr_prefix:
            return f(*args, **kwargs)

    return task(wrapper)


def auth_vault(token=None):
    """ Authorize with vault API client. """

    if token is None:
        token = configuration['token']

    with hide('running', 'stdout', 'stderr'):
        run('vault auth ' + token)


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

        for arg, value in role_config.iteritems():
            if arg == 'path':
                continue

            approle_args.append("{0}={1}".format(arg, value))

        # append keys and values for each AppRole init argument
        for arg in defaults.keys():
            if arg not in role_config:
                approle_args.append("{0}={1}".format(arg, defaults[arg]))

        run(string.join(approle_args))


def save_token(token):
    """ Write the build token to disk. """

    if not os.path.isdir('out'):
        print("Creating ./out/ directory.")
        os.mkdir('out')

    with open(os.path.join('out', 'build-token'), 'w') as f:
        f.write(token)


@roles('flowercluster')
@vault_task
def build_token():
    """ Generate and return a build token. """

    # check for saved token file at first
    if os.path.exists(token_file):
        print(green('found saved build token!'))
        return open(token_file).read()

    # otherwise, generate a new token
    auth_vault()

    token_args = ['vault token-create -format=yaml -policy=build-token']

    for arg, value in vault_config['build-token'].iteritems():
        token_args.append("-{0}={1}".format(arg, value))

    with hide('running', 'stdout'):
        token = yaml.load(run(string.join(token_args)))['auth']['client_token']

    save_token(token)

    return token


@roles('flowercluster')
@vault_task
def role_id(approle, token=None):
    """ Get the RoleID for a given AppRole. """

    if approle not in vault_config['approles'].keys():
        raise StandardError("Invalid AppRole!")

    if token is None:
        token = build_token()

    auth_vault(token)

    role = "auth/approle/role/{}".format(approle)
    role_cmd = "vault read -format=yaml {0}".format(role + '/role-id')

    with hide('stdout'):
        role_id = yaml.load(run(role_cmd))['data']['role_id']

    print(green('RoleID: ' + role_id))
    return role_id


@roles('flowercluster')
@vault_task
def secret_id(approle, token=None):
    """ Return a SecretID wrapped-token. """

    if approle not in vault_config['approles'].keys():
        raise StandardError("Invalid AppRole!")

    if token is None:
        token = build_token()

    auth_vault(token)

    role = "auth/approle/role/{}".format(approle)
    secret_cmd = [
        'vault write',
        '-wrap-ttl=5m',
        '-format=yaml',
        '-f',
        role + '/secret-id',
    ]

    with hide('stdout'):
        token = yaml.load(run(string.join(secret_cmd)))['wrap_info']['token']

    print(green('SecretID Wrap Token: ' + token))
    return token
