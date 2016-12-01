#!/usr/bin/env python

import subprocess
from config import images, containers


def start_container(configuration, secret_id=None):
    """ Start a container, passing in a SecretID wrap token if needed. """

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
