#!/bin/bash

if [[ ! -f /root/vault_token ]]; then
  # fetch token
  SECRET_TOKEN=$1

  /usr/bin/get-token $(/usr/bin/get-secret-id ${SECRET_TOKEN}) >/dev/null

  if [[ $? != 0 ]]; then
    echo "failed to get AppRole token!"
    exit 1
  fi
fi

# run ansible
cd /var/local/ansible
ansible-playbook --vault-password-file=/usr/sbin/vault_pass setup.yml

# supervisord
exec /usr/bin/supervisord
