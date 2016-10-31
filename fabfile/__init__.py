#!/usr/bin/env python

import string
from functools import wraps

from config import load_config

import yaml
from fabric.api import task, run, prefix, hide, local
from fabric_gce_tools import update_roles_gce

config = load_config()


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
def launch_instance():
    """ Launch flowercluster instance. """

    args = [
        'gcloud compute instances create flowercluster',
        '--metadata-from-file user-data=config/ignition.json',
        '--tags flowercluster',
        "--disk name={0},device-name={0}".format(config['disk']),
        "--machine-type {}".format(config['machine-type']),
        "--network {}".format(config['network']),
        "--image {}".format(config['image']),
    ]

    local(string.join(args))


@task
def delete_instance():

    """ Delete flowercluster instance. """

    return local('gcloud compute instances delete flowercluster')


@task
def recreate_instance():

    """ Delete and recreate flowercluster instance. """

    if delete_instance().succeeded:
        launch_instance()


@task
def vault_policies():
    """ Update vault policies. """

    policies = yaml.load(open('policy.yml'))

    for name, policy in policies.iteritems():
        pass


update_roles_gce(use_cache=False)
