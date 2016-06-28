FROM fedora-ansible:latest

ADD ./vault_pass /tmp/vault_pass

RUN git clone https://github.com/djanatyn/zubkoland.git /var/local/zubkoland
RUN chown -R ansible:ansible /var/local/zubkoland

RUN ansible-galaxy install -r /var/local/zubkoland/requirements.yml
RUN cd /var/local/zubkoland && ansible-playbook --vault-password-file=/tmp/vault_pass setup.yml
