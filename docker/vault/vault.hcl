backend "file" {
  path = "/vault/file"
}

default_lease_ttl = "168h"

listener "tcp" {
  address = "0.0.0.0:8200"
  tls_disable = 1
}
