#!/usr/bin/env python

import string

from load_config import configuration
from fabric.api import task, run, cd, roles

import vault

build_config = configuration['build']


@roles('flowercluster')
@task
def containers():
    """ Build all containers specified in config.yml """

    for container in build_config:
        args = [
            'docker build . -t {}'.format(container['name']),
        ]

        if 'approle' in container:
            # append vault credentials
            creds = vault.approle_creds(container['approle'])

            for key, value in creds.iteritems():
                args.append("--build-arg {0}={1}".format(key, value))

        with cd(container['path']):
            run(string.join(args))

__all__ = ['containers']
