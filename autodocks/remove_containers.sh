#!/bin/bash

sudo docker rm $(sudo docker ps -a -f status=exited -q)