#!/bin/bash
# standard form: sudo ./env_setup.sh

# install htop
apt update
apt install htop -y

# install curl
apt install curl -y

# verify version of python3
python3 --version

# install pip3
apt install python3-pip -y

# verify pip3 version
pip3 --version

# install flask
pip3 install flask

# install nginx
apt install nginx -y

# enable, start, and status nginx service
systemctl enable nginx
systemctl start nginx
systemctl status nginx | grep Active

# backup config and copy in new config for web app
cp -p /etc/nginx/nginx.conf /etc/nginx/nginx.conf_ORIG
cp nginx.conf /etc/nginx/nginx.conf

# restart nginx service, and get status
systemctl restart nginx
systemctl status nginx | grep Active


