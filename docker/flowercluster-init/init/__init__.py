#!/usr/bin/env python

import logging

import vault

log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(format=log_format)

__all__ = ['vault']
