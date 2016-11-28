FROM flowercluster/fedora-ansible:latest

ARG ROLE_ID

# save one-time-use SecretID and RoleID
ADD ./get-secret-id /usr/bin/get-secret-id
ADD ./get-token /usr/bin/get-token
ADD ./vault_pass /usr/sbin/vault_pass
ADD ./update_development /usr/bin/update_development

RUN echo ${ROLE_ID} > /root/role-id

# add flowercluster repository
RUN git clone http://github.com/djanatyn/flowercluster-development /var/local/ansible
RUN ansible-galaxy install -r /var/local/ansible/requirements.yml
RUN chown -R ansible:ansible /var/local/ansible

# RUN cd /var/local/ansible && ansible-playbook --vault-password-file=/root/vault_pass setup.yml && chmod a-rwx /root/vault_pass

ADD ./docker-entrypoint.sh /usr/bin/docker-entrypoint
ENTRYPOINT ["/usr/bin/docker-entrypoint"]
