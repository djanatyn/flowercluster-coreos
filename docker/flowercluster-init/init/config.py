#!/usr/bin/env python

import yaml

site_config = yaml.load(open('/var/local/flowercluster/config.yml', 'r'))

vault = site_config['vault']
