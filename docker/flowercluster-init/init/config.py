#!/usr/bin/env python

import yaml

site_config = yaml.load(open('/var/local/flowercluster/config.yml', 'r'))

# convenience definitions
vault = site_config['vault']

images = site_config['images']
containers = site_config['containers']

checkout = site_config['git-checkout']
