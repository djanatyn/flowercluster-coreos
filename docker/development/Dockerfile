FROM flowercluster/fedora-ansible:latest

ARG SECRET_TOKEN
ARG ROLE_ID

ADD ./get-secret-id /usr/bin/get-secret-id
ADD ./get-token /usr/bin/get-token

RUN echo ${SECRET_TOKEN} > /var/local/SECRET_TOKEN 
RUN echo ${ROLE_ID} > /var/locala/ROLE_ID

RUN git clone http://git.flowercluster.io/flowercluster/flowercluster-development.git /var/local/ansible
RUN ansible-galaxy install -r /var/local/ansible/requirements.yml
RUN chown -R ansible:ansible /var/local/ansible

RUN dnf install -y openssh-server passwd @development-tools
RUN ssh-keygen -A

RUN pip install supervisor
COPY supervisord.conf /etc/supervisord.conf

ADD ./docker-entrypoint.sh /usr/bin/docker-entrypoint
# RUN cd /var/local/ansible && ansible-playbook --vault-password-file=/root/vault_pass setup.yml && chmod a-rwx /root/vault_pass

CMD ["/usr/bin/docker-entrypoint"]
