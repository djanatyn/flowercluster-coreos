#!/usr/bin/env python

import argparse

import init


def parse_args():
    parser = argparse.ArgumentParser(description='initialize flowercluster containers on boot')
    parser.add_argument('token', type=str, help='build token for vault')
    parser.add_argument('--policy', '-p', action='store_true', help='write policies')
    parser.add_argument('--approles', '-a', action='store_true', help='write approles')
    parser.add_argument('--build', '-b', action='store_true', help='build images')
    parser.add_argument('--start', '-s', action='store_true', help='start containers')
    parser.add_argument('--initialize', '-i', action='store_true', help='initialize everything')

    return parser.parse_args()


def main():
    """ Command-line interface to running init functions. """

    args = parse_args()

    if args.initialize:
        init.write_policies(args.token)
        init.write_approles(args.token)
        init.build_images(token=args.token)
        init.start_containers(token=args.token)
    else:
        if args.policy:
            init.write_policies(args.token)

        if args.approles:
            init.write_approles(args.token)

        if args.build:
            init.build_images(token=args.token)

        if args.start:
            init.start_containers(token=args.token)


if __name__ == '__main__':
    main()
