#!/bin/bash

# fetch token inside container it doesn't exist
if [[ ! -f /root/vault_token ]]; then
  echo "no token found inside container!"

  if [[ $# -eq 0 ]]; then
    echo "please pass a SecretID wrap token as an argument!"
    exit 1
  fi

  SECRET_TOKEN=$1
  exec /usr/bin/get-token $(/usr/bin/get-secret-id ${SECRET_TOKEN})
fi

# run ansible
/usr/bin/update_development

# supervisord
exec /usr/bin/supervisord
