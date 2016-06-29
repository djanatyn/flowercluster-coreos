flowercluster
=============

flowercluster is a CoreOS cluster running on Google Compute Engine.

the goal is an entirely reproducible, fault-tolerant, mostly stateless distributed compute cluster to run web applications and daemon services in containers.

---

there are four main nodes: proxy, web, stable, and development.

- the proxy nodes grab IPs from the public subnet (10.0.3.0/24) and recieve requests hitting flowercluster.io. requests are routed based on the port number or 'Host' header to the web nodes and the stable node. it's storage is entirely ephemeral, only running haproxy. 

- the web nodes runs nginx and routes HTTP requests to containers running web applications, based on their 'Host' parameter. they are entirely stateless and do not attach any persistent volumes.

- the stable node is intended to be running at all times - it runs the docker registry, holds the code in git, runs monitoring, and several other essential services. an ext4 GCS drive is mounted as /var/lib/docker to keep the images and containers consistent across new instances.

- the development node launches a fedora rawhide development server with user accounts created and some development packages installed. a GCS ext4 volume is mounted as /home/ and is consistent across new instances.
