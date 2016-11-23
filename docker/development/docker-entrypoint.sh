#!/bin/bash

# fetch token
/usr/bin/get-token

# run ansible
cd /var/local/ansible
ansible-playbook --vault-password-file=/usr/sbin/vault_pass setup.yml

# supervisord
exec /usr/bin/supervisord
