#!/usr/bin/env python

import logging

from config import load_policies, load_approles, load_images, load_containers, vault_url
from vault import validate_token

policies = load_policies()
approles = load_approles()

log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(format=log_format)


def write_policies(token):
    """ Write all loaded policies. """

    for name, policy in policies.iteritems():
        policy.write(token, vault_url)


def write_approles(token):
    """ Create all AppRoles. """

    for name, approle in approles.iteritems():
        approle.write(token, vault_url)


def build_images(token=None):
    """ Build all images. """

    if token is not None:
        validate_token(token, vault_url)

    images = load_images(approles, token=token)
    for image in images:
        image.build()


def start_containers(token=None):
    """ Start all containers. """

    if token is not None:
        validate_token(token, vault_url)

    containers = load_containers(approles, token=token)
    for container in containers:
        container.start()
