#!/bin/bash

echo -en "Starting Docker"
sudo docker run -dp 8001:80 actix-server

sudo docker run -dp 8002:80 gunicorn-server

sudo docker run -dp 8003:80 node-server

sudo docker run -dp 8004:80 golang-server

sudo docker run -dp 8006:80 hyper-server