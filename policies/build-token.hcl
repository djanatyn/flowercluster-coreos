# we need to create approles + policies
path "auth/approle/role/*" {
  policy = "write"
}

path "sys/policy/*" {
  policy = "write"
}
