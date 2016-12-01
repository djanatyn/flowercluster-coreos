#!/usr/bin/env python

import requests
import logging

log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(format=log_format)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

__all__ = []
