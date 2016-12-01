#!/usr/bin/env python

import subprocess
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class Image(object):
    """ A Docker image to be built. """

    def __init__(self, name, path, role_id=None):
        self.name = name
        self.role_id = role_id
        self.path = path

    def build(self):
        """ Attempt to build the image. """

        logger.info("building image '{}'".format(self.name))

        args = ['/usr/bin/docker', 'build', self.path, '-t', self.name]

        if self.role_id is not None:
            args += ['--build-arg', 'ROLE_ID=' + self.role_id]

        return subprocess.call(args)


class Container(object):
    """ A docker containers to be started. """

    def __init__(self, name, image, token=None, network=None, volumes=None, ports=None):
        self.name = name
        self.image = image
        self.token = token
        self.network = network
        self.volumes = volumes
        self.ports = ports

    def start(self):
        """ Start the container, passing in a SecretID wrap token if needed. """

        logger.info("starting container '{0}' ({1})".format(self.name, self.image))

        args = ['/usr/bin/docker', 'run', '-d', '--name', self.name]

        if self.network is not None:
            args += ['--network', self.network]

        if self.volumes is not None:
            for volume in self.volumes:
                args += ['-v', volume]

        if self.ports is not None:
            for port in self.ports:
                args += ['-p', port]

        # container image name needs to come after flags
        args.append(self.image)

        # and if there's a secret id, it's an argument for the entrypoint
        if self.token is not None:
            args.append(self.token)

        return subprocess.call(args)
