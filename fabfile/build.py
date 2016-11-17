#!/usr/bin/env python

from load_config import configuration
from fabric.api import task, run, cd, roles

build_config = configuration['build']


@roles('flowercluster')
@task
def containers():
    """ Build all containers specified in config.yml """

    for container in build_config:
        with cd(container['path']):
            run("docker build . -t {0}".format(container['name']))
