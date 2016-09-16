#!/usr/bin/env python

import sys

try:
    configuration = [
        {'name': 'stable',
         'filename': 'stable/ignition.json',
         'config': {
             'units': [
                 {'name': 'etcd2.service',
                  'enable': True},
                 {'name': 'var-lib-docker.mount',
                  'enable': True,
                  'contents': open('config/var-lib-docker.mount').read()},
                 {'name': 'docker.service',
                  'dropins': [
                      {'name': '10-wait-docker.conf',
                       'contents': open('config/10-wait-docker.conf').read()},
                  ]},
                 {'name': 'registry.service',
                  'enable': True,
                  'contents': open('config/registry.service').read()},
                 {'name': 'gogs.service',
                  'enable': True,
                  'contents': open('config/gogs.service').read()},
                 {'name': 'development.service',
                  'enable': True,
                  'contents': open('config/development.service').read()},
             ]}},
    ]

except StandardError as e:
    sys.stderr.write("failed to generate configuration!")
    raise e
