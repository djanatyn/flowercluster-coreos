#!/bin/bash

dnf install -y git sudo python-pip clang python-devel redhat-rpm-config openssl-devel libffi-devel python2-cffi python2-dnf

useradd -r -M -U ansible

mkdir /var/local/zubkoland
chown -R ansible:ansible /var/local/zubkoland

pip install ansible
