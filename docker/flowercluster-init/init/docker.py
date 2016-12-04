#!/usr/bin/env python

import subprocess
import logging
import os

from config import images, containers, checkout

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def start_container(configuration, secret_id=None, network=None):
    """ Start a container, passing in a SecretID wrap token if needed. """

    name = configuration['name']
    image = configuration['image']

    logger.info("starting container '{0}' ({1})".format(name, image))

    args = ['/usr/bin/docker', 'run', '-d', '--name', name]

    if network is not None:
        args += ['--network', network]

    # container image name needs to come after flags
    args.append(image)

    # and if there's a secret id, it's an argument for the entrypoint
    if secret_id is not None:
        args.append(secret_id)

    return subprocess.call(args)


def build_container(configuration, role_id=None):
    """ Build a container. Returns exit code. """

    logger.info("building image '{}'".format(configuration['image']))

    path = os.path.join(checkout, configuration['path'])
    args = ['/usr/bin/docker', 'build', path, '-t', configuration['image']]

    if role_id is not None:
        args += ['--build-arg', 'ROLE_ID=' + role_id]

    return subprocess.call(args)


def initialize(vault_instance):
    """ Build and start all containers. """

    for image in images:
        role_id = None
        if 'approle' in image:
            role_id = vault_instance.role_id(image['approle'])

        build_container(image, role_id=role_id)

    for container in containers:
        run_args = {
            'secret_id': None,
            'network': None,
        }

        for arg in run_args.keys():
            if arg in container:
                run_args[arg] = container[arg]

        start_container(container, **run_args)
