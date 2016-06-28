overview
========
there are four main instances that flowercluster.io needs to function:

proxy
-----
flowercluster.io requests get sent here first

this runs haproxy and redirects requests to instances in the web subnet block. multiple proxies can be launched to deal with lots of requests

redirects:
- shell.flowercluster.io -> development:22

- whalespeak.flowercluster.io -> whalespeak web application
- git.flowercluster.io -> gogs http
- monitoring.flowercluster.io -> sensu interface
- files.flowercluster.io -> owncloud

proxy listens on ports 80, 443, and 22. it does not run an sshd (?)

mail directed to djanatyn@flowercluster.io needs to get to the mail instance running on stable somehow.
can mail be handled by an external google service?

web
---
- web applications
- whalespeak

- nginx

these should be using persistent letsencrypt certificates, but the process should be automated!
these are stateless instances; any state should be stored elsewhere

nginx with docker-gen proxies based on the Host header to the ips of running container instances. https://hub.docker.com/r/jwilder/nginx-proxy/
we can show an error page if there's nothing to proxy to

these contain ssl certs that are added when the docker image is created. this means we need to make a new docker image when we update our certs, but the process is automated with letsencrypt.

these instances are created inside a special subnet block which the proxy instances load balance requests to

stable
------
this runs core services that need to be up 24/7

- gogs
- docker registry
- configuration managed by ansible
- irc
- mail
- owncloud
- monitoring with sensu

when launched, the stable instances mounts a persistent 500GB volume from GCS
the registry is launched as a systemd unit and the volumes are stored on the volume

development
-----------
- development server, pulled from docker registry
- docker volume is backed by persistent ssd gcs volume attached to instance on creation
- reproducible!

- only /home/ should be persistent - about 20GB

this is not meant to go down, but it can.
