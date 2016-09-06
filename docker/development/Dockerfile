FROM stable:5000/fedora-ansible:latest

ADD ./vault_pass /root/vault_pass

RUN git clone http://git.flowercluster.io/flowercluster/flowercluster-development.git /var/local/ansible
RUN chown -R ansible:ansible /var/local/ansible

RUN dnf install -y openssh-server passwd @development-tools
RUN ssh-keygen -A

RUN ansible-galaxy install -r /var/local/ansible/requirements.yml
RUN cd /var/local/ansible && ansible-playbook --vault-password-file=/root/vault_pass setup.yml && chmod a-rwx /root/vault_pass
