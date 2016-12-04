#!/bin/bash

# fetch token inside container it doesn't exist
if [[ ! -f /root/vault_token ]]; then
  echo "no token found inside container!"

  if [[ $# -eq 0 ]]; then
    echo "please pass a SecretID wrap token as an argument!"
    exit 1
  fi

  SECRET_TOKEN=$1
  /usr/bin/get-token $(/usr/bin/get-secret-id ${SECRET_TOKEN})

  if [[ $? -ne 0 ]]; then
    exit 1
  fi
fi

# run ansible
cd /var/local/ansible && sudo -u ansible git pull
ansible-playbook -i hosts setup.yml --vault-password-file=/usr/sbin/vault_pass

# supervisord
exec /usr/bin/supervisord
