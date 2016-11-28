FROM fedora:24

# install basic development packages
RUN dnf install -y git sudo python-pip clang python-devel redhat-rpm-config openssl-devel libffi-devel python2-cffi python2-dnf openssh-server passwd @development-tools jq

# add ansible user + paths
RUN useradd -r -M -U ansible
RUN mkdir /var/local/ansible

# install ansible
RUN pip install ansible

# supervisord
RUN pip install supervisor
COPY supervisord.conf /etc/supervisord.conf

RUN ssh-keygen -A

# remove /run/nologin so PAM works
RUN test -f /run/nologin && rm /run/nologin

CMD ["/usr/bin/supervisord"]
