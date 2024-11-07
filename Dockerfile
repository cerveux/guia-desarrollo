FROM odoo:15.0

COPY ./config/odoo.conf /etc/odoo/
# COPY ./gitman.yml /usr/lib/python3/dist-packages/odoo/

COPY ./install_dependencies.sh /usr/lib/python3/dist-packages/odoo/
USER root

RUN apt update && apt install git openssh-server -y

RUN python3 -m pip install debugpy gitman
# RUN gitman install -r /usr/lib/python3/dist-packages/odoo/

CMD python3 -m debugpy --listen 0.0.0.0:8888 /usr/bin/odoo -c /etc/odoo/odoo.conf