#!/bin/bash

# fetch token
SECRET_TOKEN=$(cat /root/secret-token)
/usr/bin/get-token $(/usr/bin/get-secret-id ${SECRET_TOKEN})

# run ansible
cd /var/local/ansible
ansible-playbook --vault-password-file=/usr/sbin/vault_pass setup.yml

# supervisord
exec /usr/bin/supervisord
