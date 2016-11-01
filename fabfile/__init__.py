#!/usr/bin/env python

from fabric_gce_tools import update_roles_gce

import vault
import instances

update_roles_gce(use_cache=False)

__all__ = ['instances', 'vault']
