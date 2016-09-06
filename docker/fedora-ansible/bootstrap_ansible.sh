#!/bin/bash

dnf install -y git sudo python-pip clang python-devel redhat-rpm-config openssl-devel libffi-devel python2-cffi python2-dnf

useradd -r -M -U ansible

mkdir /var/local/ansible
chown -R ansible:ansible /var/local/ansible

pip install ansible
