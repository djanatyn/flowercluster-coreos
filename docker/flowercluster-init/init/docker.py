#!/usr/bin/env python

import subprocess
import logging

from config import images, containers

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def start_container(configuration, secret_id=None):
    """ Start a container, passing in a SecretID wrap token if needed. """

    logger.log("starting container '{0}' ({1})".format(configuration['name'], configuration['image']))
    args = [
        '/usr/bin/docker',
        'run', configuration['image'],
        '--name', configuration['name'],
    ]

    if secret_id is not None:
        args.append(secret_id)

    return subprocess.call(args)


def build_container(configuration, role_id=None):
    """ Build a container. Returns exit code. """

    logger.log("building image '{}'".format(configuration['image']))
    args = ['/usr/bin/docker', 'build', configuration['path'], '-t', configuration['image']]

    if role_id is not None:
        args.append('--build-arg ROLE_ID=' + role_id)

    return subprocess.call(args)


def initialize(vault_instance):
    """ Build and start all containers. """

    for image in images:
        role_id = None
        if 'approle' in image:
            role_id = vault_instance.role_id(image['approle'])

        build_container(image, role_id=role_id)

    for container in containers:
        secret_id = None
        if 'approle' in container:
            secret_id = vault_instance.secret_id(container['approle'])

        start_container(container, secret_id=secret_id)
