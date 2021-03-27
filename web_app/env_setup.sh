#!/bin/bash

# install htop
apt update
apt install htop -y

# verify version of python3
python3 --version

# install pip3
apt install python3-pip

# verify pip3 version
pip3 --version

# install flask
pip3 install flask

# install nginx
apt install nginx -y

# enable, start, and status nginx service
systemctl enable nginx
systemctl start nginx
systemctl status nginx

# clone repo containing nginx conf and python web apps
git clone https://github.com/njloden/python.git

# cd to web app dir within python repo
cd python/web_app

# backup config and copy in new config for web app
cp -p /etc/nginx/nginx.conf /etc/nginx/nginx.conf_ORIG
cp nginx.conf /etc/nginx/nginx.conf

# restart nginx service, and get status
systemctl restart nginx
systemctl status nginx

# startup all flask web applications
./start_all_web_apps.sh

# test out nginx, and direct connection to all three web applications
curl http://localhost:80
curl http://localhost:5001
curl http://localhost:5002
curl http://localhost:5003





