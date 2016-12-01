#!/usr/bin/env python


from os.path import join

import yaml

from vault import Policy, AppRole
from docker import Container, Image

config = yaml.load(open('/var/local/flowercluster/config.yml', 'r'))

checkout = config['git-checkout']
default_args = config['vault']['approle_defaults']
vault_url = config['vault']['url']


def load_policies():
    """ Load policies from configuration into Policy objects. """

    policies = {}

    for policy in config['vault']['policies']:
        name = policy['name']
        path = join(checkout, policy['path'])

        policies[name] = Policy(name, path)

    return policies


def load_approles():
    """ Load AppRoles from configuration into AppRole objects. """

    approles = {}

    for role in config['vault']['approles']:
        name = role['name']
        wrap_ttl = config['vault']['secret_id_wrap_ttl']

        args = default_args.copy()
        args.update(role['args'])

        approles[name] = AppRole(name, wrap_ttl, args)

    return approles


def lookup_approle(approles, name):
    """ Look up an AppRole in a dictionary of them. If it doesn't exist,
    raise StandardError.
    """

    if name not in approles:
        msg = "AppRole '{0}' does not exist!".format(name)
        raise StandardError(msg)
    else:
        return approles[name]


def load_images(approles, token=None):
    """ Loads images from configuration into Image objects.

    This must be run after collecting AppRoles, as we fetch (dynamic) RoleIDs!
    """

    images = []

    for image in config['images']:
        image_name = image['image']
        path = join(checkout, image['path'])

        # fetch RoleID if AppRole specified
        role_id = None
        if 'role_id' in image:
            approle = lookup_approle(approles, image['role_id'])
            role_id = approle.role_id(token, vault_url)

        images.append(Image(image_name, path, role_id=role_id))

    return images


def load_containers(approles, token=None):
    """ Loads containers from configuration into Container objects.

    This must be run after collecting AppRoles, as we fetch (dynamic) SecretIDs!
    """

    containers = []

    for container in config['containers']:
        name = container['name']
        image = container['image']

        wrap_token = None
        if 'secret_id' in container:
            approle = lookup_approle(approles, container['secret_id'])
            wrap_token = approle.wrapped_secret_id(token, vault_url)

        params = {
            'network': container.get('network'),
            'volumes': container.get('volumes'),
            'ports': container.get('ports'),
            'token': wrap_token,
        }

        containers.append(Container(name, image, **params))

    return containers
