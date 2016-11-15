path "auth/approle/role/ansible/secret-id" {
  policy = "write"
}

path "auth/approle/role/ansible/role-id" {
  policy = "read"
}
