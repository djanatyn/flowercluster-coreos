#!/usr/bin/env python

import argparse
from init.vault import Vault


def parse_args():
    parser = argparse.ArgumentParser(description='initialize flowercluster containers on boot')
    parser.add_argument('token', type=str, help='build token for vault')
    parser.add_argument('--policy', '-p', action='store_true', help='update policies and AppRoles')

    return parser.parse_args()


def main():
    """ Command-line interface to running init functions. """

    args = parse_args()

    vault = Vault(args.token)
    if args.policy:
        vault.update_policies()
        vault.update_approles()

if __name__ == '__main__':
    main()
